from fastapi import FastAPI, Query
from pedalboard import Pedalboard, Reverb, PitchShift, LowpassFilter, Distortion, Gain
from pedalboard.io import AudioFile
from pydub import AudioSegment
import os

app = FastAPI()

# Define output directory for processed files
OUTPUT_DIR = "processed_audio"
os.makedirs(OUTPUT_DIR, exist_ok=True)

@app.post("/apply-effects/")
async def apply_effects(
    file: str = Query(...),  # File name from the frontend
    Reverb: float = Query(...),  # Reverb level (0-100)
    PitchShift: float = Query(...),  # Pitch Shift (semitones)
    LowpassFilter: float = Query(...),  # Lowpass Filter frequency (Hz)
    Distortion: float = Query(...),  # Distortion level (0-100)
    Gain: float = Query(...),  # Gain (dB)
    Speed: float = Query(...),  # Speed (percentage, 100 = normal speed)
):
    try:
        # Step 1: Load the merged file from the "downloads" folder
        merged_file_path = os.path.join('downloads', file)  # Path to the merged file
        if not os.path.exists(merged_file_path):
            return {"status": "error", "message": "File not found."}

        audio = AudioSegment.from_file(merged_file_path, format="wav")

        # Step 2: Export to temporary file for Pedalboard
        temp_file = "temp_file.wav"
        audio.export(temp_file, format="wav")

        # Load the temporary file into Pedalboard
        with AudioFile(temp_file) as f:
            audio_data = f.read(f.frames)
            sample_rate = f.samplerate

        # Create Pedalboard effects
        board = Pedalboard([
            Reverb(room_size=Reverb / 100),  # Reverb level (scaled 0-1)
            PitchShift(semitones=PitchShift),  # Pitch shift in semitones
            LowpassFilter(cutoff_hz=LowpassFilter),  # Lowpass filter frequency
            Distortion(drive_db=Distortion),  # Distortion level
            Gain(gain_db=Gain)  # Gain in dB
        ])

        # Apply Pedalboard effects
        effected = board(audio_data, sample_rate)

        # Step 3: Apply speed change if necessary
        if Speed != 100:
            audio = audio.speedup(playback_speed=Speed / 100)
            audio.export(temp_file, format="wav")  # Update the temp file with new speed

        # Step 4: Save the final output to the "processed_audio" folder
        output_audio_path = os.path.join(OUTPUT_DIR, "final_lofi_output.wav")
        with AudioFile(output_audio_path, 'w', sample_rate, effected.shape[0]) as f:
            f.write(effected)

        # Clean up temporary files
        os.remove(temp_file)

        return {"status": "success", "file": output_audio_path}  # Return the processed file path

    except Exception as e:
        return {"status": "error", "message": str(e)}  # Return error message
