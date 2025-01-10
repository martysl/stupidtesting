from flask import Flask, request, jsonify, send_file
from ytube_api import Ytube
import logging
import os
import tempfile

# Create a new Flask app
app = Flask(__name__)

# Set up logging to debug level
logging.basicConfig(level=logging.DEBUG)

# Define the index route
@app.route('/')
def index():
    # Return a simple HTML page with a message
    return '<body style="background-color:black; color:white;"><h1>This API is private and made by AI</h1></body>'

# Define the ytdl route
@app.route('/ytdl', methods=['POST'])
def download_video():
    # Get the URL from the request body
    url = request.json.get('url')
    
    # Check if the URL is provided
    if not url:
        # Return an error response if the URL is not provided
        return jsonify({'error': 'URL is required'}), 400
    
    # Create a new Ytube object
    yt = Ytube()
    
    # Search for videos using the provided URL
    search_results = yt.search_videos(url)
    
    # Get the first search result
    target_video = search_results.items[0]
    
    # Get the download link for the target video
    download_link = yt.get_download_link(target_video, format="mp3", quality="320")
    
    # Return the download link as a JSON response
    return jsonify({'download_link': download_link.url})

# Run the app in debug mode
if __name__ == '__main__':
    app.run(debug=True)
