from flask import Blueprint, jsonify, request
from database.db import get_appointments_collection

appointments_bp = Blueprint('appointments', __name__)

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
    """POST /api/appointments - Schedule a new appointment with double-booking validation"""
    try:
        data = request.get_json()
        if not data or not data.get('patient_name') or not data.get('doctor_name'):
            return jsonify({"error": "Patient name and Doctor name are required"}), 400

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
            "patient_name": data.get("patient_name"),
            "doctor_name": doc_name,
            "date": date_str,
            "time": time_slot,
            "department": data.get("department", "General"),
            "status": data.get("status", "Scheduled")
        }

        result = apts_col.insert_one(appointment_doc)
        appointment_doc['_id'] = str(result.inserted_id)

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
