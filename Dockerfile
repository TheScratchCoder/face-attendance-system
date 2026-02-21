# ─── Base Image ────────────────────────────────────────────────────────────
FROM python:3.10-slim

# ─── System Dependencies ────────────────────────────────────────────────────
RUN apt-get update && apt-get install -y \
    build-essential \
    cmake \
    libopenblas-dev \
    liblapack-dev \
    libx11-dev \
    libgtk-3-dev \
    libboost-python-dev \
    libboost-thread-dev \
    ffmpeg \
    libsm6 \
    libxext6 \
    && rm -rf /var/lib/apt/lists/*

# ─── Working Directory ───────────────────────────────────────────────────────
WORKDIR /app

# ─── Install Python Deps ─────────────────────────────────────────────────────
COPY requirements.txt .
RUN pip install --upgrade pip
RUN pip install dlib==19.24.2
RUN pip install -r requirements.txt

# ─── Copy App ────────────────────────────────────────────────────────────────
COPY . .

# ─── Create required dirs ────────────────────────────────────────────────────
RUN mkdir -p known_faces encodings attendance

# ─── Expose Port ─────────────────────────────────────────────────────────────
EXPOSE 8501

# ─── Healthcheck ─────────────────────────────────────────────────────────────
HEALTHCHECK CMD curl --fail http://localhost:8501/_stcore/health || exit 1

# ─── Run App ─────────────────────────────────────────────────────────────────
ENTRYPOINT ["streamlit", "run", "app.py", \
            "--server.port=8501", \
            "--server.address=0.0.0.0", \
            "--server.headless=true"]
