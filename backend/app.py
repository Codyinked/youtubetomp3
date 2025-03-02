from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
import os
from youtube_downloader import download_youtube_audio

# Initialize Flask app
app = Flask(__name__)
CORS(app)  # Allow frontend access

# Ensure downloads folder exists
DOWNLOAD_FOLDER = "downloads"
os.makedirs(DOWNLOAD_FOLDER, exist_ok=True)

# Ensure FFmpeg is available
os.environ["PATH"] += os.pathsep + "/usr/bin"

@app.route('/convert', methods=['POST'])
def convert():
    """ API to download and convert YouTube video to MP3 """
    try:
        data = request.json
        youtube_url = data.get("youtube_url")

        if not youtube_url:
            return jsonify({"error": "No YouTube URL provided"}), 400

        # Download YouTube video as MP3
        mp3_file = download_youtube_audio(youtube_url, DOWNLOAD_FOLDER)

        if not mp3_file:
            return jsonify({"error": "Failed to download and convert"}), 500

        # Serve the MP3 file for download
        return send_file(mp3_file, as_attachment=True)

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
