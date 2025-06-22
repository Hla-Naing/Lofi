import os
import shutil
import yt_dlp
from fastapi import FastAPI, File, UploadFile, Form
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from typing import Optional, List
from pydantic import BaseModel
from merge_and_cleanup import merge_and_cleanup


# Import the splitting logic from lalal_split.py
from lalal_split import split_file_with_lalal

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

@app.get("/split/{id}")
async def debug_unexpected_get(id: str):
    print(f"⚠️ Unexpected GET request to /split/{id}")
    return JSONResponse(
        {"status": "error", "message": f"GET /split/{id} is not allowed."},
        status_code=405
    )

@app.post("/split/")
async def split_audio(data: SplitRequest):
    try:
        file_path = os.path.join(DOWNLOAD_DIR, data.file)
        if not os.path.exists(file_path):
            return JSONResponse({"status": "error", "message": "File not found"}, status_code=404)

        result = split_file_with_lalal(file_path, data.stems)

        if result.get("status") == "ok":
            try:
                merged_path = merge_and_cleanup("split")
                result["merged"] = merged_path
            except Exception as e:
                result["merged"] = None
                print(f"⚠️ Merge failed: {e}")

        return JSONResponse(result)

    except Exception as e:
        return JSONResponse({"status": "error", "message": str(e)}, status_code=500)
