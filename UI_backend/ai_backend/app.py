from flask import Flask, request, jsonify
from ultralytics import YOLO
from PIL import Image
import os
import json

app = Flask(__name__)
OUTPUT_FOLDER = 'output'
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

# Load YOLO model
model = YOLO("yolov3.pt")

@app.route('/detect', methods=['POST'])
def detect_objects():
    if 'image' not in request.files:
        return jsonify({"error": "No image file provided"}), 400
    
    image = request.files['image']
    img = Image.open(image)

    # Perform object detection
    results = model(img, device='cpu')

    output_image_path = os.path.join(OUTPUT_FOLDER, image.filename)
    results[0].plot(save_dir=OUTPUT_FOLDER)
    
    # Create a JSON response
    detections = []
    for obj in results[0].boxes:
        detections.append({
            "class": obj.cls.item(),
            "confidence": obj.conf.item(),
            "box": obj.xyxy.tolist()
        })
    
    output_json_path = os.path.join(OUTPUT_FOLDER, "results.json")
    with open(output_json_path, 'w') as f:
        json.dump(detections, f)

    return jsonify(detections)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5001)
