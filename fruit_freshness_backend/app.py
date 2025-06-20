from flask import Flask, request, jsonify
import tensorflow as tf
import numpy as np
from PIL import Image
import io
from flask_cors import CORS
import os
from ocr import process_image, preprocess_image  # Directly import functions
from datetime import datetime

# Initialize the Flask app
app = Flask(__name__)
CORS(app)

# Load the trained fruit classifier model
model = tf.keras.models.load_model(os.path.join(os.path.dirname(__file__), "improved_fruit_classifier.h5"))

# Predict freshness
def predict_image(image_bytes):
    try:
        image = Image.open(io.BytesIO(image_bytes)).convert('RGB')
        image = image.resize((224, 224))
        img_array = np.array(image) / 255.0
        img_array = np.expand_dims(img_array, axis=0)
        prediction = model.predict(img_array)[0][0]
        label = "Rotten" if prediction > 0.5 else "Fresh"
        confidence = prediction if prediction > 0.5 else 1 - prediction
        return label, float(confidence)
    except Exception as e:
        print(f"Prediction error: {e}")
        return None, None

# Fruit freshness prediction endpoint
@app.route('/predict', methods=['POST'])
def predict():
    if 'file' not in request.files:
        return jsonify({'error': 'No image uploaded'}), 400
    file = request.files['file']
    label, confidence = predict_image(file.read())
    if label is None:
        return jsonify({'error': 'Prediction failed'}), 500
    return jsonify({'label': label, 'confidence': confidence})

# OCR endpoint for extracting expiry date
@app.route('/ocr', methods=['POST'])
def ocr_endpoint():
    file = request.files.get('file')
    if not file:
        return jsonify({"error": "No file uploaded"}), 400

    image_path = "uploaded.jpg"
    file.save(image_path)

    expiry_date = process_image(image_path)

    if not expiry_date:
        print("[INFO] Retrying with preprocessed image...")
        preprocessed_path = preprocess_image(image_path)
        expiry_date = process_image(preprocessed_path)

    if isinstance(expiry_date, datetime):
        return jsonify({"expiry_date": expiry_date.strftime('%Y-%m-%d')}), 200
    else:
        return jsonify({"expiry_date": None, "message": "No valid expiry date found"}), 200



if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=False, threaded=True)
