import cv2
from paddleocr import PaddleOCR
import os
import logging

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

ocr = PaddleOCR(use_textline_orientation=True)

def extract_text(image_path: str):
    if not os.path.exists(image_path):
        logging.error(f"Image not found: {image_path}")
        return

    img = cv2.imread(image_path)
    if img is None:
        logging.error("Failed to load image (cv2 returned None).")
        return

    logging.info(f"Running OCR on: {image_path}")
    result = ocr.predict(img)

    if not result or result[0] is None:
        print("❌  No text detected.")
        return

    print("\n✅  Detected Text:")
    for box, (text, conf) in result[0]:
        print(f" - {text}  (confidence: {conf:.2f})")

if __name__ == "__main__":
    image_path = r"C:\Users\SHAIK SAMEER\Desktop\License-Plate-Recognition-Integrating-No-Helmet-Detection-with-YOLOv12-main\test_input1.jpeg"
    extract_text(image_path)
