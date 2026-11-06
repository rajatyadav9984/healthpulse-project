# ❤️‍🔥 HealthPulse — Healthcare Operations Suite & Clinical AI Intelligence

[![Python](https://img.shields.io/badge/Python-3.14-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://python.org)
[![Flask](https://img.shields.io/badge/Backend-Flask-000000?style=for-the-badge&logo=flask&logoColor=white)](https://flask.palletsprojects.com/)
[![Scikit-Learn](https://img.shields.io/badge/Machine%20Learning-Random%20Forest-F7931E?style=for-the-badge&logo=scikitlearn&logoColor=white)](https://scikit-learn.org/)
[![Terraform](https://img.shields.io/badge/IaC-Terraform-7B42BC?style=for-the-badge&logo=terraform&logoColor=white)](https://terraform.io)
[![Azure](https://img.shields.io/badge/Cloud-Microsoft%20Azure-0078D4?style=for-the-badge&logo=microsoftazure&logoColor=white)](https://azure.microsoft.com/)
[![MongoDB](https://img.shields.io/badge/Database-MongoDB%20%2F%20JSON-47A248?style=for-the-badge&logo=mongodb&logoColor=white)](https://mongodb.com)
[![Pytest](https://img.shields.io/badge/Testing-Pytest%20Passing-success?style=for-the-badge&logo=pytest&logoColor=white)](https://docs.pytest.org/)
[![License](https://img.shields.io/badge/License-MIT-blue?style=for-the-badge)](LICENSE)

> **HealthPulse** is an enterprise-grade Healthcare Operations and Clinical Scheduling Suite. It combines real-time hospital administration, appointment management, live clinical analytics, and **Random Forest Machine Learning** for attendance forecasting, backed by **Automated Terraform Infrastructure on Microsoft Azure**.

---

## 🌟 Core System Modules

The project is built around **5 streamlined, production-ready modules**:

### 1. 🩺 Patient Directory & Medical Records
- Comprehensive patient registration (Full Name, Age, Blood Group, Contact, Medical Condition, Clinical Status).
- Instant status management (`Stable`, `Under Observation`, `Discharged`, `Critical`).
- Search, filter, and real-time patient directory sync with dual-storage persistence.

### 2. 👨‍⚕️ Doctor Roster & Specialty Scheduling
- Specialist directory spanning **50+ clinical departments** (Cardiology, Neurology, Orthopedics, Pediatrics, Emergency, etc.).
- Active shift tracking, room allocations, consultation hours, and instant availability toggling (`Available`, `In Surgery`, `On Leave`).

### 3. 📅 Smart Appointment Booking Engine
- Interactive booking gateway with specialist filtering, calendar date selector, and time-slot scheduling.
- **Double-booking collision prevention**: Returns HTTP `409 Conflict` if a doctor is already booked for that date & time slot.
- **Automated Patient Linking**: Auto-registers first-time patients into the central records database on booking.

### 4. 📊 Live Appointment Analytics
- High-level executive KPI cards:
  - **Total Appointments**: Live count across the facility.
  - **Attended Consultations**: Successfully completed patient visits.
  - **Missed Appointments / No-Shows**: Patient no-shows and cancellations.
  - **Attendance Rate (%) & No-Show Rate (%)**: Computed dynamically from real-time records.
- Interactive **"🔄 Refresh Analytics"** button with dynamic loading feedback and immediate KPI re-computation.

### 5. 🤖 Attendance Prediction (Random Forest AI)
- Built-in **Scikit-learn Random Forest Classifier** evaluating patient attendance likelihood.
- Input parameters: Patient Name & Age, Attending Doctor & Department, Booking Lead Time (days), Prior No-Show History, Automated SMS Reminder (Yes/No), and Appointment Time Slot.
- Flexible input modes: Enter custom patient data freely or choose existing registered patients via smart suggestions.
- Actionable clinical output: Exact **Probability Score (%)**, categorical verdict (`Likely to Attend ✅` vs `High Risk of No-Show ⚠️`), and smart automated recommendations for hospital coordinators.

---

## 🛠️ Technology Stack

| Domain | Technology / Library | Role & Purpose |
|---|---|---|
| **Frontend UI** | HTML5, Vanilla JavaScript (ES6+), CSS3 | High-performance glassmorphism interface, responsive layouts, zero external UI framework dependencies |
| **Backend REST API** | Python 3, Flask, Flask-CORS | Modular Blueprint architecture, validation pipelines, error handling |
| **Machine Learning** | Scikit-learn, NumPy, Joblib | Random Forest Classifier for appointment attendance prediction |
| **Data & Storage** | MongoDB Atlas / Local + JSON Fallback | Hybrid database engine: connects to MongoDB when available; seamlessly falls back to persistent JSON storage |
| **Infrastructure as Code** | HashiCorp Terraform | Full Azure cloud automation: Resource Group, VNet, Subnet, NSG, Public IP, and Linux VM |
| **Cloud Hosting** | Microsoft Azure (Ubuntu 22.04 LTS) | Hosted on Azure cloud VM with automated systemd service management and auto-restart |
| **Test Automation** | Pytest | Comprehensive test suite covering health checks, CRUD, collision prevention, analytics, and ML inference |
| **Local Automation** | Windows Batch Scripts (`.bat`), PowerShell | 1-click startup, port verification, health probing, and browser launch |

---

## 📁 Project Architecture

```text
HealthPulse-project/
│
├── backend/
│   ├── app.py                      # Flask Application Entrypoint & Static Server
│   ├── requirements.txt            # Python Dependencies (Flask, scikit-learn, numpy, pytest)
│   ├── database/
│   │   └── db.py                   # MongoDB Driver & Persistent JSON Storage Fallback
│   ├── routes/
│   │   ├── patients.py             # Patient CRUD & Status Endpoints (/api/patients)
│   │   ├── doctors.py              # Doctor Roster & Specialty Filtering (/api/doctors)
│   │   └── appointments.py         # Appointment Booking, Analytics & AI Prediction (/api/appointments, /api/analytics, /api/predict)
│   ├── data/                       # Persistent JSON Data Store
│   │   ├── patients.json           # Patient Records
│   │   ├── doctors.json            # Doctor Roster Data
│   │   └── appointments.json       # Scheduled Consultations Data
│   └── tests/
│       └── test_app.py             # Pytest Suite (6 Unit & Integration Tests)
│
├── frontend/
│   ├── html/
│   │   ├── index.html              # Executive Operations Dashboard
│   │   ├── patients.html           # Patient Directory & Admission Manager
│   │   ├── doctors.html            # Doctor Specialties & Duty Schedules
│   │   ├── appointments.html      # Appointment Booking & Consultations
│   │   └── analytics.html          # Live Analytics & Random Forest AI Prediction
│   ├── css/
│   │   └── style.css               # Glassmorphism Design System & Dark UI
│   └── js/
│       └── app.js                  # Frontend Gateway, Dynamic DOM & Prediction Controller
│
├── infrastructure/
│   └── terraform/                  # Infrastructure as Code (IaC) for Azure
│       ├── providers.tf            # AzureRM Provider Configuration
│       ├── main.tf                 # Resource Group, VNet, Subnet, NSG, NIC, Public IP & Linux VM
│       ├── variables.tf            # Configurable Input Variables (Region, VM Size, CIDR)
│       ├── outputs.tf              # Outputs (Public IP, SSH Command, VM Name)
│       └── terraform.tfvars        # Environment Specific Values
│
├── pytest.ini                      # Pytest Configuration File
├── start_healthpulse.bat           # 🚀 1-Click Windows App Launcher
├── stop_healthpulse.bat            # 🛑 1-Click Server Shutdown Script
└── README.md                       # Comprehensive Project Documentation
```

---

## 🚀 Quick Start Guide

### Option 1: 1-Click Launch (Windows Local)

1. Double-click **`start_healthpulse.bat`**.
2. The script will automatically:
   - Free Port `5000` from any orphaned instances.
   - Boot up the Flask server in the background.
   - Probe `http://127.0.0.1:5000/health` until the service is healthy.
   - Automatically open the dashboard in your default browser.
3. When finished, double-click **`stop_healthpulse.bat`** to stop all background processes cleanly.

---

### Option 2: Manual Local Setup

1. **Clone the repository:**
   ```bash
   git clone https://github.com/rajatyadav9984/healthpulse-project.git
   cd healthpulse-project
   ```

2. **Install Python dependencies:**
   ```bash
   pip install -r backend/requirements.txt
   ```

3. **Start the HealthPulse Server:**
   ```bash
   python backend/app.py
   ```

4. **Open in Browser:**
   - Operations Dashboard: [http://127.0.0.1:5000/](http://127.0.0.1:5000/)
   - Analytics & ML Prediction: [http://127.0.0.1:5000/analytics.html](http://127.0.0.1:5000/analytics.html)

---

### Option 3: Cloud Deployment with Terraform (Azure VM)

The entire cloud infrastructure is codified with **HashiCorp Terraform** in `infrastructure/terraform/`:

1. **Login to Azure:**
   ```bash
   az login
   ```

2. **Initialize Terraform:**
   ```bash
   cd infrastructure/terraform
   terraform init
   ```

3. **Review and Apply Cloud Plan:**
   ```bash
   terraform plan
   terraform apply -auto-approve
   ```

4. **Outputs Generated:**
   ```text
   resource_group_name = "rg-healthpulse-vm-demo"
   vm_name             = "vm-healthpulse-app-demo"
   vm_public_ip        = "<AZURE_PUBLIC_IP>"
   ssh_command         = "ssh azureuser@<AZURE_PUBLIC_IP>"
   ```

5. **Access Live Cloud Application:**
   Navigate to `http://<AZURE_PUBLIC_IP>:5000/` in any web browser.

---

## 🔌 Complete REST API Reference

### System Probe
| Method | Endpoint | Description | Sample Response |
|---|---|---|---|
| `GET` | `/health` | DevOps health check probe | `{"status": "ok", "service": "HealthPulse Backend API", "version": "1.0.0"}` |

### Patient Management
| Method | Endpoint | Description |
|---|---|---|
| `GET` | `/api/patients` | Retrieve list of all registered patients |
| `POST` | `/api/patients` | Register a new patient record |
| `PUT` | `/api/patients/<id>` | Update patient clinical status or condition |
| `DELETE` | `/api/patients/<id>` | Remove patient record |

### Doctor Management
| Method | Endpoint | Description |
|---|---|---|
| `GET` | `/api/doctors` | Retrieve doctor directory (optional filter: `?department=Cardiology`) |
| `POST` | `/api/doctors` | Add a new attending specialist |
| `PUT` | `/api/doctors/<id>` | Update doctor availability status or shift room |
| `DELETE` | `/api/doctors/<id>` | Remove doctor from roster |

### Appointment Management
| Method | Endpoint | Description |
|---|---|---|
| `GET` | `/api/appointments` | Retrieve all scheduled consultations |
| `POST` | `/api/appointments` | Schedule consultation slot (prevents double booking with `409 Conflict`) |
| `PUT` | `/api/appointments/<id>` | Update consultation status (`Completed`, `Cancelled`, `Missed`) |
| `DELETE` | `/api/appointments/<id>` | Cancel / delete appointment slot |

### Real-time Analytics & AI Forecasting
| Method | Endpoint | Description |
|---|---|---|
| `GET` | `/api/analytics` | Returns real-time KPI metrics (Total, Attended, Missed, Attendance Rate %, No-Show Rate %) |
| `POST` | `/api/predict` | Runs Random Forest AI prediction for attendance likelihood |

#### Sample `/api/predict` Request Body:
```json
{
  "patient_name": "Aman Verma",
  "age": 34,
  "lead_days": 2,
  "previous_no_shows": 0,
  "has_sms_reminder": 1,
  "appointment_time": "10:00 AM"
}
```

#### Sample `/api/predict` Response:
```json
{
  "status": "success",
  "model_name": "Random Forest Classifier",
  "prediction": "Attended",
  "attendance_probability": 1.0,
  "no_show_probability": 0.0,
  "attendance_percentage": "100%",
  "risk_level": "Low",
  "recommendation": "High likelihood of attendance. Send standard reminder notification."
}
```

---

## 🧪 Automated Testing Suite

HealthPulse includes automated tests covering all modules:

```bash
pytest backend/tests/test_app.py -v
```

### Verified Test Coverage:
- `test_health_check`: Probes `/health` endpoint for 200 OK and service metadata.
- `test_patients_crud`: Verifies patient registration, read, update, and deletion.
- `test_doctors_crud`: Validates specialist directory and department-based query filtering.
- `test_appointments_full_workflow`: Tests booking flow, double-booking rejection (`409 Conflict`), status transitions, and cleanup.
- `test_appointment_analytics`: Tests calculation of total consultations, attendance rate, and no-show rate.
- `test_random_forest_attendance_prediction`: Validates Random Forest ML model outputs under low-risk and high-risk patient feature vectors.

```text
============================= 6 passed in 10.77s ==============================
```

---

## ☁️ Azure Cloud & DevOps Highlights

- **Infrastructure as Code (IaC)**: Zero manual cloud provisioning — 100% automated with HashiCorp Terraform.
- **Security Group (NSG)**: Port 22 restricted for SSH administrative access, Port 5000 exposed for web application delivery.
- **Production Daemonization**: Configured with Linux `systemd` (`healthpulse.service`) with `Restart=always` for continuous 24/7 uptime and fault tolerance.

---

## 🤝 Contributing

Contributions, issues, and feature suggestions are welcome!  
Feel free to open an issue or pull request on the [GitHub Repository](https://github.com/rajatyadav9984/healthpulse-project).

---

## 📄 License

Distributed under the **MIT License**. See `LICENSE` for more information.
