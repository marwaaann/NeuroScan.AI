# Brain Tumor Detection Web Application

A web-based application for detecting brain tumors in medical images using YOLO (You Only Look Once) deep learning model.

## Features

- 🖼️ **Image Upload**: Drag and drop or browse to upload brain scan images
- 🔍 **AI Detection**: Automatic detection of brain tumors with confidence scores
- 📊 **Visual Results**: Display of detected tumors with bounding boxes
- 🎨 **Modern UI**: Beautiful and intuitive user interface
- ⚡ **Real-time Analysis**: Fast prediction using YOLO model

## Detection Classes

The model can detect the following:
- **Glioma**: A type of tumor that occurs in the brain and spinal cord
- **Meningioma**: A tumor that arises from the meninges
- **No Tumor**: Healthy brain scan
- **Pituitary**: Tumor in the pituitary gland

## Installation

1. **Install Python dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

2. **Ensure you have a trained model**:
   - The app will look for models in this order:
     1. `brain_tumor_detector/yolov8n_run_1/weights/best.pt`
     2. `brain_tumor_detector/yolov8n_run_12/weights/best.pt`
     3. `yolo11n.pt`
     4. `yolov8n.pt`
   - Place your trained model in one of these locations

## Running the Application

1. **Navigate to the project directory**:
   ```bash
   cd brain_tumor_project
   ```

2. **Start the Flask server**:
   ```bash
   python app.py
   ```

3. **Open your web browser**:
   - Navigate to: `C`
   - The web interface will be displayed

## Usage

1. **Upload an Image**:
   - Click "Choose Image" button or drag and drop an image
   - Supported formats: JPG, PNG, JPEG, etc.

2. **Analyze**:
   - Click the "🔍 Analyze Image" button
   - Wait for the analysis to complete (usually a few seconds)

3. **View Results**:
   - The annotated image with bounding boxes will be displayed
   - Detection results showing tumor type and confidence scores
   - Each detection includes a confidence percentage

## API Endpoints

### `GET /`
Returns the main web interface.

### `POST /predict`
Upload an image for tumor detection.

**Request**: 
- Method: POST
- Content-Type: multipart/form-data
- Body: `image` (file)

**Response**:
```json
{
  "detections": [
    {
      "class": "Glioma",
      "confidence": 85.5,
      "bbox": [x1, y1, x2, y2]
    }
  ],
  "message": "Found 1 detection(s)",
  "image": "data:image/png;base64,..."
}
```

### `GET /health`
Check application health and model status.

**Response**:
```json
{
  "status": "healthy",
  "model_loaded": true
}
```

## Troubleshooting

### Model Not Found
- Ensure you have a trained model file in one of the expected locations
- Check the console output when starting the app for model loading status

### Prediction Errors
- Make sure the image is a valid brain scan image
- Check that the image file size is under 16MB
- Verify that all dependencies are installed correctly

### Port Already in Use
- Change the port in `app.py`: `app.run(port=5001)`
- Or stop the process using port 5000

## Technical Details

- **Backend**: Flask (Python web framework)
- **Model**: YOLO (Ultralytics)
- **Image Processing**: PIL/Pillow
- **Frontend**: HTML5, CSS3, JavaScript

## Notes

- This is a research/educational tool and should not be used as a substitute for professional medical diagnosis
- Always consult with qualified medical professionals for actual medical decisions
- The model accuracy depends on the training data and may vary

## License

This project is for educational purposes.
