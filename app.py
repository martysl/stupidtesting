from flask import Flask, request, jsonify, send_file
from pytubefix import YouTube
from pytubefix.cli import on_progress
import os
import tempfile
app = Flask(__name__)
# Download the MP3 file
def download_mp3(url):
yt = YouTube(url, on_progress_callback=on_progress)
print(yt.title)
ys = yt.streams.get_audio_only()
filename = yt.title + '.mp3'
ys.download(filename=filename)
return filename
# Route to download the MP3 file
@app.route('/ytdl', methods=['POST'])
def download_video():
url = request.json.get('url')
if not url:
return jsonify({'error': 'URL is required'}), 400
filename = download_mp3(url)
return jsonify({'message': 'File downloaded successfully!', 'url': f'/file/{filename}'})
# Route to share the MP3 file
@app.route('/file/<filename>')
def share_file(filename):
return send_file(filename, as_attachment=True)
if __name__ == '__main__':
app.run(debug=True)
