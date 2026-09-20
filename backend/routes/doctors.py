from flask import Blueprint, jsonify, request
from database.db import get_doctors_collection

doctors_bp = Blueprint('doctors', __name__)

@doctors_bp.route('/api/doctors', methods=['GET'])
def get_doctors():
    """GET /api/doctors - Fetch doctor entries with optional ?department= filter"""
    try:
        dept = request.args.get('department')
        doctors_col = get_doctors_collection()
        all_docs = list(doctors_col.find())
        
        if dept:
            doctors = [d for d in all_docs if d.get('department', '').lower() == dept.lower()]
        else:
            doctors = all_docs

        for d in doctors:
            d['_id'] = str(d['_id'])
        return jsonify(doctors), 200
    except Exception as e:
        return jsonify({"error": "Failed to fetch doctors", "details": str(e)}), 500

@doctors_bp.route('/api/doctors', methods=['POST'])
def add_doctor():
    """POST /api/doctors - Add a new doctor entry"""
    try:
        data = request.get_json()
        if not data or not data.get('name'):
            return jsonify({"error": "Doctor name is required"}), 400

        doctor_doc = {
            "name": data.get("name"),
            "specialization": data.get("specialization", "General Medicine"),
            "department": data.get("department", "Outpatient"),
            "experience": data.get("experience", "1 Yr"),
            "room": data.get("room", "101"),
            "status": data.get("status", "Available")
        }

        doctors_col = get_doctors_collection()
        result = doctors_col.insert_one(doctor_doc)
        doctor_doc['_id'] = str(result.inserted_id)

        return jsonify({"message": "Doctor record created", "doctor": doctor_doc}), 201
    except Exception as e:
        return jsonify({"error": "Failed to create doctor record", "details": str(e)}), 500

@doctors_bp.route('/api/doctors/<doctor_id>', methods=['PUT'])
def update_doctor(doctor_id):
    """PUT /api/doctors/<doctor_id> - Update doctor record"""
    try:
        data = request.get_json()
        if not data:
            return jsonify({"error": "No data provided"}), 400

        doctors_col = get_doctors_collection()
        
        try:
            from bson.objectid import ObjectId
            query_id = ObjectId(doctor_id)
        except Exception:
            query_id = doctor_id

        update_data = {}
        for key in ["name", "specialization", "department", "experience", "room", "status", "schedule"]:
            if key in data:
                update_data[key] = data[key]

        if hasattr(doctors_col, 'update_one'):
            doctors_col.update_one({"_id": query_id}, {"$set": update_data})

        return jsonify({"message": f"Doctor {doctor_id} updated successfully"}), 200
    except Exception as e:
        return jsonify({"error": "Failed to update doctor", "details": str(e)}), 500

@doctors_bp.route('/api/doctors/<doctor_id>', methods=['DELETE'])
def delete_doctor(doctor_id):
    """DELETE /api/doctors/<doctor_id> - Delete a doctor record"""
    try:
        doctors_col = get_doctors_collection()

        try:
            from bson.objectid import ObjectId
            query_id = ObjectId(doctor_id)
        except Exception:
            query_id = doctor_id

        doctors_col.delete_one({"_id": query_id})
        return jsonify({"message": f"Doctor {doctor_id} deleted successfully"}), 200
    except Exception as e:
        return jsonify({"error": "Failed to delete doctor", "details": str(e)}), 500

