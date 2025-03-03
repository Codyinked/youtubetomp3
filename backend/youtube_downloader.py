import yt_dlp
import os

def download_youtube_audio(youtube_url, output_dir="downloads"):
    """
    Downloads a YouTube video as MP3.
    """
    os.makedirs(output_dir, exist_ok=True)
    output_template = os.path.join(output_dir, "%(title)s.%(ext)s")

    ydl_opts = {
        "format": "bestaudio/best",
        "outtmpl": output_template,
        "postprocessors": [{
            "key": "FFmpegExtractAudio",
            "preferredcodec": "mp3",
            "preferredquality": "192",
        }],
        "ffmpeg_location": "/usr/bin/ffmpeg",  # Ensure ffmpeg is installed
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info_dict = ydl.extract_info(youtube_url, download=True)
            file_path = ydl.prepare_filename(info_dict).replace(".webm", ".mp3").replace(".m4a", ".mp3")
            return file_path
    except Exception as e:
        print(f"Error downloading video: {str(e)}")
        return None
