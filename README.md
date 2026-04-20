# 🎓 Smart Attendance System (Face Recognition + Tracking)

## 📌 Project Overview

The **Smart Attendance System** is an AI-based application that automates attendance marking using **Face Recognition and Tracking**.
It captures live video, detects faces, identifies individuals, and records attendance in a database with real-time analytics.

---

## 🚀 Features

* 📷 **Real-Time Face Detection** using OpenCV
* 🧠 **Face Recognition** using FaceNet
* 🎯 **Multi-Object Tracking** using DeepSORT
* ❌ **Duplicate Prevention** (one person marked once)
* 🗄️ **SQL Server Integration** for permanent storage
* 📊 **Dashboard (Streamlit)**:

  * Daily Attendance
  * Person-wise Count
  * Monthly Analytics
* ⚡ **Fast & Real-Time Processing**

---

## 🛠️ Technologies Used

* **Python**
* **OpenCV**
* **FaceNet (Deep Learning)**
* **DeepSORT (Tracking)**
* **Streamlit (Frontend UI)**
* **SQL Server (Database)**
* **Pandas, NumPy, Scikit-learn**

---

## 📁 Project Structure

```
Smart_Attendance_System/
│
├── app.py
├── requirements.txt
├── known_faces/
│     ├── person1.jpg
│     ├── person2.jpg
│
└── README.md
```

---

## ⚙️ Installation & Setup

### 1️⃣ Clone the Repository

```bash
git clone https://github.com/your-username/smart-attendance-system.git
cd smart-attendance-system
```

---

### 2️⃣ Install Dependencies

```bash
pip install -r requirements.txt
```

---

### 3️⃣ Setup SQL Server

Run the following queries in **SQL Server (SSMS)**:

```sql
CREATE DATABASE attendance_db;
GO

USE attendance_db;

CREATE TABLE attendance (
    id INT IDENTITY(1,1) PRIMARY KEY,
    name VARCHAR(50),
    date DATE,
    time TIME
);
```

---

### 4️⃣ Update Database Connection

In `app.py`, update your server name:

```python
Server=YOUR_SERVER_NAME
```

Example:

```python
Server=SMARTPHONE\\SQLEXPRESS
```

---

### 5️⃣ Add Known Faces

* Create a folder: `known_faces`
* Add images of people
* File name = Person Name

Example:

```
known_faces/
├── sayan.jpg
├── rahul.jpg
```

---

### 6️⃣ Run the Application

```bash
streamlit run app.py
```

---

## 🎯 How It Works

1. Camera captures live video
2. Faces are detected using OpenCV
3. FaceNet generates embeddings
4. System matches faces with known database
5. DeepSORT assigns unique IDs (tracking)
6. Attendance is recorded in SQL database
7. Dashboard displays analytics

---

## 📊 Output

* ✔ Face Recognition with Name
* ✔ Attendance Stored in Database
* ✔ Dashboard Visualization
* ✔ Duplicate Attendance Prevention

---

## ⚠️ Limitations

* Requires good lighting conditions
* Accuracy depends on image quality
* SQL Server must be running

---

## 🔮 Future Enhancements

* 📧 Email/SMS Alerts
* 🌐 Cloud Deployment
* 📱 Mobile App Integration
* 🧠 Advanced Face Models (YOLO Face / RetinaFace)

---

## 👨‍💻 Author

**Sayan Das**
B.E. Artificial Intelligence & Data Science

---

## ⭐ Conclusion

This project demonstrates how **AI + Computer Vision + Database Systems** can be integrated to build a **real-world automated attendance solution**.

---

## 📌 License

This project is for educational purposes.
