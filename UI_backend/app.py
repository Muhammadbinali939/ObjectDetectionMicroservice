from flask import Flask, request, jsonify, send_file
import requests
import os

app = Flask(__name__)
UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

AI_BACKEND_URL = "http://ai_backend:5001/detect"

@app.route('/upload', methods=['POST'])
def upload_image():
    if 'image' not in request.files:
        return jsonify({"error": "No image file provided"}), 400
    
    image = request.files['image']
    filepath = os.path.join(UPLOAD_FOLDER, image.filename)
    image.save(filepath)

    # Send the image to the AI backend
    with open(filepath, 'rb') as img:
        response = requests.post(AI_BACKEND_URL, files={'image': img})
    
    if response.status_code == 200:
        result = response.json()
        return jsonify(result)
    else:
        return jsonify({"error": "Detection failed"}), 500

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
