# Face Attendance System

A real-time AI-powered attendance management system built with Python, Face Recognition, OpenCV, SQLite, and Streamlit.

---

## Live Demo
https://thescratchcoder-face-attendance-system.streamlit.app

---

## Features

- Real-time face detection and recognition via webcam
- Register users with photo upload or webcam capture
- Auto-mark attendance with duplicate prevention
- SQLite database with full attendance history
- Filter attendance by date and export to CSV
- Manage registered users (view and delete)
- Confidence score displayed during recognition

---

## How It Works

### Registration Flow
1. Upload or capture a photo
2. System detects the face using dlib HOG algorithm
3. Deep neural network converts face into 128-dimensional vector (face encoding)
4. Encoding and user details saved to database

### Attendance Flow
1. Webcam captures live video frames
2. Each frame is scanned for faces
3. Detected face encoding is compared to stored encodings using Euclidean distance
4. If distance is below 0.5 threshold, face is recognized
5. Attendance is marked in SQLite database with name, roll no, date and time

---

## Tech Stack

| Layer | Technology |
|-------|-----------|
| UI | Streamlit |
| Face Detection | dlib HOG algorithm |
| Face Recognition | dlib ResNet (128D face embeddings) |
| Computer Vision | OpenCV |
| Database | SQLite |
| Data Processing | Pandas, NumPy |

---

## Project Structure

```
face-attendance-system/
│
├── app.py                   # Main Streamlit application
├── utils/
│   ├── database.py          # SQLite CRUD operations
│   └── encode.py            # Face encoding logic
│
├── known_faces/             # Registered face images
├── encodings/               # Saved face encodings
├── attendance/              # CSV exports
├── requirements.txt
├── Dockerfile
└── README.md
```

---

## Setup and Run Locally

### Prerequisites
- Python 3.10
- Anaconda or Miniconda

### Steps

```bash
# Create conda environment
conda create -n attendance python=3.10 -y
conda activate attendance

# Install dlib
conda install -c conda-forge dlib=19.24.2 -y

# Install other dependencies
pip install face-recognition streamlit opencv-python-headless numpy==1.26.4 Pillow pandas

# Run the app
streamlit run app.py
```

Open http://localhost:8501 in Chrome.

---

## Usage

### Register a User
1. Go to Register User in the sidebar
2. Enter Name and Roll No
3. Upload a clear front-facing photo
4. Click Register User

### Take Attendance
1. Go to Take Attendance
2. Start the camera
3. System automatically recognizes and marks attendance

### View Reports
1. Go to View Reports
2. Filter by date or view all records
3. Download as CSV

---

## Author

Ankit | GitHub: [@TheScratchCoder](https://github.com/TheScratchCoder)