from flask import Flask, request, jsonify
from flask_cors import CORS
from dotenv import load_dotenv
import re
import requests
from bs4 import BeautifulSoup
import os
import google.generativeai as genai
from youtube_transcript_api import YouTubeTranscriptApi
import logging
logger = logging.getLogger(__name__)


load_dotenv()

app = Flask(__name__)

CORS(app, resources={r"/*": {"origins": "http://127.0.0.1:5000"}})

port = int(os.environ.get('PORT', 5000))

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
model = genai.GenerativeModel("gemini-1.5-flash")


def extract_video_id(url):
    match = re.search(r'(?:v=|\/)([0-9A-za-z_-]{11})', url)
    return match.group(1) if match else None


def get_video_title(url):
    try:
        r = requests.get(url)
        r.raise_for_status()
        soup = BeautifulSoup(r.text, 'html.parser')
        title_tag = soup.find('title')
        return title_tag.text if title_tag else "Unknown Title"
    except Exception as e:
        print(f"Error fetching video title: {e}")
        return "Unknown Title"


@app.route('/process/', methods=['POST'])
def send_response():
    try:
        if not request.is_json:
            return jsonify({"error": "Invalid content type. JSON expected."}), 400

        data = request.get_json()
        link = data.get('link')
        if not link:
            return jsonify({"error": "Missing link parameter"}), 400

        specifics = data.get('specifics', '')
        video_id = extract_video_id(link)
        if not video_id:
            return jsonify({"error": "Invalid or missing video ID"}), 400

        title = get_video_title(link)
        logger.info('-------------------->')
        transcript_data = ''
        try:
            transcript_data = YouTubeTranscriptApi.get_transcript(video_id)
            logger.info(transcript_data)
        except Exception as e:
            print(f"Error fetching transcript: {e}")
        # print(transcript_data)
        transcript = " ".join([item['text'] for item in transcript_data])

        prompt = (
            "The following is a transcript from a YouTube video. "
            "Tell me what the video is about: " + transcript
        )
        if specifics:
            prompt += f" Please focus on the following aspects: {specifics}"

        response = model.generate_content(prompt)

        if not hasattr(response, 'text') or not response.text:
            return jsonify({"error": "Failed to generate content"}), 500

        return jsonify({
            "title": title,
            "summary": response.text
        })

    except Exception as e:
        return jsonify({"error": transcript_data + str(e)}), 500


if __name__ == '__main__':
    app.run(debug=True, port=port)
