import cv2
import os
import logging
from ultralytics import YOLO
from supervision import Detections, BoxAnnotator, LabelAnnotator

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Load YOLO models
helmet_model = YOLO("best.pt")       # Helmet detection model
plate_model = YOLO("lprbest.pt")     # License plate detection model

# Annotators
box_annotator = BoxAnnotator()
label_annotator = LabelAnnotator()

def detect_objects(image_path):
    if not os.path.exists(image_path):
        logging.error(f"Image not found: {image_path}")
        return

    image = cv2.imread(image_path)
    if image is None:
        logging.error("Failed to load image.")
        return

    annotated_image = image.copy()

    # -------------------------
    # 1. License Plate Detection
    # -------------------------
    plate_result = plate_model(image)[0]
    plate_detections = Detections.from_ultralytics(plate_result)
    logging.info(f"🟩 Found {len(plate_detections)} license plates.")

    plate_class_names = plate_result.names
    plate_labels = [plate_class_names[class_id] for class_id in plate_detections.class_id]

    annotated_image = box_annotator.annotate(annotated_image, plate_detections)
    annotated_image = label_annotator.annotate(annotated_image, plate_detections, labels=plate_labels)

    # -------------------------
    # 2. Helmet Detection
    # -------------------------
    helmet_result = helmet_model(image)[0]
    helmet_detections = Detections.from_ultralytics(helmet_result)
    logging.info(f"🟨 Found {len(helmet_detections)} helmet-related detections.")

    helmet_class_names = helmet_result.names
    helmet_labels = [helmet_class_names[class_id] for class_id in helmet_detections.class_id]

    annotated_image = box_annotator.annotate(annotated_image, helmet_detections)
    annotated_image = label_annotator.annotate(annotated_image, helmet_detections, labels=helmet_labels)

    # -------------------------
    # Save Final Annotated Image
    # -------------------------
    output_dir = "annotated_output"
    os.makedirs(output_dir, exist_ok=True)
    output_path = os.path.join(output_dir, "final_output.jpg")
    cv2.imwrite(output_path, annotated_image)
    logging.info(f"✅ Saved annotated image at: {output_path}")

if __name__ == "__main__":
    image_path = r"C:\Users\SHAIK SAMEER\Desktop\License-Plate-Recognition-Integrating-No-Helmet-Detection-with-YOLOv12-main\test_input.jpg"
    detect_objects(image_path)
