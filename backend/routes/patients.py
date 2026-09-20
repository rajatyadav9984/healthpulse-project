from flask import Blueprint, jsonify, request
from database.db import get_patients_collection

patients_bp = Blueprint('patients', __name__)

@patients_bp.route('/api/patients', methods=['GET'])
def get_patients():
    """GET /api/patients - Fetch all patient records"""
    try:
        patients_col = get_patients_collection()
        patients = list(patients_col.find())
        for p in patients:
            p['_id'] = str(p['_id'])
        return jsonify(patients), 200
    except Exception as e:
        return jsonify({"error": "Failed to fetch patients", "details": str(e)}), 500

@patients_bp.route('/api/patients', methods=['POST'])
def add_patient():
    """POST /api/patients - Add a new patient record"""
    try:
        data = request.get_json()
        if not data or not data.get('name'):
            return jsonify({"error": "Patient name is required"}), 400

        patient_doc = {
            "name": data.get("name"),
            "age": data.get("age", 0),
            "gender": data.get("gender", "Unknown"),
            "blood_group": data.get("blood_group", "N/A"),
            "contact": data.get("contact", ""),
            "condition": data.get("condition", "General"),
            "status": data.get("status", "Stable")
        }

        patients_col = get_patients_collection()
        result = patients_col.insert_one(patient_doc)
        patient_doc['_id'] = str(result.inserted_id)

        return jsonify({"message": "Patient registered successfully", "patient": patient_doc}), 201
    except Exception as e:
        return jsonify({"error": "Failed to create patient", "details": str(e)}), 500

@patients_bp.route('/api/patients/<patient_id>', methods=['PUT'])
def update_patient(patient_id):
    """PUT /api/patients/<patient_id> - Update patient record"""
    try:
        data = request.get_json()
        if not data:
            return jsonify({"error": "No data provided"}), 400

        patients_col = get_patients_collection()
        
        try:
            from bson.objectid import ObjectId
            query_id = ObjectId(patient_id)
        except Exception:
            query_id = patient_id

        update_data = {}
        for key in ["name", "age", "gender", "blood_group", "contact", "condition", "status"]:
            if key in data:
                update_data[key] = data[key]

        if hasattr(patients_col, 'update_one'):
            patients_col.update_one({"_id": query_id}, {"$set": update_data})

        return jsonify({"message": f"Patient {patient_id} updated successfully"}), 200
    except Exception as e:
        return jsonify({"error": "Failed to update patient", "details": str(e)}), 500

@patients_bp.route('/api/patients/<patient_id>', methods=['DELETE'])
def delete_patient(patient_id):
    """DELETE /api/patients/<patient_id> - Delete a patient record"""
    try:
        patients_col = get_patients_collection()

        try:
            from bson.objectid import ObjectId
            query_id = ObjectId(patient_id)
        except Exception:
            query_id = patient_id

        patients_col.delete_one({"_id": query_id})
        return jsonify({"message": f"Patient {patient_id} deleted successfully"}), 200
    except Exception as e:
        return jsonify({"error": "Failed to delete patient", "details": str(e)}), 500

