import os
from fastapi import FastAPI, File, UploadFile, Form
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from typing import Optional
import yt_dlp
import shutil

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
