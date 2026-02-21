# 🎯 Face Attendance System

A real-time AI-powered attendance management system using **Face Recognition**, **OpenCV**, **SQLite**, and **Streamlit**.

---

## 📸 Features

- ✅ Real-time face detection and recognition via webcam
- ✅ Register users with photo upload or webcam capture
- ✅ Auto-mark attendance (once per session, no duplicates)
- ✅ SQLite database with full attendance history
- ✅ Filter attendance by date and export to CSV
- ✅ Manage registered users (view/delete)
- ✅ Confidence score displayed during recognition
- ✅ Dockerized for easy deployment

---

## 🏗️ Project Structure

```
face-attendance-system/
│
├── app.py                   # Main Streamlit application
├── utils/
│   ├── __init__.py
│   ├── database.py          # SQLite CRUD operations
│   └── encode.py            # Face encoding logic
│
├── known_faces/             # Registered face images (auto-created)
├── encodings/               # Saved face encodings .pkl (auto-created)
├── attendance/              # CSV exports (auto-created)
├── attendance.db            # SQLite database (auto-created)
│
├── requirements.txt
├── Dockerfile
├── docker-compose.yml
├── .streamlit/
│   └── config.toml
└── README.md
```

---

## ⚙️ How It Works (Workflow)

```
┌─────────────────────────────────────────────────────────────┐
│                    REGISTRATION FLOW                        │
│                                                             │
│  Upload Photo → Detect Face → Generate 128D Encoding →     │
│  Save to known_faces/ → Update encodings.pkl → Save to DB  │
└─────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────┐
│                   RECOGNITION FLOW                          │
│                                                             │
│  Webcam Frame → Resize (0.25x for speed) → Detect Faces →  │
│  Generate Encodings → Compare with known_encodings →        │
│  Euclidean Distance < 0.5? → Match Found →                 │
│  Mark Attendance in SQLite → Display on UI                  │
└─────────────────────────────────────────────────────────────┘
```

### AI/ML Details
| Component | Technology |
|-----------|-----------|
| Face Detection | dlib HOG-based detector |
| Face Encoding | dlib ResNet (128D face embedding) |
| Similarity | Euclidean distance (threshold: 0.5) |
| Camera Input | OpenCV VideoCapture |

---

## 🚀 Setup & Run Locally

### Prerequisites
- Python 3.9 or 3.10
- Webcam
- CMake installed (for dlib)

### Step 1: Clone the repo
```bash
git clone https://github.com/yourusername/face-attendance-system.git
cd face-attendance-system
```

### Step 2: Create virtual environment
```bash
python -m venv venv

# Windows
venv\Scripts\activate

# Mac/Linux
source venv/bin/activate
```

### Step 3: Install dependencies

**On Linux/Mac:**
```bash
pip install -r requirements.txt
```

**On Windows (dlib can be tricky):**
```bash
pip install cmake
pip install dlib
pip install -r requirements.txt
```

> 💡 If dlib fails on Windows, download a pre-built wheel from:
> https://github.com/z-mahmud22/Dlib_Windows_Python3.x

### Step 4: Run the app
```bash
streamlit run app.py
```

Open http://localhost:8501 in your browser.

---

## 🐳 Run with Docker

### Option 1: Docker Compose (Recommended)
```bash
docker-compose up --build
```

### Option 2: Manual Docker
```bash
# Build
docker build -t face-attendance .

# Run
docker run -p 8501:8501 \
  -v $(pwd)/known_faces:/app/known_faces \
  -v $(pwd)/encodings:/app/encodings \
  -v $(pwd)/attendance.db:/app/attendance.db \
  face-attendance
```

Open http://localhost:8501

---

## ☁️ Deployment Options

### Option 1: Streamlit Community Cloud (Free) ⭐ Recommended for Resume

1. Push code to GitHub
2. Go to https://share.streamlit.io
3. Connect your GitHub repo
4. Set main file: `app.py`
5. Deploy!

> ⚠️ Note: Streamlit Cloud doesn't support webcam in some browsers.
> Use the photo upload option for demo purposes.

### Option 2: Hugging Face Spaces (Free)

1. Create account at https://huggingface.co
2. New Space → Streamlit SDK
3. Upload all files
4. Add `requirements.txt`
5. Done!

### Option 3: AWS EC2

```bash
# SSH into EC2 instance
ssh -i key.pem ubuntu@your-ec2-ip

# Install Docker
sudo apt update
sudo apt install docker.io docker-compose -y

# Clone and run
git clone https://github.com/yourusername/face-attendance-system.git
cd face-attendance-system
sudo docker-compose up -d

# Open port 8501 in EC2 Security Group
```

### Option 4: Render.com (Free tier)

1. Connect GitHub repo on https://render.com
2. New Web Service
3. Build command: `pip install -r requirements.txt`
4. Start command: `streamlit run app.py --server.port $PORT --server.address 0.0.0.0`
5. Deploy

---

## 📱 Usage Guide

### Registering a User
1. Go to ➕ **Register User**
2. Enter Name and Roll No / Employee ID
3. Upload a clear front-facing photo (or use webcam)
4. Click **Register User**

### Taking Attendance
1. Go to 📸 **Take Attendance**
2. Check **Start Camera**
3. Stand in front of webcam
4. System auto-marks attendance when face is recognized

### Viewing Reports
1. Go to 📊 **View Reports**
2. Filter by date or view all
3. Download as CSV

---

## 🛠️ Tech Stack

| Layer | Technology |
|-------|-----------|
| UI | Streamlit |
| Face AI | face_recognition + dlib |
| Computer Vision | OpenCV |
| Database | SQLite |
| Data | Pandas, NumPy |
| Deployment | Docker, Streamlit Cloud |

---

## 🎯 Resume Highlights

- Built a real-time face recognition attendance system using **dlib's 128D face embedding model**
- Implemented **Euclidean distance-based face matching** with configurable confidence thresholds
- Designed a full-stack solution with **Streamlit UI**, **SQLite database**, and **REST-ready architecture**
- Containerized application using **Docker** for reproducible deployment
- Deployed on **[Streamlit Cloud / Hugging Face Spaces]** — live demo: [your-link]

---

## 📄 License

MIT License - feel free to use for your portfolio!
