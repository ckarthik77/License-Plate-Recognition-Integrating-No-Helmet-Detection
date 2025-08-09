import cv2

# Load the original image
image_path = r"C:\Users\SHAIK SAMEER\Desktop\License-Plate-Recognition-Integrating-No-Helmet-Detection-with-YOLOv12-main\test_input1.jpeg"# Replace with your image path
image = cv2.imread(image_path)
if image is None:
    print("Error: Image not found.")
    exit()

# Resize image for consistent view
image = cv2.resize(image, (800, 500))
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

# Load OpenCV's pre-trained number plate Haar Cascade
cascade_path = cv2.data.haarcascades + 'haarcascade_russian_plate_number.xml'
plate_cascade = cv2.CascadeClassifier(cascade_path)

# Detect number plates
plates = plate_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(50, 20))

# Draw bounding boxes
if len(plates) == 0:
    print("⚠️ No number plate detected.")
else:
    for (x, y, w, h) in plates:
        cv2.rectangle(image, (x, y), (x + w, y + h), (0, 255, 0), 3)
        plate_roi = image[y:y + h, x:x + w]
        cv2.imshow("Detected Number Plate", plate_roi)

# Show final result
cv2.imshow("Detected Plates", image)
cv2.waitKey(0)
cv2.destroyAllWindows()