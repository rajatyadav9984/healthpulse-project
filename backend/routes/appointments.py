import numpy as np
from flask import Blueprint, jsonify, request
from database.db import get_appointments_collection, get_patients_collection

appointments_bp = Blueprint('appointments', __name__)

# ============================================================================
# Core Appointment CRUD Operations
# ============================================================================

@appointments_bp.route('/api/appointments', methods=['GET'])
def get_appointments():
    """GET /api/appointments - Fetch all scheduled appointments"""
    try:
        apts_col = get_appointments_collection()
        appointments = list(apts_col.find())
        for a in appointments:
            a['_id'] = str(a['_id'])
        return jsonify(appointments), 200
    except Exception as e:
        return jsonify({"error": "Failed to fetch appointments", "details": str(e)}), 500

@appointments_bp.route('/api/appointments', methods=['POST'])
def add_appointment():
    """POST /api/appointments - Schedule a new appointment with double-booking validation and patient auto-registration"""
    try:
        data = request.get_json()
        if not data or not data.get('patient_name') or not data.get('doctor_name'):
            return jsonify({"error": "Patient name and Doctor name are required"}), 400

        patient_name = str(data.get("patient_name")).strip()
        doc_name = data.get("doctor_name")
        date_str = data.get("date")
        time_slot = data.get("time")

        if not date_str or not time_slot:
            return jsonify({"error": "Appointment date and time slot are required"}), 400

        apts_col = get_appointments_collection()
        existing_apts = list(apts_col.find())
        
        # Check double booking
        for a in existing_apts:
            if (a.get("doctor_name") == doc_name and 
                a.get("date") == date_str and 
                a.get("time") == time_slot and 
                a.get("status") != "Cancelled"):
                return jsonify({"error": f"Time slot {time_slot} is already booked for {doc_name} on {date_str}."}), 409

        appointment_doc = {
            "patient_name": patient_name,
            "doctor_name": doc_name,
            "date": date_str,
            "time": time_slot,
            "department": data.get("department", "General"),
            "status": data.get("status", "Scheduled")
        }

        result = apts_col.insert_one(appointment_doc)
        appointment_doc['_id'] = str(result.inserted_id)

        # Auto-register patient in patients database if not already existing
        try:
            patients_col = get_patients_collection()
            existing_patients = list(patients_col.find())
            if not any(p.get("name", "").strip().lower() == patient_name.lower() for p in existing_patients):
                patients_col.insert_one({
                    "name": patient_name,
                    "age": int(data.get("age", 30)),
                    "gender": data.get("gender", "Unknown"),
                    "blood_group": data.get("blood_group", "O+"),
                    "contact": data.get("contact", "+91 98000 00000"),
                    "condition": f"{data.get('department', 'General')} Consultation",
                    "status": "Stable"
                })
        except Exception as pe:
            print("Auto-registration notice:", pe)

        return jsonify({"message": "Appointment scheduled successfully", "appointment": appointment_doc}), 201
    except Exception as e:
        return jsonify({"error": "Failed to schedule appointment", "details": str(e)}), 500

@appointments_bp.route('/api/appointments/<apt_id>', methods=['PUT'])
def update_appointment_status(apt_id):
    """PUT /api/appointments/<apt_id> - Update appointment status (e.g. Completed, Cancelled)"""
    try:
        data = request.get_json()
        new_status = data.get("status", "Scheduled")

        apts_col = get_appointments_collection()
        
        try:
            from bson.objectid import ObjectId
            query_id = ObjectId(apt_id)
        except Exception:
            query_id = apt_id

        if hasattr(apts_col, 'update_one'):
            apts_col.update_one({"_id": query_id}, {"$set": {"status": new_status}})

        return jsonify({"message": f"Appointment {apt_id} status updated to {new_status}"}), 200
    except Exception as e:
        return jsonify({"error": "Failed to update appointment", "details": str(e)}), 500

@appointments_bp.route('/api/appointments/<apt_id>', methods=['DELETE'])
def delete_appointment(apt_id):
    """DELETE /api/appointments/<apt_id> - Delete an appointment record"""
    try:
        apts_col = get_appointments_collection()

        try:
            from bson.objectid import ObjectId
            query_id = ObjectId(apt_id)
        except Exception:
            query_id = apt_id

        apts_col.delete_one({"_id": query_id})
        return jsonify({"message": f"Appointment {apt_id} deleted successfully"}), 200
    except Exception as e:
        return jsonify({"error": "Failed to delete appointment", "details": str(e)}), 500


# ============================================================================
# Feature 4: Simplified Appointment Analytics (Total, Attended, Missed, Rates)
# ============================================================================

@appointments_bp.route('/api/analytics', methods=['GET'])
@appointments_bp.route('/api/analytics/summary', methods=['GET'])
def get_appointment_analytics():
    """
    GET /api/analytics
    Returns dynamic high-level summary KPIs directly from appointments:
    - Total appointments
    - Attended appointments
    - Missed / No-Show appointments
    - Attendance Rate (%)
    - No-Show Rate (%)
    """
    try:
        apts_col = get_appointments_collection()
        appointments = list(apts_col.find())
        total = len(appointments)

        if total == 0:
            return jsonify({
                "total_appointments": 0,
                "attended": 0,
                "no_shows": 0,
                "attendance_rate": 0.0,
                "no_show_rate": 0.0
            }), 200

        attended = sum(1 for a in appointments if a.get("status") in ["Completed", "Attended", "Confirmed"])
        no_shows = sum(1 for a in appointments if a.get("status") in ["Missed", "No-Show", "Cancelled"])

        # Calculate exact percentage
        attendance_rate = round((attended / total) * 100, 1)
        no_show_rate = round((no_shows / total) * 100, 1)

        return jsonify({
            "total_appointments": total,
            "attended": attended,
            "no_shows": no_shows,
            "attendance_rate": attendance_rate,
            "no_show_rate": no_show_rate
        }), 200
    except Exception as e:
        return jsonify({"error": "Failed to fetch analytics", "details": str(e)}), 500


# ============================================================================
# Feature 5: Random Forest Attendance Prediction
# ============================================================================

def _build_rf_classifier():
    """Initializes and trains an in-memory Random Forest Classifier on attendance factors."""
    from sklearn.ensemble import RandomForestClassifier

    # Features: [age, lead_days, previous_no_shows, has_sms_reminder, hour]
    # Label: 1 = Attended, 0 = No-Show
    X = np.array([
        [22, 1, 0, 1, 10], [28, 2, 0, 1, 11], [35, 1, 0, 1, 9],  [42, 2, 0, 1, 10],
        [50, 1, 0, 1, 14], [62, 3, 0, 1, 10], [33, 4, 0, 1, 11], [45, 3, 0, 1, 14],
        [29, 6, 1, 1, 15], [38, 7, 1, 1, 16], [55, 8, 1, 0, 11], [40, 5, 0, 0, 14],
        [24, 14, 2, 0, 16], [31, 18, 3, 0, 17], [27, 21, 2, 0, 16], [60, 25, 3, 0, 17]
    ])
    y = np.array([1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0])

    rf = RandomForestClassifier(n_estimators=30, max_depth=4, random_state=42)
    rf.fit(X, y)
    return rf

_rf_classifier_instance = None

@appointments_bp.route('/api/predict', methods=['POST'])
@appointments_bp.route('/api/predictions/attendance', methods=['POST'])
def predict_attendance():
    """
    POST /api/predict
    Evaluates appointment attendance probability using Random Forest Classifier.
    """
    global _rf_classifier_instance
    try:
        data = request.get_json() or {}
        age = int(data.get('age', 35))
        lead_days = int(data.get('lead_days', 2))
        prev_no_shows = int(data.get('previous_no_shows', 0))
        sms = int(data.get('has_sms_reminder', 1))

        # Parse hour from time string
        time_str = str(data.get('appointment_time', '10:00 AM'))
        hour = 10
        try:
            hour_part = int(time_str.split(':')[0])
            if 'PM' in time_str.upper() and hour_part != 12:
                hour = hour_part + 12
            else:
                hour = hour_part
        except Exception:
            hour = 10

        if _rf_classifier_instance is None:
            _rf_classifier_instance = _build_rf_classifier()

        sample = np.array([[age, lead_days, prev_no_shows, sms, hour]])
        proba = _rf_classifier_instance.predict_proba(sample)[0]
        attended_prob = round(float(proba[1]), 3)

        if attended_prob >= 0.70:
            risk_level = "Low"
            recommendation = "High likelihood of attendance. Send standard reminder notification."
        elif attended_prob >= 0.45:
            risk_level = "Medium"
            recommendation = "Moderate attendance risk. Automated 24h SMS + WhatsApp confirmation recommended."
        else:
            risk_level = "High"
            recommendation = "High risk of No-Show! Clinical coordinator should place a confirmation call."

        return jsonify({
            "status": "success",
            "model_name": "Random Forest Classifier",
            "prediction": "Attended" if attended_prob >= 0.50 else "No-Show",
            "attendance_probability": attended_prob,
            "no_show_probability": round(1.0 - attended_prob, 3),
            "attendance_percentage": f"{round(attended_prob * 100)}%",
            "risk_level": risk_level,
            "recommendation": recommendation
        }), 200
    except Exception as e:
        return jsonify({"error": "Prediction failed", "details": str(e)}), 500
