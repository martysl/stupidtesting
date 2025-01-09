from flask import Flask, request, jsonify, send_file
from pytube import YouTube
import os

app = Flask(__name__)

DOWNLOAD_DIR = "/tmp"  # Dla Vercel, używamy /tmp do przechowywania plików tymczasowych

@app.route('/api/download', methods=['POST'])
def download():
    data = request.get_json()
    url = data.get('url')

    if not url:
        return jsonify({"error": "No URL provided"}), 400

    try:
        yt = YouTube(url)
        audio_stream = yt.streams.filter(only_audio=True).first()
        output_path = os.path.join(DOWNLOAD_DIR, f"{yt.title}.mp3")
        
        # Pobranie pliku audio
        audio_stream.download(DOWNLOAD_DIR, filename=f"{yt.title}.mp3")

        return jsonify({"link": f"/api/file/{yt.title}.mp3"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/file/<filename>', methods=['GET'])
def get_file(filename):
    file_path = os.path.join(DOWNLOAD_DIR, filename)
    if os.path.exists(file_path):
        return send_file(file_path, as_attachment=True)
    else:
        return jsonify({"error": "File not found"}), 404

if __name__ == "__main__":
    app.run()
