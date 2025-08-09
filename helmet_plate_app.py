import cv2
import supervision as sv
from ultralytics import YOLO
from paddleocr import PaddleOCR
import typer
import numpy as np
import logging

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Initialize PaddleOCR
ocr = PaddleOCR(use_angle_cls=True, lang='en')  # No need for 'rec=True' later

# Load both YOLO models
plate_model = YOLO("lprbest.pt")     # For number plate detection
helmet_model = YOLO("best.pt")       # For helmet detection

app = typer.Typer()

# OCR Helper Function
def perform_ocr(image_array):
    if image_array is None or image_array.size == 0:
        logging.warning("Empty image provided for OCR")
        return ""

    try:
        results = ocr.ocr(image_array)
        detected_text = []
        if results and results[0] is not None:
            for result in results[0]:
                text = result[1][0]
                detected_text.append(text)
        return ''.join(detected_text)
    except Exception as e:
        logging.error(f"OCR error: {e}")
        return ""

# Live Webcam Processing
def process_webcam(output_file="output_live.avi"):
    cap = cv2.VideoCapture(0)  # Default webcam

    if not cap.isOpened():
        logging.error("Could not open webcam.")
        return

    # Set resolution
    target_width = 1280
    target_height = 720
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, target_width)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, target_height)

    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fps = cap.get(cv2.CAP_PROP_FPS) or 30.0
    logging.info(f"Webcam resolution: {width}x{height}, FPS: {fps}")

    # Save output
    fourcc = cv2.VideoWriter_fourcc(*'XVID')
    out = cv2.VideoWriter(output_file, fourcc, fps, (width, height))

    if not out.isOpened():
        logging.error("Could not initialize VideoWriter.")
        cap.release()
        return

    # Annotators
    helmet_box_annotator = sv.BoundingBoxAnnotator()
    helmet_label_annotator = sv.LabelAnnotator()

    frame_count = 0
    while True:
        ret, frame = cap.read()
        if not ret:
            logging.warning("Failed to read frame.")
            break

        frame_count += 1
        logging.info(f"Processing frame {frame_count}...")

        annotated_frame = frame.copy()

        # -------- License Plate Detection + OCR ----------
        plate_results = plate_model(frame)[0]
        plate_detections = sv.Detections.from_ultralytics(plate_results)

        for xyxy, _, class_id in zip(plate_detections.xyxy, plate_detections.confidence, plate_detections.class_id):
            x1, y1, x2, y2 = map(int, xyxy)
            crop = frame[y1:y2, x1:x2]
            if crop.size == 0:
                continue
            crop = cv2.resize(crop, (110, 70))
            text = perform_ocr(crop)
            if text:
                text = text.replace('(', '').replace(')', '').replace(',', '').replace(']', '').replace('-', ' ')
                cv2.rectangle(annotated_frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
                cv2.putText(annotated_frame, text, (x1, y1 - 10),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2)

        # -------- Helmet Detection ----------
        helmet_results = helmet_model(frame)[0]
        helmet_detections = sv.Detections.from_ultralytics(helmet_results)

        annotated_frame = helmet_box_annotator.annotate(scene=annotated_frame, detections=helmet_detections)
        annotated_frame = helmet_label_annotator.annotate(scene=annotated_frame, detections=helmet_detections)

        # Display & Save
        out.write(annotated_frame)
        cv2.imshow("Helmet & Number Plate Detection", annotated_frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    out.release()
    cv2.destroyAllWindows()
    logging.info(f"Finished. Output saved to {output_file}")

# Typer CLI command
@app.command()
def webcam(output_file: str = "output_live.avi"):
    typer.echo("Starting live webcam detection...")
    process_webcam(output_file)

if __name__ == "__main__":
    app()
