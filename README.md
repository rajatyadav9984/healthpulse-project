# ❤️‍🔥 HealthPulse — Healthcare Operations & Clinical Management System

[![Python](https://img.shields.io/badge/Python-3.14-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://python.org)
[![Flask](https://img.shields.io/badge/Backend-Flask-000000?style=for-the-badge&logo=flask&logoColor=white)](https://flask.palletsprojects.com/)
[![MongoDB](https://img.shields.io/badge/Database-MongoDB%20%2F%20JSON-47A248?style=for-the-badge&logo=mongodb&logoColor=white)](https://mongodb.com)
[![License](https://img.shields.io/badge/License-MIT-blue.style=for-the-badge)](LICENSE)

> **HealthPulse** is a modern, full-stack Healthcare Operations Suite designed for hospital administration, emergency response, patient record tracking, doctor scheduling, and real-time clinical monitoring.

---

## 🌟 Key Features

- 🩺 **Patient Record Management**: Register patients, track blood groups, ages, conditions, and real-time admission statuses.
- 👨‍⚕️ **Doctor Directory & Specialty Scheduling**: Manage 50+ clinical departments, doctor availability, room allocations, and shift schedules.
- 📅 **Smart Appointment Booking**: Department-wise specialist filtering, dynamic date picker, and automated slot allocation.
- 🚨 **Emergency Protocol & Code Blue**: Instant trauma alert triggers with direct dispatch notification banners.
- 📊 **Executive Operations Dashboard**: Real-time stats on bed occupancy, active consultations, emergency protocols, and operational metrics.
- ⚡ **1-Click Windows Launcher**: Pre-configured Batch & VBScript scripts to launch full-stack backend & frontend with a single click.

---

## 🛠️ Technology Stack

| Layer | Technologies Used |
|---|---|
| **Frontend** | HTML5, Modern Vanilla CSS3 (Dark Glassmorphism UI), JavaScript (ES6+) |
| **Backend API** | Python 3, Flask, Flask-CORS, PyMongo, Python-dotenv |
| **Database** | MongoDB (Primary) with Automatic Persistent JSON Fallback Storage |
| **Testing** | Pytest |
| **Automation** | Windows Batch Scripts (`.bat`), VBScript (`.vbs`), PowerShell |

---

## 📁 Project Architecture

```text
HealthPulse-project/
├── backend/
│   ├── app.py                 # Flask Server Entrypoint & Static Route Handler
│   ├── requirements.txt       # Python Dependencies
│   ├── database/
│   │   └── db.py              # MongoDB Connection & JSON Storage Fallback Logic
│   ├── routes/
│   │   ├── patients.py        # Patient REST API Endpoints
│   │   ├── doctors.py         # Doctor REST API Endpoints
│   │   └── appointments.py    # Appointment Scheduling API Endpoints
│   ├── data/                  # Persistent Storage Fallback Data
│   └── tests/
│       └── test_app.py        # Pytest Test Cases
├── frontend/
│   ├── index.html             # Operations Dashboard Page
│   ├── patients.html          # Patient Directory Page
│   ├── doctors.html           # Doctor Roster & Shift Schedules Page
│   ├── appointments.html     # Appointment Booking & Consultations Page
│   ├── css/
│   │   └── style.css          # Design Tokens & UI Stylesheet
│   └── js/
│       └── app.js             # Client API Gateway & Dynamic DOM Controllers
├── start_healthpulse.bat      # 🚀 1-Click App Launcher Script
├── stop_healthpulse.bat       # 🛑 1-Click Server Termination Script
├── create_desktop_shortcut.bat# 🖥️ Desktop Icon Generator
└── README.md                  # Project Documentation
```

---

## 🚀 Quick Start Guide

### Option 1: One-Click Launch (Windows)

1. Double-click **`start_healthpulse.bat`** (or the **HealthPulse** Desktop Shortcut).
2. The launcher will automatically check dependencies, start the Flask server on **Port 5000**, and open `http://127.0.0.1:5000/` in your browser.
3. To stop the application, double-click **`stop_healthpulse.bat`**.

---

### Option 2: Manual Setup

1. **Clone the repository:**
   ```bash
   git clone https://github.com/rajatyadav9984/healthpulse-project.git
   cd healthpulse-project
   ```

2. **Install Backend Dependencies:**
   ```bash
   pip install -r backend/requirements.txt
   ```

3. **Start the Flask Backend & Frontend Server:**
   ```bash
   python backend/app.py
   ```

4. **Access the Dashboard:**
   Open your browser and navigate to:
   👉 **`http://127.0.0.1:5000/`**

---

## 🔌 API Reference Endpoints

| Method | Endpoint | Description |
|---|---|---|
| `GET` | `/health` | System health check & API status probe |
| `GET` | `/api/patients` | Fetch list of registered patients |
| `POST` | `/api/patients` | Register a new patient record |
| `GET` | `/api/doctors` | Fetch list of attending doctors & schedules |
| `GET` | `/api/appointments` | Fetch active appointment slots |
| `POST` | `/api/appointments` | Book a doctor consultation slot |

---

## 🧪 Running Unit Tests

Run the automated test suite using `pytest`:

```bash
pytest backend/tests/
```

---

## 🤝 Contributing

Contributions, issues, and feature requests are welcome!  
Feel free to check the [Issues page](https://github.com/rajatyadav9984/healthpulse-project/issues).

---

## 📄 License

Distributed under the MIT License. See `LICENSE` for details.
