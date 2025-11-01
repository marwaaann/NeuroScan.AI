from ultralytics import YOLO

def train_model():
    # 1. Load a pre-trained YOLOv8 model
    # 'yolov8n.pt' is the nano version, fast and small.
    # You can also use 'yolov8s.pt' (small) for better accuracy.
    model = YOLO('yolov8n.pt')

    # 2. Train the model
    # 'data' points to our YAML file.
    # 'epochs' is the number of times to go through the dataset.
    # 'imgsz' is the image size to train on.
    print("Starting model training...")
    try:
        results = model.train(
            data='brain_tumor_dataset.yaml',
            epochs=100,
            imgsz=640,
            project='brain_tumor_detector', # Project folder name
            name='yolov8n_run_1'         # Experiment name
        )
        
        print("Training complete!")
        print(f"Model results saved to: {results.save_dir}")
        print("Your trained model is at: {results.save_dir}/weights/best.pt")

    except Exception as e:
        print(f"An error occurred during training: {e}")
        print("Please ensure 'brain_tumor_dataset.yaml' is in the same directory.")
        print("Also, check that the 'path' inside the YAML file is correct.")

if __name__ == '__main__':
    # Make sure your 'brain_tumor_dataset.yaml' is in the same folder
    # and you have updated the 'path' inside it.
    train_model()