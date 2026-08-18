from ultralytics import YOLO

def validate_model():
    print("--- Starting model validation ---")
    
    model_path = 'brain_tumor_detector/yolov8n_run_1/weights/best.pt'
    
    data_yaml_path = 'brain_tumor_dataset.yaml'

    try:
        print(f"Loading model from: {model_path}")
        model = YOLO(model_path)

        print(f"Running validation using dataset config: {data_yaml_path}")
        metrics = model.val(
            data=data_yaml_path,
            split='val',
            project='brain_tumor_detector',
            name='validation_run'
        )
        
        print("--- Validation Complete ---")
        print(f"Results saved to 'brain_tumor_detector/validation_run'")
        
        map50_95 = metrics.maps[0] 
        map50 = metrics.maps[1] 

        print(f"\n--- Key Metrics ---")
        print(f"Mean Average Precision (mAP) 50-95: {map50_95*100:.2f}%")
        print(f"Mean Average Precision (mAP) 50:    {map50*100:.2f}%")

    except Exception as e:
        print(f"An error occurred during validation: {e}")

if __name__ == '__main__':
    validate_model()