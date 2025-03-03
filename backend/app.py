from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
import os
import yt_dlp

app = Flask(__name__)
CORS(app)

DOWNLOAD_FOLDER = "downloads"
os.makedirs(DOWNLOAD_FOLDER, exist_ok=True)  # Ensure the downloads folder exists

def download_youtube_audio(youtube_url, output_dir=DOWNLOAD_FOLDER):
    """Download a YouTube video as an MP3 file."""
    output_template = os.path.join(output_dir, "%(title)s.%(ext)s")

    ydl_opts = {
        "format": "bestaudio/best",
        "outtmpl": output_template,
        "postprocessors": [
            {
                "key": "FFmpegExtractAudio",
                "preferredcodec": "mp3",
                "preferredquality": "192",
            }
        ],
        "ffmpeg_location": "/usr/bin/ffmpeg",  # Ensure FFmpeg is correctly referenced
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info_dict = ydl.extract_info(youtube_url, download=True)
            file_path = ydl.prepare_filename(info_dict).replace(".webm", ".mp3").replace(".m4a", ".mp3")
            return file_path
    except Exception as e:
        print(f"Error downloading video: {str(e)}")
        return None

@app.route('/convert', methods=['POST'])
def convert():
    """API to download and convert YouTube video to MP3"""
    try:
        data = request.json
        youtube_url = data.get("youtube_url")

        if not youtube_url:
            return jsonify({"error": "No YouTube URL provided"}), 400

        mp3_file = download_youtube_audio(youtube_url, DOWNLOAD_FOLDER)

        if not mp3_file:
            return jsonify({"error": "Failed to download and convert"}), 500

        return send_file(mp3_file, as_attachment=True)

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
