import streamlit as st
import cv2
import face_recognition
import pickle
import os
import numpy as np
from datetime import datetime
from PIL import Image
import io

from utils.database import init_db, mark_attendance, get_attendance, get_all_users, delete_user
from utils.encode import encode_faces

#  Page Config 
st.set_page_config(
    page_title="Face Attendance System",
    page_icon="",
    layout="wide",
    initial_sidebar_state="expanded"
)

#  CSS 
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 1rem;
    }
    .metric-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 1rem;
        border-radius: 10px;
        color: white;
        text-align: center;
    }
    .success-box {
        background-color: #d4edda;
        border: 1px solid #c3e6cb;
        padding: 0.75rem;
        border-radius: 5px;
        color: #155724;
    }
    .stButton>button {
        width: 100%;
        border-radius: 8px;
    }
</style>
""", unsafe_allow_html=True)

#  Init 
init_db()
os.makedirs("known_faces", exist_ok=True)
os.makedirs("encodings", exist_ok=True)
os.makedirs("attendance", exist_ok=True)

#  Sidebar 
st.sidebar.markdown("## Face Attendance System")
st.sidebar.markdown("---")
page = st.sidebar.radio(
    "Navigate",
    ["Take Attendance", "Register User", "View Reports", "Manage Users", "How It Works"]
)
st.sidebar.markdown("---")

# Show registered count
users = get_all_users()
st.sidebar.metric("Registered Users", len(users))

#  Helper: Load Encodings 
def load_encodings():
    enc_path = "encodings/encodings.pkl"
    if os.path.exists(enc_path):
        with open(enc_path, "rb") as f:
            return pickle.load(f)
    return [], []

#  Page: Take Attendance 
if page == "Take Attendance":
    st.markdown('<div class="main-header">Take Attendance</div>', unsafe_allow_html=True)

    known_encodings, known_names = load_encodings()

    if not known_encodings:
        st.warning("Warning: No faces registered yet. Please register users first.")
    else:
        col1, col2 = st.columns([2, 1])

        with col1:
            st.markdown("### Live Camera Feed")
            run = st.checkbox("Start Camera", key="camera_run")
            FRAME_WINDOW = st.image([])
            status_text = st.empty()

        with col2:
            st.markdown("### Marked Today")
            marked_display = st.empty()

        if "marked_today" not in st.session_state:
            st.session_state.marked_today = set()

        if run:
            cap = cv2.VideoCapture(0)

            if not cap.isOpened():
                st.error("Error: Cannot access webcam. Please check your camera.")
            else:
                while run:
                    ret, frame = cap.read()
                    if not ret:
                        st.error("Failed to read frame.")
                        break

                    # Resize for speed
                    small = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)
                    rgb_small = cv2.cvtColor(small, cv2.COLOR_BGR2RGB)

                    face_locations = face_recognition.face_locations(rgb_small)
                    face_encs = face_recognition.face_encodings(rgb_small, face_locations)

                    for enc, loc in zip(face_encs, face_locations):
                        matches = face_recognition.compare_faces(known_encodings, enc, tolerance=0.5)
                        face_distances = face_recognition.face_distance(known_encodings, enc)
                        name = "Unknown"
                        confidence = 0

                        if len(face_distances) > 0:
                            best_idx = np.argmin(face_distances)
                            if matches[best_idx]:
                                name = known_names[best_idx]
                                confidence = round((1 - face_distances[best_idx]) * 100, 1)

                        # Scale back up
                        top, right, bottom, left = [v * 4 for v in loc]

                        color = (0, 255, 0) if name != "Unknown" else (0, 0, 255)
                        cv2.rectangle(frame, (left, top), (right, bottom), color, 2)
                        cv2.rectangle(frame, (left, bottom - 35), (right, bottom), color, cv2.FILLED)
                        label = f"{name} ({confidence}%)" if name != "Unknown" else "Unknown"
                        cv2.putText(frame, label, (left + 6, bottom - 6),
                                    cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 1)

                        # Mark attendance
                        if name != "Unknown" and name not in st.session_state.marked_today:
                            mark_attendance(name)
                            st.session_state.marked_today.add(name)
                            status_text.success(f"Attendance marked for **{name}**!")

                    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                    FRAME_WINDOW.image(rgb_frame)

                    # Update marked list
                    if st.session_state.marked_today:
                        marked_display.markdown(
                            "\n".join([f"**{n}**" for n in st.session_state.marked_today])
                        )

                    run = st.session_state.get("camera_run", False)

                cap.release()
        else:
            st.info(" Check the box above to start the camera.")

#  Page: Register User 
elif page == "Register User":
    st.markdown('<div class="main-header"> Register New User</div>', unsafe_allow_html=True)

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("### User Details")
        name = st.text_input("Full Name", placeholder="e.g. Rahul Sharma")
        roll = st.text_input("Roll No / Employee ID", placeholder="e.g. CS2021001")

        st.markdown("### Upload Face Photo")
        uploaded = st.file_uploader("Upload a clear front-facing photo", type=["jpg", "jpeg", "png"])

        if uploaded:
            img = Image.open(uploaded)
            st.image(img, caption="Uploaded Photo", width=250)

    with col2:
        st.markdown("### Or Capture from Webcam")
        capture = st.camera_input("Take a photo")

        if capture:
            img = Image.open(capture)
            st.image(img, caption="Captured Photo", width=250)

    st.markdown("---")
    if st.button("Register User", type="primary"):
        if not name or not roll:
            st.error("Error: Please enter Name and Roll No.")
        elif not uploaded and not capture:
            st.error("Error: Please upload or capture a photo.")
        else:
            source = capture if capture else uploaded
            # Seek to start in case buffer was already read
            source.seek(0)
            file_bytes = np.frombuffer(source.read(), np.uint8)
            img_cv = cv2.imdecode(file_bytes, cv2.IMREAD_COLOR)
            img_array = cv2.cvtColor(img_cv, cv2.COLOR_BGR2RGB)
            img = Image.fromarray(img_array)

            face_locs = face_recognition.face_locations(img_array)
            if not face_locs:
                st.error("Error: No face detected in the image. Please use a clear front-facing photo.")
            else:
                # Save face image
                filename = f"{name}_{roll}.jpg"
                save_path = os.path.join("known_faces", filename)
                img.save(save_path)

                # Save user to database
                from utils.database import register_user
                register_user(name, roll)

                # Re-encode all faces
                encode_faces()

                st.success(f"**{name}** registered successfully!")
                st.balloons()

#  Page: View Reports 
elif page == "View Reports":
    import pandas as pd

    st.markdown('<div class="main-header">Attendance Reports</div>', unsafe_allow_html=True)

    col1, col2, col3 = st.columns(3)
    with col1:
        date_filter = st.date_input("Filter by Date", value=datetime.now().date())
    with col2:
        st.markdown("<br>", unsafe_allow_html=True)
        show_all = st.checkbox("Show All Records")

    records = get_attendance(str(date_filter) if not show_all else None)

    if records:
        df = pd.DataFrame(records, columns=["ID", "Name", "Roll No", "Date", "Time", "Status"])
        df = df.drop(columns=["ID"])

        # Metrics
        m1, m2, m3 = st.columns(3)
        m1.metric("Total Records", len(df))
        m2.metric("Unique Students", df["Name"].nunique())
        m3.metric("Date Range", f"{df['Date'].min()} → {df['Date'].max()}" if show_all else str(date_filter))

        st.markdown("---")
        st.dataframe(df, use_container_width=True)

        # Export
        csv = df.to_csv(index=False).encode("utf-8")
        st.download_button(
            "Download CSV",
            data=csv,
            file_name=f"attendance_{date_filter}.csv",
            mime="text/csv"
        )
    else:
        st.info("No attendance records found for the selected date.")

#  Page: Manage Users 
elif page == "Manage Users":
    import pandas as pd

    st.markdown('<div class="main-header">Manage Users</div>', unsafe_allow_html=True)

    users = get_all_users()
    if users:
        df = pd.DataFrame(users, columns=["ID", "Name", "Roll No", "Registered On"])
        st.dataframe(df.drop(columns=["ID"]), use_container_width=True)

        st.markdown("### Delete User")
        user_names = [f"{u[1]} ({u[2]})" for u in users]
        selected = st.selectbox("Select user to delete", user_names)
        if st.button("Delete Selected User", type="secondary"):
            idx = user_names.index(selected)
            user_id = users[idx][0]
            user_name = users[idx][1]
            user_roll = users[idx][2]

            # Delete from DB
            delete_user(user_id)

            # Delete face image
            for f in os.listdir("known_faces"):
                if f.startswith(f"{user_name}_{user_roll}"):
                    os.remove(os.path.join("known_faces", f))

            # Re-encode
            encode_faces()
            st.success(f" Deleted {user_name}")
            st.rerun()
    else:
        st.info("No users registered yet.")

#  Page: How It Works 
elif page == "How It Works":
    st.markdown('<div class="main-header">How It Works</div>', unsafe_allow_html=True)

    st.markdown("""
    ##  Technology Behind This System

    ### 1. Face Detection
    - Uses **OpenCV** + **dlib HOG** model to detect face regions in each camera frame
    - Draws bounding boxes around detected faces in real time

    ### 2. Face Encoding
    - The `face_recognition` library (built on **dlib's deep learning model**) converts each face into a **128-dimensional vector** (face encoding)
    - These encodings are unique to each person — like a face fingerprint

    ### 3. Face Recognition
    - When a new face is detected, its encoding is compared to all stored encodings using **Euclidean distance**
    - If the distance is below a threshold (0.5), it's a match → attendance is marked

    ### 4. Attendance Logging
    - Matched identities are logged into an **SQLite database** with name, roll no, date & time
    - Each person is marked only **once per session** to avoid duplicates

    ### 5. Reports
    - Filter by date, view all records, and export to **CSV**

    ---
    ##  Project Structure
    ```
    face-attendance-system/
     app.py                  # Main Streamlit UI
     utils/
        database.py         # SQLite operations
        encode.py           # Face encoding logic
     known_faces/            # Registered face images
     encodings/              # Saved face encodings (.pkl)
     attendance/             # CSV exports
     requirements.txt
     Dockerfile
     README.md
    ```
    """)