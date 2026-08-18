from ultralytics import YOLO
import os

def run_prediction():
    print("--- Starting prediction script ---")
    
    model_path = 'brain_tumor_detector/yolov8n_run_1/weights/best.pt'

    test_image_path = r'C:\Users\USER\Desktop\Brain Tumor\brain_tumor_project\brain_tumor_dataset\Train\images\gg (105).jpg'

    # Check if model file exists
    print(f"Checking for model at: {model_path}")
    if not os.path.exists(model_path):
        print(f"--- SCRIPT STOPPED ---")
        print(f"Error: Model file not found at '{model_path}'")
        print("Please check your 'brain_tumor_detector' folder to ensure the 'yolov8n_run_1' folder and 'best.pt' file exist.")
        return
    print("Model file found.")

    # Check if test image exists
    print(f"Checking for test image at: {test_image_path}")
    if not os.path.exists(test_image_path):
        print(f"Error: Test image not found at '{test_image_path}'")
        print("Please make sure you have copied an image to this exact location and named it 'my_test_image.jpg'.")
        return
    print("Test image file found.")

    # Load the model
    try:
        print("Loading custom-trained model...")
        model = YOLO(model_path)
        print("Model loaded successfully.")
    except Exception as e:
        print(f"Error loading model: {e}")
        return

    # Run prediction
    print(f"Detecting tumors in '{test_image_path}'...")
    results = model.predict(
        source=test_image_path,
        save=True,
        conf=0.5
    )
    print("Prediction complete.")

    # Process results
    if not results:
        print("Prediction ran, but the 'results' object is empty.")
        return

    if len(results) > 0:
        result = results[0]
        print(f"Result image saved in: '{result.save_dir}'")

        if len(result.boxes) == 0:
            print("Detection summary: No tumors detected with confidence > 50%.")
        else:
            print("Detection summary:")
            for box in result.boxes:
                class_id = int(box.cls[0])
                class_name = model.names[class_id]
                confidence = float(box.conf[0])
                print(f"- Detected: {class_name} with {confidence*100:.2f}% confidence.")
    else:
        print("Prediction ran, but the 'results' list is empty.")
    
    print("Prediction finished")

if __name__ == '__main__':
    run_prediction()