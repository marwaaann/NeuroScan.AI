from flask import Flask, render_template, request, jsonify, send_from_directory
from ultralytics import YOLO
import os
import base64
from PIL import Image
import io
import json

app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['RESULTS_FOLDER'] = 'results'

# Create necessary directories
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
os.makedirs(app.config['RESULTS_FOLDER'], exist_ok=True)

# Load model on startup
model = None
model_paths = [
    'brain_tumor_detector/yolov8n_run_1/weights/best.pt',
    'brain_tumor_detector/yolov8n_run_12/weights/best.pt',
    'yolo11n.pt',
    'yolov8n.pt'
]

def load_model():
    """Load the YOLO model from available paths"""
    global model
    for path in model_paths:
        if os.path.exists(path):
            try:
                print(f"Loading model from: {path}")
                model = YOLO(path)
                print("Model loaded successfully!")
                return True
            except Exception as e:
                print(f"Error loading model from {path}: {e}")
                continue
    return False

# Load model when app starts
if not load_model():
    print("WARNING: No model file found. Please ensure a model file exists.")

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    if model is None:
        return jsonify({'error': 'Model not loaded. Please ensure a model file exists.'}), 500
    
    if 'image' not in request.files:
        return jsonify({'error': 'No image file provided'}), 400
    
    file = request.files['image']
    if file.filename == '':
        return jsonify({'error': 'No image selected'}), 400
    
    try:
        # Read image
        image_bytes = file.read()
        image = Image.open(io.BytesIO(image_bytes))
        
        # Convert to RGB if necessary
        if image.mode != 'RGB':
            image = image.convert('RGB')
        
        # Save uploaded image temporarily
        upload_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
        image.save(upload_path)
        
        # Run prediction
        results = model.predict(
            source=upload_path,
            conf=0.25,  # Lower confidence threshold for better detection
            save=False,
            verbose=False
        )
        
        # Process results
        if not results or len(results) == 0:
            return jsonify({
                'detections': [],
                'message': 'No tumors detected',
                'image': None
            })
        
        result = results[0]
        detections = []
        
        # Extract detection information
        if len(result.boxes) > 0:
            for box in result.boxes:
                class_id = int(box.cls[0])
                class_name = model.names[class_id]
                confidence = float(box.conf[0])
                bbox = box.xyxy[0].tolist()  # [x1, y1, x2, y2]
                
                detections.append({
                    'class': class_name,
                    'confidence': round(confidence * 100, 2),
                    'bbox': [round(coord, 2) for coord in bbox]
                })
        
        # Draw bounding boxes on image
        annotated_image = result.plot()
        annotated_pil = Image.fromarray(annotated_image)
        
        # Convert annotated image to base64
        img_buffer = io.BytesIO()
        annotated_pil.save(img_buffer, format='PNG')
        img_str = base64.b64encode(img_buffer.getvalue()).decode('utf-8')
        
        # Clean up uploaded file
        if os.path.exists(upload_path):
            os.remove(upload_path)
        
        return jsonify({
            'detections': detections,
            'message': f'Found {len(detections)} detection(s)' if detections else 'No tumors detected',
            'image': f'data:image/png;base64,{img_str}'
        })
        
    except Exception as e:
        return jsonify({'error': f'Prediction error: {str(e)}'}), 500

@app.route('/health')
def health():
    return jsonify({
        'status': 'healthy',
        'model_loaded': model is not None
    })

if __name__ == '__main__':
    print("Starting Brain Tumor Detection Web App...")
    print("Open your browser and navigate to: http://localhost:5000")
    app.run(debug=True, host='0.0.0.0', port=5000)
