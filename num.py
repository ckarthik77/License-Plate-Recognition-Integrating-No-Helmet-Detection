import cv2
import pytesseract
from ultralytics import YOLO
import re
import os
import tempfile

# ✅ Set up Tesseract executable path
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

# ✅ Optional: Use safe temporary directory to avoid permission issues
custom_temp_dir = os.path.join(os.getcwd(), "tess_tmp")
os.makedirs(custom_temp_dir, exist_ok=True)
pytesseract.pytesseract.TEMP_DIR = custom_temp_dir

# ✅ Load YOLO model
model = YOLO("lprbest.pt")  # ⛳ Replace with actual model path

# ✅ Load test image
image_path = r"C:\Users\SHAIK SAMEER\Desktop\License-Plate-Recognition-Integrating-No-Helmet-Detection-with-YOLOv12-main\dumb.jpg"
image = cv2.imread(image_path)
if image is None:
    print("❌ Could not load image.")
    exit()

# ✅ Run detection
results = model(image)[0]

# ✅ Process each detected plate
for box in results.boxes:
    x1, y1, x2, y2 = map(int, box.xyxy[0])
    cropped = image[y1:y2, x1:x2]

    # 🔍 Preprocess for OCR
    gray = cv2.cvtColor(cropped, cv2.COLOR_BGR2GRAY)
    blur = cv2.bilateralFilter(gray, 11, 17, 17)
    thresh = cv2.adaptiveThreshold(
        blur, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 31, 3
    )

    # 💾 Debug image save (optional)
    cv2.imwrite("debug_thresh.jpg", thresh)

    # 🧾 OCR Config
    config = r'--oem 3 --psm 6 -c tessedit_char_whitelist=ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789'

    # 🧠 Run Tesseract safely
    try:
        raw_text = pytesseract.image_to_string(thresh, config=config)
        print(f"[DEBUG] RAW OCR OUTPUT:\n{repr(raw_text)}")
    except Exception as e:
        print("❌ OCR failed:", e)
        exit()

    # 🧹 Clean and merge lines
    lines = raw_text.splitlines()
    merged_text = ''.join(lines).replace(" ", "").upper()
    print(f"[DEBUG] CLEANED OCR TEXT: {merged_text}")

    # 🎯 Match Indian plate format: e.g., AP40AA6623
    match = re.search(r'[A-Z]{2}\d{2}[A-Z]{1,2}\d{4}', merged_text)
    if match:
        plate_text = match.group(0)
        print(f"✅ Valid Plate Detected: {plate_text}")
    else:
        plate_text = "UNREADABLE"
        print("⚠️ No valid plate pattern detected.")

    # 🖼️ Annotate original image
    cv2.rectangle(image, (x1, y1), (x2, y2), (0, 255, 0), 2)
    cv2.putText(image, plate_text, (x1, y1 - 10),
                cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2)
    break  # Only process the first detection

# 💾 Save result
os.makedirs("output", exist_ok=True)
output_path = os.path.join("output", "annotated_plate_output.jpg")
cv2.imwrite(output_path, image)
print(f"💾 Annotated image saved at: {output_path}")
