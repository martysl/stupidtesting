from flask import Flask, request, jsonify, send_file, render_template_string
from pytubefix import YouTube
from pytubefix.cli import on_progress
import os

app = Flask(__name__)

DOWNLOAD_DIR = "/tmp"  # Katalog tymczasowy dla Vercel

# Strona główna z logo
@app.route('/')
def index():
    html = """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>YouTube to MP3 API</title>
        <style>
            body {
                background-color: #000;
                color: #fff;
                text-align: center;
                font-family: Arial, sans-serif;
            }
            img {
                margin-top: 20px;
                width: 300px;
            }
        </style>
    </head>
    <body>
        <h1>YouTube to MP3 API</h1>
        <p>Welcome to EasierIT's YouTube to MP3 API!</p>
        <img src="http://easierit.org/logo-pp.png" alt="EasierIT Logo">
    </body>
    </html>
    """
    return render_template_string(html)

# Endpoint do pobierania MP3
@app.route('/api/download', methods=['POST'])
def download():
    data = request.get_json()
    url = data.get('url')

    if not url:
        return jsonify({"error": "No URL provided"}), 400

    try:
        yt = YouTube(url, on_progress_callback=on_progress)
        audio_stream = yt.streams.get_audio_only()

        # Ustawienie ścieżki do pliku
        output_path = os.path.join(DOWNLOAD_DIR, f"{yt.title}.mp3")

        # Pobieranie audio
        audio_stream.download(output_path=DOWNLOAD_DIR, filename=f"{yt.title}.mp3")

        return jsonify({"link": f"/api/file/{yt.title}.mp3"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Endpoint do pobierania pliku
@app.route('/api/file/<filename>', methods=['GET'])
def get_file(filename):
    file_path = os.path.join(DOWNLOAD_DIR, filename)
    if os.path.exists(file_path):
        return send_file(file_path, as_attachment=True)
    else:
        return jsonify({"error": "File not found"}), 404

if __name__ == "__main__":
    app.run(debug=True)
