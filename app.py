import os
import requests
from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

# Your API Credentials
API_KEY = 'eef2cd17633d424f85e7f1a5f765d6b7eb2647032c6dfef9e056e5c2d835cefbe0b46c85d10943305abfccc7da3b104e'
TEMPLATE_ID = 'd0216794-be78-4770-909f-5ea58ab1fbad'

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/create-video', methods=['POST'])
def create_video():
    user_video_url = request.json.get('video_url', '').strip()
    if not user_video_url:
        return jsonify({'error': 'No URL provided'}), 400
    
    headers = {
        'Authorization': f'Bearer {API_KEY}',
        'Content-Type': 'application/json'
    }
    
    payload = {
        'template_id': TEMPLATE_ID,
        'modifications': {
            "Video": user_video_url,
            "Video-1": user_video_url,
            "video-1": user_video_url,
            "Media": user_video_url,
            "Source": user_video_url,
            "Background": user_video_url
        }
    }
    
    try:
        response = requests.post('https://api.creatomate.com/v1/renders', headers=headers, json=payload, timeout=30)
        data = response.json()
        return jsonify({'render_id': data[0]['id']})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/status/<render_id>')
def get_status(render_id):
    headers = {'Authorization': f'Bearer {API_KEY}'}
    try:
        response = requests.get(f'https://api.creatomate.com/v1/renders/{render_id}', headers=headers, timeout=20)
        return jsonify(response.json())
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)