from flask import Flask, request, jsonify
from pytube import YouTube

app = Flask(__name__)

@app.route('/ytdl', methods=['POST'])
def download_mp3():
    data = request.json
    url = data.get('url')

    if not url:
        return jsonify({'error': 'URL is required'}), 400

    try:
        yt = YouTube(url)
        stream = yt.streams.filter(only_audio=True).first()
        link = stream.download()
        return jsonify({'link': link})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
