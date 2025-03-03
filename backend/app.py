from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
import os
import yt_dlp

app = FastAPI()

DOWNLOAD_FOLDER = "downloads"
os.makedirs(DOWNLOAD_FOLDER, exist_ok=True)

def download_youtube_audio(youtube_url, output_dir="downloads"):
    os.makedirs(output_dir, exist_ok=True)
    output_template = os.path.join(output_dir, "%(title)s.%(ext)s")

    ydl_opts = {
        "format": "bestaudio/best",
        "outtmpl": output_template,
        "postprocessors": [{
            "key": "FFmpegExtractAudio",
            "preferredcodec": "mp3",
            "preferredquality": "192",
        }]
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info_dict = ydl.extract_info(youtube_url, download=True)
            file_path = ydl.prepare_filename(info_dict).replace(".webm", ".mp3").replace(".m4a", ".mp3")
            return file_path
    except Exception as e:
        print(f"Error downloading video: {str(e)}")
        return None

@app.post("/convert")
async def convert(data: dict):
    youtube_url = data.get("youtube_url")
    if not youtube_url:
        raise HTTPException(status_code=400, detail="No YouTube URL provided")

    mp3_file = download_youtube_audio(youtube_url, DOWNLOAD_FOLDER)
    if not mp3_file:
        raise HTTPException(status_code=500, detail="Failed to download and convert video")

    return FileResponse(mp3_file, filename=os.path.basename(mp3_file), media_type='audio/mpeg')
