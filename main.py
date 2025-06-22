import os
import shutil
import yt_dlp
from fastapi import FastAPI, File, UploadFile, Form, HTTPException, Request
from fastapi.responses import JSONResponse, FileResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from typing import Optional, List
from pydantic import BaseModel
from pathlib import Path
from merge_and_cleanup import merge_and_cleanup  # Import your merge and cleanup function
from lalal_split import split_file_with_lalal
from pedalboard import Pedalboard, Reverb, Compressor, PitchShift, LowpassFilter, Distortion, Gain
from pedalboard.io import AudioFile
from pydub import AudioSegment
import logging

# Set up logging
logging.basicConfig(level=logging.DEBUG)

app = FastAPI()

# Allow frontend to talk to backend (adjust origins for production)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Change to frontend domain in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Ensure download folder exists
DOWNLOAD_DIR = "downloads"
os.makedirs(DOWNLOAD_DIR, exist_ok=True)

# Model for split request
class SplitRequest(BaseModel):
    file: str
    stems: List[str]

@app.post("/convert/")
async def convert_audio(
    youtube_url: Optional[str] = Form(None),
    file: Optional[UploadFile] = File(None)
):
    if youtube_url:
        try:
            ydl_opts = {
                'format': 'bestaudio/best',
                'outtmpl': os.path.join(DOWNLOAD_DIR, '%(title)s.%(ext)s'),
                'postprocessors': [{
                    'key': 'FFmpegExtractAudio',
                    'preferredcodec': 'mp3',
                    'preferredquality': '192',
                }],
            }

            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(youtube_url, download=True)
                filename = ydl.prepare_filename(info).rsplit('.', 1)[0] + '.mp3'

            return JSONResponse({"status": "success", "filename": os.path.basename(filename)})
        except Exception as e:
            return JSONResponse({"status": "error", "message": str(e)}, status_code=500)

    elif file:
        try:
            file_ext = file.filename.rsplit('.', 1)[-1].lower()
            if file_ext not in ['mp3', 'wav', 'flac', 'm4a']:
                return JSONResponse({"status": "error", "message": "Invalid file type"}, status_code=400)

            file_path = os.path.join(DOWNLOAD_DIR, file.filename)
            with open(file_path, "wb") as buffer:
                shutil.copyfileobj(file.file, buffer)

            return JSONResponse({"status": "success", "filename": file.filename})
        except Exception as e:
            return JSONResponse({"status": "error", "message": str(e)}, status_code=500)

    else:
        return JSONResponse({"status": "error", "message": "No input provided"}, status_code=400)

@app.post("/split/")
async def split_audio(data: SplitRequest):
    try:
        file_path = os.path.join(DOWNLOAD_DIR, data.file)
        if not os.path.exists(file_path):
            return JSONResponse({"status": "error", "message": "File not found"}, status_code=404)

        # Split the audio file into stems
        result = split_file_with_lalal(file_path, data.stems)

        # If splitting is successful, merge the stems
        if result.get("status") == "ok":
            try:
                # Merge and clean up the files
                merged_output_path = merge_and_cleanup("split")
                result["merged"] = merged_output_path
            except Exception as e:
                result["merged"] = None
                print(f"⚠️ Merge failed: {e}")

        return JSONResponse(result)

    except Exception as e:
        return JSONResponse({"status": "error", "message": str(e)}, status_code=500)

# Directory for storing processed audio
OUTPUT_DIR = "processed_audio"
os.makedirs(OUTPUT_DIR, exist_ok=True)

@app.post("/process-effects")
async def process_effects(request: Request):
    try:
        # Receive data from the frontend
        data = await request.json()

        # Log the received data
        logging.debug(f"Received data: {data}")

        # Ensure the values are correctly parsed as numbers (float or int)
        reverb_value = float(data["Reverb"])  # Reverb should match the frontend's key
        pitch_shift_value = float(data["PitchShift"])  # PitchShift in semitones
        lowpass_filter_value = float(data["LowpassFilter"])  # Lowpass Filter (Hz)
        distortion_value = float(data["Distortion"])  # Distortion (dB)
        gain_value = float(data["Gain"])  # Gain (dB)

        # Log the parsed values
        logging.debug(f"Parsed values - Reverb: {reverb_value}, Pitch Shift: {pitch_shift_value}, "
                      f"Lowpass Filter: {lowpass_filter_value}, Distortion: {distortion_value}, Gain: {gain_value}")

        # Define the path to the input audio (from split/merge)
        input_audio_path = "split/merged_output.wav"  # Adjust this based on where your final merged audio is stored
        if not os.path.exists(input_audio_path):
            raise FileNotFoundError(f"Input audio file not found at: {input_audio_path}")

        # Load the audio file
        with AudioFile(input_audio_path) as f:
            audio = f.read(f.frames)
            sample_rate = f.samplerate

        # Apply the effects using Pedalboard
        board = Pedalboard([
            Reverb(room_size=reverb_value),  # Reverb scaled between 0-1
            PitchShift(semitones=pitch_shift_value),  # Pitch shift in semitones
            LowpassFilter(cutoff_frequency_hz=lowpass_filter_value),  # Lowpass filter frequency (Hz)
            Distortion(drive_db=distortion_value),  # Distortion level (dB)
            Gain(gain_db=gain_value),  # Gain (dB)
        ])

        # Apply the effects to the audio
        processed_audio = board(audio, sample_rate)

        # Define the output file path
        output_audio_path = os.path.join("processed_audio", "final_lofi_output.wav")

        # Save the processed audio to the file system
        with AudioFile(output_audio_path, 'w', sample_rate, processed_audio.shape[0]) as f:
            f.write(processed_audio)

        # Log the success and return the path to the processed audio file
        logging.debug(f"Processed audio saved to: {output_audio_path}")
        return {"status": "success", "output_file": "processed_audio/final_lofi_output.wav"}

    except Exception as e:
        # Log the error and return a detailed error message
        logging.error(f"Error processing effects: {e}")
        return {"status": "error", "message": str(e)}

# Serve files from the 'processed_audio' directory
app.mount("/processed_audio", StaticFiles(directory="processed_audio"), name="processed_audio")

@app.get("/processed_audio/{filename}")
async def get_audio_file(filename: str):
    file_path = os.path.join("processed_audio", filename)
    
    # Check if the file exists
    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="File not found")
    
    return FileResponse(file_path)