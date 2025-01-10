from flask import Flask, request, jsonify, send_file
from pytube import YouTube
import logging
import os
import tempfile

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
        logging.debug(f"Downloading video from URL: {url}")
        yt = YouTube(url)
        logging.debug(f"Video title: {yt.title}")
        stream = yt.streams.filter(only_audio=True).first()
        if stream is None:
            logging.error(f"No audio stream found for URL: {url}")
            return jsonify({
                'error': 'No audio stream found',
                'details': f'URL: {url}'
            }), 404
        logging.debug(f"Audio stream found: {stream}")
        tmp_dir = tempfile.gettempdir()
        file_path = os.path.join(tmp_dir, 'audio.mp3')
        try:
            stream.download(output_path=tmp_dir, filename='audio.mp3')
        except Exception as e:
            logging.error(f"Error downloading video: {e}")
            return jsonify({
                'error': 'Failed to download video',
                'details': f'URL: {url}, Error: {str(e)}'
            }), 500
        logging.debug(f"File downloaded to: {file_path}")
        return send_file(file_path, as_attachment=True, attachment_filename='audio.mp3')
    except Exception as e:
        logging.error(f"Error: {e}")
        return jsonify({
            'error': 'An error occurred',
            'details': f'Error: {str(e)}'
        }), 500

if __name__ == '__main__':
    app.run(debug=True)
