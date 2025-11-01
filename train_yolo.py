from ultralytics import YOLO

def train_model():
    print("Loading pre-trained YOLOv8n model...")
    # Load a pre-trained model (e.g., 'yolov8n.pt' for nano)
    # This downloads the model if not already present
    model = YOLO('yolov8n.pt')

    print("Starting model training...")
    try:
        # Train the model
        results = model.train(
            data='brain_tumor_dataset.yaml',  # Path to your dataset YAML file
            
            # UPDATED: Reduced epochs from 100 to 20 for faster CPU training
            epochs=20,                         
            
            imgsz=640,                         # Image size (pixels)
            batch=8,                           # Reduced batch size for CPU to prevent memory issues
            project='brain_tumor_detector',    # Directory to save results
            name='yolov8n_run_1',              # Experiment name
            exist_ok=True                      # Overwrite existing experiment
        )
        print("Training complete. Results saved in 'brain_tumor_detector/yolov8n_run_1'")
    
    except Exception as e:
        print(f"An error occurred during training: {e}")
        print("Please check the following:")
        print("1. Your 'brain_tumor_dataset.yaml' file is in the same directory.")
        print("2. The 'path' in your YAML file is the correct *absolute* path to 'brain_tumor_dataset'.")
        print("3. Your dataset folder structure is correct (Train/images, Train/labels, etc.).")


if __name__ == '__main__':
    train_model()

