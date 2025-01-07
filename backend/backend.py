from flask import Flask, request, jsonify
from flask_cors import CORS
from dotenv import load_dotenv
import os
import google.generativeai as genai
from youtube_transcript_api import YouTubeTranscriptApi

load_dotenv()

app = Flask(__name__)

CORS(app, resources={r"/*": {"origins": "http://127.0.0.1:5500"}})

port = int(os.environ.get('PORT', 5000))

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
model = genai.GenerativeModel("gemini-1.5-flash")

@app.route('/process', methods=['POST'])
def send_response():
    try:
        video_id = request.json.get('id')
        if not video_id:
            return jsonify({"error": "Missing video ID"}), 400

        transcript_data = YouTubeTranscriptApi.get_transcript(video_id)
        transcript = " ".join([item['text'] for item in transcript_data])

        response = model.generate_content(
            "The following is a transcript from a Youtube video. Tell me what the video is about: " + transcript
        )

        return jsonify({"summary": response.text})

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, port=port)
