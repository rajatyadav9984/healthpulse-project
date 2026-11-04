import pytest
import sys
import os
import time

# Ensure backend root is on sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app import create_app

@pytest.fixture
def client():
    app = create_app()
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_health_check(client):
    """Test 1: Healthcheck endpoint /health"""
    response = client.get('/health')
    assert response.status_code == 200
    json_data = response.get_json()
    assert json_data['status'] == 'ok'
    assert 'HealthPulse' in json_data['service']

def test_patients_crud(client):
    """Test 2: Patient CRUD operations"""
    # 2a. GET patients
    get_res = client.get('/api/patients')
    assert get_res.status_code == 200
    assert isinstance(get_res.get_json(), list)

    # 2b. POST patient
    new_patient = {
        "name": "Aman Verma",
        "age": 32,
        "gender": "Male",
        "blood_group": "O+",
        "contact": "+91 91234 56789",
        "condition": "Fever & Cold",
        "status": "Stable"
    }
    post_res = client.post('/api/patients', json=new_patient)
    assert post_res.status_code == 201
    created = post_res.get_json()['patient']
    p_id = created['_id']
    assert created['name'] == "Aman Verma"

    # 2c. PUT patient
    put_res = client.put(f'/api/patients/{p_id}', json={"condition": "Recovered", "status": "Discharged"})
    assert put_res.status_code == 200

    # 2d. DELETE patient
    del_res = client.delete(f'/api/patients/{p_id}')
    assert del_res.status_code == 200

def test_doctors_crud(client):
    """Test 3: Doctor CRUD operations and filtering"""
    # 3a. GET all doctors
    get_res = client.get('/api/doctors')
    assert get_res.status_code == 200
    all_docs = get_res.get_json()
    assert isinstance(all_docs, list)

    # 3b. GET doctors by department filter
    cardio_res = client.get('/api/doctors?department=Cardiology')
    assert cardio_res.status_code == 200
    for doc in cardio_res.get_json():
        assert doc['department'].lower() == 'cardiology'

    # 3c. POST doctor
    new_doc = {
        "name": "Dr. Test Specialist",
        "specialization": "General Surgery",
        "department": "Emergency",
        "experience": "5 Yrs",
        "room": "105",
        "status": "Available"
    }
    post_res = client.post('/api/doctors', json=new_doc)
    assert post_res.status_code == 201
    doc_id = post_res.get_json()['doctor']['_id']

    # 3d. PUT doctor
    put_res = client.put(f'/api/doctors/{doc_id}', json={"status": "In Surgery"})
    assert put_res.status_code == 200

    # 3e. DELETE doctor
    del_res = client.delete(f'/api/doctors/{doc_id}')
    assert del_res.status_code == 200

def test_appointments_full_workflow(client):
    """Test 4: Appointment Booking, Validation, Double Booking (409), Update, Delete"""
    unique_date = "2026-11-20"
    unique_time = f"09:{int(time.time() * 100) % 50:02d} AM"
    doc_name = "Dr. Vikram Sethi"

    # 4a. Successful Booking
    apt_data = {
        "patient_name": "Rohan Gupta",
        "doctor_name": doc_name,
        "date": unique_date,
        "time": unique_time,
        "department": "Cardiology",
        "status": "Scheduled"
    }
    res = client.post('/api/appointments', json=apt_data)
    assert res.status_code == 201
    apt = res.get_json()['appointment']
    apt_id = apt['_id']

    # 4b. Double Booking Conflict (409 Error)
    duplicate_res = client.post('/api/appointments', json=apt_data)
    assert duplicate_res.status_code == 409
    assert 'already booked' in duplicate_res.get_json()['error']

    # 4c. Missing Required Fields (400 Error)
    incomplete_res = client.post('/api/appointments', json={"patient_name": "Test"})
    assert incomplete_res.status_code == 400

    # 4d. Update Appointment Status (Completed)
    put_res = client.put(f'/api/appointments/{apt_id}', json={"status": "Completed"})
    assert put_res.status_code == 200

    # 4e. Delete Appointment
    del_res = client.delete(f'/api/appointments/{apt_id}')
    assert del_res.status_code == 200

    # Clean up auto-registered test patient so json remains clean
    try:
        p_list = client.get('/api/patients').get_json()
        for p in p_list:
            if p.get('name') == "Rohan Gupta":
                client.delete(f"/api/patients/{p['_id']}")
    except Exception:
        pass

def test_appointment_analytics(client):
    """Test 5: Simplified Appointment Analytics (Total, Attended, Missed, Attendance Rate)"""
    res = client.get('/api/analytics')
    assert res.status_code == 200
    data = res.get_json()
    assert 'total_appointments' in data
    assert 'attended' in data
    assert 'no_shows' in data
    assert 'attendance_rate' in data
    assert 'no_show_rate' in data

def test_random_forest_attendance_prediction(client):
    """Test 6: Random Forest Appointment Attendance Prediction"""
    # 6a. Low risk scenario (Clean history, SMS active, 2 lead days)
    low_risk_payload = {
        "age": 35,
        "lead_days": 2,
        "previous_no_shows": 0,
        "has_sms_reminder": 1,
        "appointment_time": "10:00 AM"
    }
    res_low = client.post('/api/predict', json=low_risk_payload)
    assert res_low.status_code == 200
    data_low = res_low.get_json()
    assert data_low['status'] == 'success'
    assert 'Random Forest' in data_low['model_name']
    assert data_low['attendance_probability'] >= 0.60
    assert data_low['risk_level'] == 'Low'

    # 6b. High risk scenario (Multiple prior no-shows, No SMS, Long lead time)
    high_risk_payload = {
        "age": 28,
        "lead_days": 20,
        "previous_no_shows": 3,
        "has_sms_reminder": 0,
        "appointment_time": "04:30 PM"
    }
    res_high = client.post('/api/predict', json=high_risk_payload)
    assert res_high.status_code == 200
    data_high = res_high.get_json()
    assert data_high['status'] == 'success'
    assert data_high['attendance_probability'] < 0.50
    assert data_high['risk_level'] == 'High'
