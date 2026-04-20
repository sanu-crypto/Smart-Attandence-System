import streamlit as st
import cv2
import numpy as np
import os
import pandas as pd
import pyodbc

from keras_facenet import FaceNet
from sklearn.metrics.pairwise import cosine_similarity
from datetime import datetime
from deep_sort_realtime.deepsort_tracker import DeepSort

# ---------------- PAGE ----------------
st.set_page_config(page_title="Smart Attendance System", layout="wide")
st.title("🎓 Smart Attendance System ")

# ---------------- DATABASE CONNECTION ----------------
conn = None
cursor = None

try:
    conn = pyodbc.connect(
        "Driver={ODBC Driver 17 for SQL Server};"
        "Server=SMARTPHONE\\SQLEXPRESS;"   # change if needed
        "Database=attendance_db;"
        "Trusted_Connection=yes;"
    )
    cursor = conn.cursor()
    st.success("✅ Database Connected Successfully")
except Exception as e:
    st.error(f"❌ Database Connection Failed: {e}")

# ---------------- MODELS ----------------
embedder = FaceNet()
tracker = DeepSort(max_age=30)

face_cascade = cv2.CascadeClassifier(
    cv2.data.haarcascades + "haarcascade_frontalface_default.xml"
)

# ---------------- LOAD KNOWN FACES ----------------
KNOWN_FACES_DIR = "known_faces"
known_embeddings = []
known_names = []

def load_known_faces():
    if not os.path.exists(KNOWN_FACES_DIR):
        os.makedirs(KNOWN_FACES_DIR)
        st.warning("⚠️ Add images inside 'known_faces' folder")
        return

    for file in os.listdir(KNOWN_FACES_DIR):
        path = os.path.join(KNOWN_FACES_DIR, file)
        name = os.path.splitext(file)[0]

        img = cv2.imread(path)
        if img is None:
            continue

        face = cv2.resize(img, (160, 160))
        face_rgb = cv2.cvtColor(face, cv2.COLOR_BGR2RGB)
        emb = embedder.embeddings([face_rgb])[0]

        known_embeddings.append(emb)
        known_names.append(name)

load_known_faces()

# ---------------- ATTENDANCE ----------------
if "marked_ids" not in st.session_state:
    st.session_state.marked_ids = set()

def mark_attendance(name):
    if conn is None:
        return

    now = datetime.now()
    date = now.date()
    time = now.strftime("%H:%M:%S")

    cursor.execute(
        "INSERT INTO attendance (name, date, time) VALUES (?, ?, ?)",
        (name, date, time)
    )
    conn.commit()

    st.success(f"✅ {name} marked present")

# ---------------- CAMERA ----------------
run = st.sidebar.checkbox("Start Camera")
frame_window = st.image([])

if run:
    cap = cv2.VideoCapture(0)

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, 1.3, 5)

        detections = []
        for (x, y, w, h) in faces:
            detections.append(([x, y, w, h], 1.0, 'face'))

        tracks = tracker.update_tracks(detections, frame=frame)

        for track in tracks:
            if not track.is_confirmed():
                continue

            track_id = track.track_id
            l, t, r, b = map(int, track.to_ltrb())

            face_img = frame[t:b, l:r]

            try:
                face_img = cv2.resize(face_img, (160, 160))
                face_rgb = cv2.cvtColor(face_img, cv2.COLOR_BGR2RGB)

                emb = embedder.embeddings([face_rgb])[0]
                sims = cosine_similarity([emb], known_embeddings)[0]

                idx = np.argmax(sims)
                score = sims[idx]

                if score > 0.7:
                    name = known_names[idx]

                    if track_id not in st.session_state.marked_ids:
                        st.session_state.marked_ids.add(track_id)
                        mark_attendance(name)

                    label = f"{name} (ID:{track_id})"
                    color = (0,255,0)
                else:
                    label = "Unknown"
                    color = (0,0,255)

            except:
                label = "Error"
                color = (0,0,255)

            cv2.rectangle(frame, (l,t), (r,b), color, 2)
            cv2.putText(frame, label, (l,t-10),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.8, color, 2)

        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        frame_window.image(frame_rgb)

    cap.release()

# ---------------- DASHBOARD ----------------
st.subheader("📊 Attendance Dashboard")

if conn:
    df = pd.read_sql("SELECT * FROM attendance", conn)

    if not df.empty:
        st.write("### 📅 Daily Attendance")
        st.dataframe(df)

        st.write("### 👤 Person Wise Count")
        st.bar_chart(df['name'].value_counts())

        st.write("### 📈 Monthly Attendance")
        df['date'] = pd.to_datetime(df['date'])
        monthly = df.groupby(df['date'].dt.month)['name'].count()
        st.line_chart(monthly)
    else:
        st.warning("No attendance data yet")
else:
    st.warning("Database not connected")