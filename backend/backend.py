import os
from flask_cors import CORS
from dotenv import load_dotenv
import google.generativeai as genai
from flask import Flask, request, jsonify
from youtube_transcript_api import YouTubeTranscriptApi
import logging
from .helpers import get_video_title, extract_video_id
logger = logging.getLogger(__name__)


load_dotenv()

app = Flask(__name__)

CORS(app, resources={r"/*": {"origins": "http://127.0.0.1:5000"}})

port = int(os.environ.get('PORT', 5000))

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
model = genai.GenerativeModel("gemini-1.5-flash")


@app.route('/convert-to-text/', methods=['POST'])
def convert_image_to_text():
    print('inside the function')
    if 'images' not in request.files:
        return jsonify({"message": "No images in the request"}), 400

    files = request.files.getlist('images')
    if not files:
        return jsonify({"message": "No images uploaded"}), 400

    results = []

    for img in files:
        image_bytes = img.read()
        mime_type = img.mimetype

        image_part = {
            'mime_type': mime_type,
            'data': image_bytes
        }

        response = model.generate_content([
            image_part,
            'Please extract all readable text from this image and give absolutely no input from your side.'
        ])

        extracted_text = response.text.strip() if response.text else 'No text found.'

        results.append({
            'filename': img.filename,
            'text': extracted_text
        })

    return jsonify({"results": results})


@app.route('/get-video-summary/', methods=['POST'])
def send_response():
    try:
        if not request.is_json:
            return jsonify({"message": "Invalid content type. JSON expected."}), 400

        data = request.get_json()
        link = data.get('link')
        if not link:
            return jsonify({"message": "Missing link parameter"}), 400

        specifics = data.get('specifics', '')
        video_id = extract_video_id(link)
        if not video_id:
            return jsonify({"message": "Invalid or missing video ID"}), 400

        title = get_video_title(link)

        transcript_data = ''
        try:
            transcript_data = YouTubeTranscriptApi.fetch(video_id)
        except Exception as e:
            print(f"Error fetching transcript: {e}")
        transcript = " ".join([item['text'] for item in transcript_data])

        prompt = (
            "The following is a transcript from a YouTube video. "
            "Tell me what the video is about: " + transcript
        )
        if specifics:
            prompt += f" Please focus on the following aspects: {specifics}"

        response = model.generate_content(prompt)

        if not hasattr(response, 'text') or not response.text:
            return jsonify({"message": "Failed to generate content"}), 500

        return jsonify({
            "title": title,
            "summary": response.text
        })

    except Exception as e:
        return jsonify({"message": transcript_data + str(e)}), 500


if __name__ == '__main__':
    app.run(debug=True, port=port)
