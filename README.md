# Intelligent Traffic Violation Detection — Helmetless Riding + License Plate Recognition

An AI-powered traffic monitoring system that detects helmetless riders, recognizes vehicle number plates, and generates actionable evidence in real-time. Built with YOLOv5 for detection and EasyOCR/Tesseract for recognition, it’s designed for scalability, smart city integration, and high accuracy.

[![Watch the video](https://github.com/YOUR-USERNAME/Intelligent-Traffic-Violation-Detection/blob/main/demo.png)](https://youtu.be/YOUR-DEMO-LINK)

---

## 🚦 Overview

This system automates traffic violation detection by:

* Identifying two-wheeler riders without helmets
* Detecting & reading license plates
* Processing both images & video streams in real-time
* Generating visual + textual proof for enforcement

---

## ✨ Key Features

* **🎯 Real-time Detection** — Helmetless riding, triple riding, and license plates
* **📊 High Accuracy** — \~93% detection, \~88% OCR on clear frames
* **🖥️ Interactive Interface** — Easy-to-use Gradio web dashboard
* **⚡ Scalable** — Works with single or multi-camera feeds
* **🛠️ Extensible** — Modular pipeline to add new violations (red-light jumping, over-speeding, etc.)

---

## 🧠 Tech Stack

* **Model:** YOLOv5 (Object Detection)
* **OCR:** EasyOCR / Tesseract
* **Frameworks & Tools:** PyTorch, OpenCV, NumPy, Matplotlib, Gradio
* **Language:** Python

---

## 📂 Project Structure

```
├── yolov5/                  # Model & inference code
│   ├── app.py               # Web dashboard
│   ├── inference.py         # Detection + OCR pipeline
│   └── requirements.txt
├── models/                  # Trained weights
├── data/                    # Sample images/videos
└── README.md
```

---

## 🚀 Installation

```bash
# Clone repository
git clone https://github.com/YOUR-USERNAME/Intelligent-Traffic-Violation-Detection.git
cd Intelligent-Traffic-Violation-Detection

# Create environment
conda create -n traffic-violation python=3.11
conda activate traffic-violation

# Install dependencies
pip install -r yolov5/requirements.txt
```

---

## ▶️ Usage

```bash
# Launch web interface
python yolov5/app.py

# Access:
# Local: http://127.0.0.1:7860
# Public link: Provided in console
```

---

## 📊 Performance

| Task                    | Accuracy | Notes                        |
| ----------------------- | -------- | ---------------------------- |
| Helmet Detection        | \~93%    | Best in daylight             |
| License Plate Detection | \~91%    | Works in varied angles       |
| OCR (EasyOCR)           | \~88%    | Slight drop in poor lighting |

---

## 🔮 Future Work

* Edge deployment on Jetson Nano / Raspberry Pi
* Database integration for automated challan generation
* Multi-language license plate OCR
* Multi-camera analysis for intersections

---

## 🤝 Contributing

Contributions are welcome!
Submit issues, pull requests, or suggestions to improve detection accuracy, speed, or usability.

---

## 📜 License

MIT License — see `LICENSE` file.

---

## 🙏 Acknowledgments

* [Ultralytics YOLOv5](https://github.com/ultralytics/yolov5)
* [EasyOCR](https://github.com/JaidedAI/EasyOCR)
* [Tesseract OCR](https://github.com/tesseract-ocr/tesseract)
* [OpenCV](https://opencv.org/)
* Kaggle datasets for helmet & license plate detection
