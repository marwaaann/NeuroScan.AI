from ultralytics import YOLO

def validate_model():
    print("--- Starting model validation ---")
    
    # --- Path to your trained model ---
    model_path = 'brain_tumor_detector/yolov8n_run_1/weights/best.pt'
    
    # --- Path to your dataset config file ---
    data_yaml_path = 'brain_tumor_dataset.yaml'

    try:
        # Load your custom-trained model
        print(f"Loading model from: {model_path}")
        model = YOLO(model_path)

        # Run validation
        print(f"Running validation using dataset config: {data_yaml_path}")
        metrics = model.val(
            data=data_yaml_path,
            split='val',  # Specify you want to run on the 'val' set
            project='brain_tumor_detector',
            name='validation_run' # Save results to a new folder
        )
        
        print("--- Validation Complete ---")
        print(f"Results saved to 'brain_tumor_detector/validation_run'")
        
        # metrics.maps is a list, get the mAP50-95 (index 0)
        map50_95 = metrics.maps[0] 
        # metrics.maps is a list, get the mAP50 (index 1)
        map50 = metrics.maps[1] 

        print(f"\n--- Key Metrics ---")
        print(f"Mean Average Precision (mAP) 50-95: {map50_95*100:.2f}%")
        print(f"Mean Average Precision (mAP) 50:    {map50*100:.2f}%")
        
        print("\n* mAP50-95: This is your main accuracy score. It's the average precision calculated at 10 different overlap thresholds (from 50% to 95%). A higher score is better.")
        print("* mAP50: This score only counts a detection as 'correct' if the bounding box overlaps the true box by at least 50%. This score will be higher.")

    except Exception as e:
        print(f"An error occurred during validation: {e}")

if __name__ == '__main__':
    validate_model()