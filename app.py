from flask import Flask, request, jsonify, send_file
2	from pytube import YouTube
3	import logging
4	
5	app = Flask(__name__)
6	
7	logging.basicConfig(level=logging.DEBUG)
8	
9	@app.route('/')
10	def index():
11	    return '<h1>This API is private and made by AI</h1>'
12	
13	@app.route('/ytdl', methods=['POST'])
14	def download():
15	    try:
16	        url = request.json.get('url')
17	        if not url:
18	            return jsonify({'error': 'URL is required'}), 400
19	        yt = YouTube(url)
20	        stream = yt.streams.filter(only_audio=True).first()
21	        file_path = stream.download()
22	        return send_file(file_path, as_attachment=True, attachment_filename='audio.mp3')
23	    except Exception as e:
24	        logging.error(f"Error: {e}")
25	        return jsonify({'error': 'Failed to download video'}), 500
26	
27	if __name__ == '__main__':
28	    app.run(debug=True)
