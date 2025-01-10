from flask import Flask, request, jsonify, send_file
from pytube import YouTube

app = Flask(__name__)

@app.route('/')
def index():
    return '<h1>This API is private and made by AI</h1>'

@app.route('/ytdl', methods=['POST'])
def download():
    url = request.json.get('url')
    if not url:
        return jsonify({'error': 'URL is required'}), 400

    try:
        yt = YouTube(url)
        stream = yt.streams.filter(only_audio=True).first()
        if not stream:
            return jsonify({'error': 'No audio stream found'}), 404
        file_path = stream.download()
        return send_file(file_path, as_attachment=True, attachment_filename='audio.mp3')
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run()
