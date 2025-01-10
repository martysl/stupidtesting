from flask import Flask, request, jsonify, send_file
from pytube import YouTube
import logging

app = Flask(__name__)

logging.basicConfig(level=logging.DEBUG)

@app.route('/')
def index():
    return '<h1>This API is private and made by AI</h1>'

@app.route('/ytdl', methods=['POST'])
def download():
    try:
        url = request.json.get('url')
        if not url:
            return jsonify({'error': 'URL is required'}), 400
        yt = YouTube(url)
        stream = yt.streams.filter(only_audio=True).first()
        file_path = stream.download()
        return send_file(file_path, as_attachment=True, attachment_filename='audio.mp3')
    except Exception as e:
        logging.error(f"Error: {e}")
        return jsonify({'error': 'Failed to download video'}), 500

if __name__ == '__main__':
    app.run(debug=True)
