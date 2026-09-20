import os
import logging
from pymongo import MongoClient
from pymongo.errors import ConnectionFailure, ServerSelectionTimeoutError

logger = logging.getLogger(__name__)

MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017/")
DB_NAME = os.getenv("DB_NAME", "healthpulse_db")

# Standardized 50 Doctors with Structured Weekly Schedules
SEED_DOCTORS = [
    # Cardiology (Heart)
    {
        "_id": "d1", "name": "Dr. Vikram Sethi", "specialization": "Cardiologist", "department": "Cardiology",
        "focus": "Heart & Cardiovascular / HRT", "experience": "14 Yrs", "room": "302", "status": "Available",
        "schedule": {
            "Monday": {"start": "10:00", "end": "12:30"}, "Tuesday": {"start": "10:00", "end": "12:30"},
            "Wednesday": {"start": "10:00", "end": "12:30"}, "Thursday": {"start": "10:00", "end": "12:30"},
            "Friday": {"start": "10:00", "end": "12:30"}, "Saturday": {"start": "10:00", "end": "12:30"},
            "Sunday": {"start": "10:00", "end": "13:00"}
        }
    },
    {
        "_id": "d2", "name": "Dr. Raj Malhotra", "specialization": "Interventional Cardiologist", "department": "Cardiology",
        "focus": "Angioplasty & Heart Failure", "experience": "16 Yrs", "room": "304", "status": "Available",
        "schedule": {
            "Monday": {"start": "14:00", "end": "16:30"}, "Tuesday": {"start": "14:00", "end": "16:30"},
            "Wednesday": {"start": "14:00", "end": "16:30"}, "Thursday": {"start": "14:00", "end": "16:30"},
            "Friday": {"start": "14:00", "end": "16:30"}, "Saturday": {"start": "14:00", "end": "16:30"}, "Sunday": None
        }
    },
    {
        "_id": "d3", "name": "Dr. Ananya Sharma", "specialization": "Electrophysiologist", "department": "Cardiology",
        "focus": "Heart Rhythm & Pacemaker", "experience": "11 Yrs", "room": "306", "status": "Available",
        "schedule": {
            "Monday": {"start": "17:00", "end": "19:30"}, "Tuesday": {"start": "17:00", "end": "19:30"},
            "Wednesday": {"start": "17:00", "end": "19:30"}, "Thursday": {"start": "17:00", "end": "19:30"},
            "Friday": {"start": "17:00", "end": "19:30"}, "Saturday": {"start": "17:00", "end": "19:30"}, "Sunday": None
        }
    },

    # Dermatology (Skin)
    {
        "_id": "d4", "name": "Dr. Meera Kapoor", "specialization": "Dermatologist", "department": "Dermatology",
        "focus": "Skin & Hair Care", "experience": "9 Yrs", "room": "205", "status": "Available",
        "schedule": {
            "Monday": {"start": "10:00", "end": "13:00"}, "Tuesday": {"start": "10:00", "end": "13:00"},
            "Wednesday": {"start": "10:00", "end": "13:00"}, "Thursday": None,
            "Friday": {"start": "10:00", "end": "13:00"}, "Saturday": {"start": "10:00", "end": "13:00"}, "Sunday": None
        }
    },
    {
        "_id": "d5", "name": "Dr. Priya Sharma", "specialization": "Cosmetic Dermatologist", "department": "Dermatology",
        "focus": "Laser & Aesthetic Dermatology", "experience": "12 Yrs", "room": "207", "status": "On Leave",
        "schedule": {
            "Monday": None, "Tuesday": {"start": "14:00", "end": "18:00"},
            "Wednesday": None, "Thursday": {"start": "14:00", "end": "18:00"},
            "Friday": {"start": "14:00", "end": "18:00"}, "Saturday": {"start": "11:00", "end": "15:00"}, "Sunday": None
        }
    },
    {
        "_id": "d6", "name": "Dr. Amit Verma", "specialization": "Pediatric Dermatologist", "department": "Dermatology",
        "focus": "Eczema & Skin Infections", "experience": "10 Yrs", "room": "209", "status": "Available",
        "schedule": {
            "Monday": {"start": "11:00", "end": "14:00"}, "Tuesday": {"start": "11:00", "end": "14:00"},
            "Wednesday": {"start": "11:00", "end": "14:00"}, "Thursday": {"start": "11:00", "end": "14:00"},
            "Friday": None, "Saturday": None, "Sunday": None
        }
    },

    # Neurology (Brain)
    {
        "_id": "d7", "name": "Dr. Sunita Mehta", "specialization": "Neurologist", "department": "Neurology",
        "focus": "Brain & Nerves", "experience": "12 Yrs", "room": "415", "status": "In Surgery",
        "schedule": {
            "Monday": {"start": "10:00", "end": "13:00"}, "Tuesday": {"start": "10:00", "end": "13:00"},
            "Wednesday": None, "Thursday": {"start": "10:00", "end": "13:00"},
            "Friday": {"start": "10:00", "end": "13:00"}, "Saturday": {"start": "10:00", "end": "12:00"}, "Sunday": None
        }
    },
    {
        "_id": "d8", "name": "Dr. Rahul Singh", "specialization": "Stroke Specialist", "department": "Neurology",
        "focus": "Stroke & Epilepsy Care", "experience": "15 Yrs", "room": "417", "status": "Available",
        "schedule": {
            "Monday": {"start": "14:00", "end": "17:00"}, "Tuesday": {"start": "14:00", "end": "17:00"},
            "Wednesday": {"start": "14:00", "end": "17:00"}, "Thursday": None,
            "Friday": {"start": "14:00", "end": "17:00"}, "Saturday": None, "Sunday": None
        }
    },
    {
        "_id": "d9", "name": "Dr. Arjun Gupta", "specialization": "Neuro-Physiologist", "department": "Neurology",
        "focus": "Nerve Conduction & EEG", "experience": "8 Yrs", "room": "419", "status": "On Leave",
        "schedule": {
            "Monday": None, "Tuesday": {"start": "09:00", "end": "12:00"},
            "Wednesday": None, "Thursday": {"start": "09:00", "end": "12:00"},
            "Friday": None, "Saturday": {"start": "09:00", "end": "13:00"}, "Sunday": None
        }
    },

    # Orthopedics (Bones & Joints)
    {
        "_id": "d10", "name": "Dr. Rohan Deshmukh", "specialization": "Orthopedic Specialist", "department": "Orthopedics",
        "focus": "Bones, Joints & Muscles", "experience": "10 Yrs", "room": "108", "status": "Available",
        "schedule": {
            "Monday": {"start": "10:00", "end": "13:00"}, "Tuesday": {"start": "10:00", "end": "13:00"},
            "Wednesday": {"start": "10:00", "end": "13:00"}, "Thursday": {"start": "10:00", "end": "13:00"},
            "Friday": {"start": "10:00", "end": "13:00"}, "Saturday": None,
            "Sunday": {"start": "10:00", "end": "13:00"}
        }
    },
    {
        "_id": "d11", "name": "Dr. Varun Tej", "specialization": "Spine & Joint Replacement", "department": "Orthopedics",
        "focus": "Knee Replacement & Spine Surgery", "experience": "15 Yrs", "room": "110", "status": "Available",
        "schedule": {
            "Monday": None, "Tuesday": {"start": "14:00", "end": "18:00"},
            "Wednesday": None, "Thursday": {"start": "14:00", "end": "18:00"},
            "Friday": {"start": "14:00", "end": "18:00"}, "Saturday": {"start": "10:00", "end": "14:00"}, "Sunday": None
        }
    },
    {
        "_id": "d12", "name": "Dr. Siddharth Kaul", "specialization": "Sports Medicine Specialist", "department": "Orthopedics",
        "focus": "Ligament Tear & Sports Rehab", "experience": "9 Yrs", "room": "106", "status": "On Leave",
        "schedule": {
            "Monday": {"start": "15:00", "end": "19:00"}, "Tuesday": None,
            "Wednesday": {"start": "15:00", "end": "19:00"}, "Thursday": None,
            "Friday": {"start": "15:00", "end": "19:00"}, "Saturday": {"start": "10:00", "end": "13:00"}, "Sunday": None
        }
    },

    # Pediatrics (Children)
    {
        "_id": "d13", "name": "Dr. Neha Gupta", "specialization": "Pediatrician", "department": "Pediatrics",
        "focus": "Child Healthcare & Vaccination", "experience": "11 Yrs", "room": "204", "status": "Available",
        "schedule": {
            "Monday": {"start": "09:00", "end": "13:00"}, "Tuesday": {"start": "09:00", "end": "13:00"},
            "Wednesday": {"start": "09:00", "end": "13:00"}, "Thursday": {"start": "09:00", "end": "13:00"},
            "Friday": {"start": "09:00", "end": "13:00"}, "Saturday": None,
            "Sunday": {"start": "10:00", "end": "12:30"}
        }
    },
    {
        "_id": "d14", "name": "Dr. Ajay Rastogi", "specialization": "Pediatric Surgeon", "department": "Pediatrics",
        "focus": "Children's Surgical Care", "experience": "12 Yrs", "room": "OR-4", "status": "In Surgery",
        "schedule": {
            "Monday": None, "Tuesday": {"start": "14:00", "end": "17:00"},
            "Wednesday": {"start": "14:00", "end": "17:00"}, "Thursday": None,
            "Friday": {"start": "14:00", "end": "17:00"}, "Saturday": {"start": "10:00", "end": "13:00"}, "Sunday": None
        }
    },
    {
        "_id": "d15", "name": "Dr. Ritu Verma", "specialization": "Neonatologist", "department": "Pediatrics",
        "focus": "Newborn & ICU Care", "experience": "10 Yrs", "room": "206", "status": "Available",
        "schedule": {
            "Monday": {"start": "15:00", "end": "18:00"}, "Tuesday": {"start": "15:00", "end": "18:00"},
            "Wednesday": None, "Thursday": {"start": "15:00", "end": "18:00"},
            "Friday": {"start": "15:00", "end": "18:00"}, "Saturday": None, "Sunday": None
        }
    },

    # Ophthalmology (Eyes)
    {
        "_id": "d16", "name": "Dr. Arvind Swamy", "specialization": "Ophthalmologist", "department": "Ophthalmology",
        "focus": "Eyes & Vision Care", "experience": "13 Yrs", "room": "309", "status": "Available",
        "schedule": {
            "Monday": {"start": "10:00", "end": "13:00"}, "Tuesday": {"start": "10:00", "end": "13:00"},
            "Wednesday": None, "Thursday": {"start": "10:00", "end": "13:00"},
            "Friday": {"start": "10:00", "end": "13:00"}, "Saturday": {"start": "10:00", "end": "12:00"}, "Sunday": None
        }
    },
    {
        "_id": "d17", "name": "Dr. Abhinav Reddy", "specialization": "Retina Specialist", "department": "Ophthalmology",
        "focus": "Retina & Laser Surgery", "experience": "12 Yrs", "room": "310", "status": "On Leave",
        "schedule": {
            "Monday": None, "Tuesday": {"start": "14:00", "end": "17:00"},
            "Wednesday": {"start": "10:00", "end": "13:00"}, "Thursday": None,
            "Friday": {"start": "14:00", "end": "17:00"}, "Saturday": {"start": "10:00", "end": "13:00"}, "Sunday": None
        }
    },
    {
        "_id": "d18", "name": "Dr. Kunal Singhal", "specialization": "Cataract Surgeon", "department": "Ophthalmology",
        "focus": "Cataract & LASIK Surgery", "experience": "15 Yrs", "room": "OR-5", "status": "Available",
        "schedule": {
            "Monday": {"start": "14:00", "end": "18:00"}, "Tuesday": None,
            "Wednesday": {"start": "14:00", "end": "18:00"}, "Thursday": {"start": "14:00", "end": "18:00"},
            "Friday": None, "Saturday": None, "Sunday": None
        }
    },

    # Dentistry (Teeth)
    {
        "_id": "d19", "name": "Dr. Pooja Singhania", "specialization": "Dentist", "department": "Dentistry",
        "focus": "Teeth & Dental Health", "experience": "8 Yrs", "room": "112", "status": "Available",
        "schedule": {
            "Monday": {"start": "10:00", "end": "14:00"}, "Tuesday": {"start": "10:00", "end": "14:00"},
            "Wednesday": {"start": "10:00", "end": "14:00"}, "Thursday": None,
            "Friday": {"start": "10:00", "end": "14:00"}, "Saturday": {"start": "10:00", "end": "13:00"}, "Sunday": None
        }
    },
    {
        "_id": "d20", "name": "Dr. Farhan Qureshi", "specialization": "Maxillofacial Surgeon", "department": "Dentistry",
        "focus": "Jaw Surgery & Dental Implants", "experience": "13 Yrs", "room": "114", "status": "On Leave",
        "schedule": {
            "Monday": None, "Tuesday": {"start": "15:00", "end": "19:00"},
            "Wednesday": None, "Thursday": {"start": "15:00", "end": "19:00"},
            "Friday": {"start": "15:00", "end": "19:00"}, "Saturday": None, "Sunday": None
        }
    },
    {
        "_id": "d21", "name": "Dr. Tanya Mittal", "specialization": "Orthodontist", "department": "Dentistry",
        "focus": "Braces & Teeth Alignment", "experience": "7 Yrs", "room": "113", "status": "Available",
        "schedule": {
            "Monday": {"start": "14:00", "end": "17:00"}, "Tuesday": None,
            "Wednesday": {"start": "14:00", "end": "17:00"}, "Thursday": None,
            "Friday": {"start": "14:00", "end": "17:00"}, "Saturday": {"start": "11:00", "end": "14:00"}, "Sunday": None
        }
    },

    # ENT (Ear, Nose, Throat)
    {
        "_id": "d22", "name": "Dr. Alok Verma", "specialization": "ENT Specialist", "department": "ENT",
        "focus": "Ear, Nose & Throat Care", "experience": "14 Yrs", "room": "218", "status": "Available",
        "schedule": {
            "Monday": {"start": "10:00", "end": "13:00"}, "Tuesday": {"start": "10:00", "end": "13:00"},
            "Wednesday": None, "Thursday": {"start": "10:00", "end": "13:00"},
            "Friday": {"start": "10:00", "end": "13:00"}, "Saturday": {"start": "10:00", "end": "12:00"}, "Sunday": None
        }
    },
    {
        "_id": "d23", "name": "Dr. Shrikant Shinde", "specialization": "Rhinologist", "department": "ENT",
        "focus": "Nose & Sinus Surgery", "experience": "10 Yrs", "room": "219", "status": "Available",
        "schedule": {
            "Monday": None, "Tuesday": {"start": "14:00", "end": "17:00"},
            "Wednesday": {"start": "10:00", "end": "13:00"}, "Thursday": None,
            "Friday": {"start": "14:00", "end": "17:00"}, "Saturday": {"start": "10:00", "end": "13:00"}, "Sunday": None
        }
    },
    {
        "_id": "d24", "name": "Dr. Radhika Sen", "specialization": "Otologist", "department": "ENT",
        "focus": "Ear & Hearing Disorders", "experience": "11 Yrs", "room": "220", "status": "On Leave",
        "schedule": {
            "Monday": {"start": "14:00", "end": "17:00"}, "Tuesday": None,
            "Wednesday": {"start": "14:00", "end": "17:00"}, "Thursday": {"start": "14:00", "end": "17:00"},
            "Friday": None, "Saturday": None, "Sunday": None
        }
    },

    # Emergency & Critical Care
    {
        "_id": "d25", "name": "Dr. Karan Thapar", "specialization": "Emergency Medicine Lead", "department": "Emergency",
        "focus": "Trauma & ER Command Center", "experience": "12 Yrs", "room": "ER-1", "status": "Available",
        "schedule": {
            "Monday": {"start": "08:00", "end": "20:00"}, "Tuesday": {"start": "08:00", "end": "20:00"},
            "Wednesday": {"start": "08:00", "end": "20:00"}, "Thursday": {"start": "08:00", "end": "20:00"},
            "Friday": {"start": "08:00", "end": "20:00"}, "Saturday": {"start": "08:00", "end": "20:00"},
            "Sunday": {"start": "08:00", "end": "20:00"}
        }
    },
    {
        "_id": "d26", "name": "Dr. Vandana Tripathi", "specialization": "Critical Care Specialist", "department": "Emergency",
        "focus": "ICU & Ventilator Management", "experience": "15 Yrs", "room": "ICU-3", "status": "Available",
        "schedule": {
            "Monday": {"start": "10:00", "end": "18:00"}, "Tuesday": {"start": "10:00", "end": "18:00"},
            "Wednesday": {"start": "10:00", "end": "18:00"}, "Thursday": {"start": "10:00", "end": "18:00"},
            "Friday": {"start": "10:00", "end": "18:00"}, "Saturday": {"start": "10:00", "end": "14:00"},
            "Sunday": {"start": "10:00", "end": "16:00"}
        }
    },

    # Pulmonology (Lungs)
    {
        "_id": "d27", "name": "Dr. Suresh Nambiar", "specialization": "Pulmonologist", "department": "Pulmonology",
        "focus": "Asthma, COPD & Lung Care", "experience": "14 Yrs", "room": "312", "status": "Available",
        "schedule": {
            "Monday": {"start": "10:00", "end": "13:00"}, "Tuesday": {"start": "10:00", "end": "13:00"},
            "Wednesday": {"start": "10:00", "end": "13:00"}, "Thursday": {"start": "10:00", "end": "13:00"},
            "Friday": {"start": "10:00", "end": "13:00"}, "Saturday": {"start": "10:00", "end": "12:00"}, "Sunday": None
        }
    },
    {
        "_id": "d28", "name": "Dr. Kavita Pillai", "specialization": "Sleep Medicine Specialist", "department": "Pulmonology",
        "focus": "Sleep Apnea & Respiratory Rehab", "experience": "9 Yrs", "room": "314", "status": "Available",
        "schedule": {
            "Monday": None, "Tuesday": {"start": "14:00", "end": "17:00"},
            "Wednesday": None, "Thursday": {"start": "14:00", "end": "17:00"},
            "Friday": {"start": "14:00", "end": "17:00"}, "Saturday": None, "Sunday": None
        }
    },
    {
        "_id": "d29", "name": "Dr. Manish Saxena", "specialization": "Interventional Pulmonologist", "department": "Pulmonology",
        "focus": "Bronchoscopy & Pleural Diseases", "experience": "11 Yrs", "room": "316", "status": "In Surgery",
        "schedule": {
            "Monday": {"start": "15:00", "end": "18:00"}, "Tuesday": None,
            "Wednesday": {"start": "15:00", "end": "18:00"}, "Thursday": None,
            "Friday": {"start": "15:00", "end": "18:00"}, "Saturday": None, "Sunday": None
        }
    },

    # Gastroenterology (Stomach & Liver)
    {
        "_id": "d30", "name": "Dr. Sameer Joshi", "specialization": "Gastroenterologist", "department": "Gastroenterology",
        "focus": "Endoscopy & Gut Health", "experience": "13 Yrs", "room": "222", "status": "Available",
        "schedule": {
            "Monday": {"start": "10:00", "end": "13:00"}, "Tuesday": {"start": "10:00", "end": "13:00"},
            "Wednesday": {"start": "10:00", "end": "13:00"}, "Thursday": {"start": "10:00", "end": "13:00"},
            "Friday": {"start": "10:00", "end": "13:00"}, "Saturday": None, "Sunday": None
        }
    },
    {
        "_id": "d31", "name": "Dr. Shalini Roy", "specialization": "Hepatologist", "department": "Gastroenterology",
        "focus": "Liver Cirrhosis & Fatty Liver", "experience": "16 Yrs", "room": "224", "status": "Available",
        "schedule": {
            "Monday": None, "Tuesday": {"start": "14:00", "end": "17:00"},
            "Wednesday": None, "Thursday": {"start": "14:00", "end": "17:00"},
            "Friday": {"start": "14:00", "end": "17:00"}, "Saturday": {"start": "10:00", "end": "13:00"}, "Sunday": None
        }
    },
    {
        "_id": "d32", "name": "Dr. Harish Bhasin", "specialization": "GI Endoscopist", "department": "Gastroenterology",
        "focus": "Colonoscopy & Ulcer Management", "experience": "10 Yrs", "room": "226", "status": "On Leave",
        "schedule": {
            "Monday": {"start": "14:00", "end": "17:00"}, "Tuesday": None,
            "Wednesday": {"start": "14:00", "end": "17:00"}, "Thursday": None,
            "Friday": None, "Saturday": None, "Sunday": None
        }
    },

    # Nephrology (Kidney)
    {
        "_id": "d33", "name": "Dr. Vivek Anand", "specialization": "Nephrologist", "department": "Nephrology",
        "focus": "Kidney Care & Dialysis", "experience": "15 Yrs", "room": "402", "status": "Available",
        "schedule": {
            "Monday": {"start": "10:00", "end": "13:00"}, "Tuesday": {"start": "10:00", "end": "13:00"},
            "Wednesday": {"start": "10:00", "end": "13:00"}, "Thursday": {"start": "10:00", "end": "13:00"},
            "Friday": {"start": "10:00", "end": "13:00"}, "Saturday": {"start": "10:00", "end": "12:00"}, "Sunday": None
        }
    },
    {
        "_id": "d34", "name": "Dr. Geeta Kulkarni", "specialization": "Transplant Nephrologist", "department": "Nephrology",
        "focus": "Renal Transplant & Chronic Kidney Disease", "experience": "12 Yrs", "room": "404", "status": "Available",
        "schedule": {
            "Monday": None, "Tuesday": {"start": "14:00", "end": "17:00"},
            "Wednesday": {"start": "14:00", "end": "17:00"}, "Thursday": None,
            "Friday": {"start": "14:00", "end": "17:00"}, "Saturday": None, "Sunday": None
        }
    },
    {
        "_id": "d35", "name": "Dr. Deepak Dave", "specialization": "Dialysis Specialist", "department": "Nephrology",
        "focus": "Hemodialysis & Kidney Failure", "experience": "8 Yrs", "room": "406", "status": "Available",
        "schedule": {
            "Monday": {"start": "15:00", "end": "19:00"}, "Tuesday": {"start": "15:00", "end": "19:00"},
            "Wednesday": None, "Thursday": {"start": "15:00", "end": "19:00"},
            "Friday": {"start": "15:00", "end": "19:00"}, "Saturday": None, "Sunday": None
        }
    },

    # Urology (Urinary Track & Kidney Stones)
    {
        "_id": "d36", "name": "Dr. Pankaj Mishra", "specialization": "Urologist", "department": "Urology",
        "focus": "Kidney Stones & Prostate Care", "experience": "14 Yrs", "room": "408", "status": "Available",
        "schedule": {
            "Monday": {"start": "10:00", "end": "13:00"}, "Tuesday": {"start": "10:00", "end": "13:00"},
            "Wednesday": {"start": "10:00", "end": "13:00"}, "Thursday": {"start": "10:00", "end": "13:00"},
            "Friday": {"start": "10:00", "end": "13:00"}, "Saturday": None, "Sunday": None
        }
    },
    {
        "_id": "d37", "name": "Dr. Nikhil Bajaj", "specialization": "Andrologist & Robotic Urologist", "department": "Urology",
        "focus": "Robotic Surgery & Men's Health", "experience": "11 Yrs", "room": "410", "status": "In Surgery",
        "schedule": {
            "Monday": None, "Tuesday": {"start": "14:00", "end": "18:00"},
            "Wednesday": None, "Thursday": {"start": "14:00", "end": "18:00"},
            "Friday": {"start": "14:00", "end": "18:00"}, "Saturday": {"start": "10:00", "end": "13:00"}, "Sunday": None
        }
    },
    {
        "_id": "d38", "name": "Dr. Tarun Nanda", "specialization": "Endourologist", "department": "Urology",
        "focus": "Laser Lithotripsy & Urinary Tract", "experience": "9 Yrs", "room": "412", "status": "On Leave",
        "schedule": {
            "Monday": {"start": "14:00", "end": "17:00"}, "Tuesday": None,
            "Wednesday": {"start": "14:00", "end": "17:00"}, "Thursday": None,
            "Friday": None, "Saturday": None, "Sunday": None
        }
    },

    # Oncology (Cancer Care)
    {
        "_id": "d39", "name": "Dr. Rashmi Hegde", "specialization": "Medical Oncologist", "department": "Oncology",
        "focus": "Chemotherapy & Tumour Care", "experience": "16 Yrs", "room": "502", "status": "Available",
        "schedule": {
            "Monday": {"start": "10:00", "end": "13:00"}, "Tuesday": {"start": "10:00", "end": "13:00"},
            "Wednesday": {"start": "10:00", "end": "13:00"}, "Thursday": {"start": "10:00", "end": "13:00"},
            "Friday": {"start": "10:00", "end": "13:00"}, "Saturday": {"start": "10:00", "end": "12:00"}, "Sunday": None
        }
    },
    {
        "_id": "d40", "name": "Dr. Ashok Chawla", "specialization": "Surgical Oncologist", "department": "Oncology",
        "focus": "Cancer Surgery & Tumour Resection", "experience": "18 Yrs", "room": "OR-2", "status": "In Surgery",
        "schedule": {
            "Monday": None, "Tuesday": {"start": "14:00", "end": "17:00"},
            "Wednesday": {"start": "14:00", "end": "17:00"}, "Thursday": None,
            "Friday": {"start": "14:00", "end": "17:00"}, "Saturday": None, "Sunday": None
        }
    },
    {
        "_id": "d41", "name": "Dr. Swati Deshmukh", "specialization": "Radiation Oncologist", "department": "Oncology",
        "focus": "Radiotherapy & Target Therapy", "experience": "10 Yrs", "room": "504", "status": "Available",
        "schedule": {
            "Monday": {"start": "14:00", "end": "18:00"}, "Tuesday": None,
            "Wednesday": {"start": "14:00", "end": "18:00"}, "Thursday": {"start": "14:00", "end": "18:00"},
            "Friday": None, "Saturday": None, "Sunday": None
        }
    },

    # Endocrinology (Diabetes & Hormones)
    {
        "_id": "d42", "name": "Dr. Naresh Trehan", "specialization": "Endocrinologist", "department": "Endocrinology",
        "focus": "Diabetes & Thyroid Disorder", "experience": "15 Yrs", "room": "318", "status": "Available",
        "schedule": {
            "Monday": {"start": "10:00", "end": "13:00"}, "Tuesday": {"start": "10:00", "end": "13:00"},
            "Wednesday": {"start": "10:00", "end": "13:00"}, "Thursday": {"start": "10:00", "end": "13:00"},
            "Friday": {"start": "10:00", "end": "13:00"}, "Saturday": {"start": "10:00", "end": "13:00"}, "Sunday": None
        }
    },
    {
        "_id": "d43", "name": "Dr. Sunayana Sen", "specialization": "Diabetologist", "department": "Endocrinology",
        "focus": "Type-1 & Type-2 Diabetes Care", "experience": "9 Yrs", "room": "320", "status": "Available",
        "schedule": {
            "Monday": None, "Tuesday": {"start": "14:00", "end": "17:00"},
            "Wednesday": None, "Thursday": {"start": "14:00", "end": "17:00"},
            "Friday": {"start": "14:00", "end": "17:00"}, "Saturday": None, "Sunday": None
        }
    },

    # Psychiatry (Mental Health)
    {
        "_id": "d44", "name": "Dr. Kabir Bedi", "specialization": "Psychiatrist", "department": "Psychiatry",
        "focus": "Anxiety, Depression & Mental Wellness", "experience": "13 Yrs", "room": "510", "status": "Available",
        "schedule": {
            "Monday": {"start": "11:00", "end": "15:00"}, "Tuesday": {"start": "11:00", "end": "15:00"},
            "Wednesday": {"start": "11:00", "end": "15:00"}, "Thursday": {"start": "11:00", "end": "15:00"},
            "Friday": {"start": "11:00", "end": "15:00"}, "Saturday": None, "Sunday": None
        }
    },
    {
        "_id": "d45", "name": "Dr. Smita Patil", "specialization": "Clinical Psychologist", "department": "Psychiatry",
        "focus": "Cognitive Behavior & Counseling", "experience": "8 Yrs", "room": "512", "status": "On Leave",
        "schedule": {
            "Monday": None, "Tuesday": {"start": "14:00", "end": "18:00"},
            "Wednesday": None, "Thursday": {"start": "14:00", "end": "18:00"},
            "Friday": {"start": "14:00", "end": "18:00"}, "Saturday": {"start": "10:00", "end": "13:00"}, "Sunday": None
        }
    },

    # General Surgery
    {
        "_id": "d46", "name": "Dr. Balram Bhargava", "specialization": "General Surgeon", "department": "General Surgery",
        "focus": "Hernia, Gallbladder & Laparoscopy", "experience": "17 Yrs", "room": "OR-1", "status": "Available",
        "schedule": {
            "Monday": {"start": "10:00", "end": "13:00"}, "Tuesday": {"start": "10:00", "end": "13:00"},
            "Wednesday": {"start": "10:00", "end": "13:00"}, "Thursday": {"start": "10:00", "end": "13:00"},
            "Friday": {"start": "10:00", "end": "13:00"}, "Saturday": {"start": "10:00", "end": "12:00"}, "Sunday": None
        }
    },
    {
        "_id": "d47", "name": "Dr. Vinod Paul", "specialization": "Laparoscopic Surgeon", "department": "General Surgery",
        "focus": "Minimally Invasive Surgery", "experience": "14 Yrs", "room": "OR-3", "status": "In Surgery",
        "schedule": {
            "Monday": None, "Tuesday": {"start": "14:00", "end": "17:00"},
            "Wednesday": {"start": "14:00", "end": "17:00"}, "Thursday": None,
            "Friday": {"start": "14:00", "end": "17:00"}, "Saturday": None, "Sunday": None
        }
    },
    {
        "_id": "d48", "name": "Dr. Anuj Bhatia", "specialization": "Trauma Surgeon", "department": "General Surgery",
        "focus": "Emergency & Acute Surgical Care", "experience": "11 Yrs", "room": "OR-6", "status": "Available",
        "schedule": {
            "Monday": {"start": "15:00", "end": "19:00"}, "Tuesday": None,
            "Wednesday": {"start": "15:00", "end": "19:00"}, "Thursday": None,
            "Friday": {"start": "15:00", "end": "19:00"}, "Saturday": None, "Sunday": None
        }
    },

    # Internal Medicine
    {
        "_id": "d49", "name": "Dr. Randeep Guleria", "specialization": "Internal Medicine Lead", "department": "General Medicine",
        "focus": "Chronic Fever, Diabetes & Hypertension", "experience": "20 Yrs", "room": "101", "status": "Available",
        "schedule": {
            "Monday": {"start": "09:00", "end": "13:00"}, "Tuesday": {"start": "09:00", "end": "13:00"},
            "Wednesday": {"start": "09:00", "end": "13:00"}, "Thursday": {"start": "09:00", "end": "13:00"},
            "Friday": {"start": "09:00", "end": "13:00"}, "Saturday": {"start": "09:00", "end": "13:00"}, "Sunday": None
        }
    },
    {
        "_id": "d50", "name": "Dr. Soumya Swaminathan", "specialization": "General Physician", "department": "General Medicine",
        "focus": "Preventive Care & Infectious Diseases", "experience": "18 Yrs", "room": "103", "status": "Available",
        "schedule": {
            "Monday": {"start": "14:00", "end": "18:00"}, "Tuesday": {"start": "14:00", "end": "18:00"},
            "Wednesday": {"start": "14:00", "end": "18:00"}, "Thursday": {"start": "14:00", "end": "18:00"},
            "Friday": {"start": "14:00", "end": "18:00"}, "Saturday": None, "Sunday": None
        }
    }
]

import json

DATA_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "data")
os.makedirs(DATA_DIR, exist_ok=True)

class JSONCollection:
    """Persistent file-backed JSON collection when local MongoDB server is offline."""
    def __init__(self, filename, initial_data=None):
        self.filepath = os.path.join(DATA_DIR, filename)
        self.initial_data = list(initial_data or [])
        self._load()

    def _load(self):
        if os.path.exists(self.filepath):
            try:
                with open(self.filepath, 'r', encoding='utf-8') as f:
                    self.data = json.load(f)
                    return
            except Exception as e:
                logger.warning(f"Failed to load JSON file {self.filepath}: {e}")
        
        self.data = list(self.initial_data)
        self._save()

    def _save(self):
        try:
            with open(self.filepath, 'w', encoding='utf-8') as f:
                json.dump(self.data, f, indent=2, ensure_ascii=False)
        except Exception as e:
            logger.error(f"Failed to save JSON file {self.filepath}: {e}")

    def find(self, query=None):
        self._load()
        return list(self.data)

    def insert_one(self, doc):
        self._load()
        if "_id" not in doc:
            doc["_id"] = f"rec_{len(self.data) + 1}_{int(os.urandom(2).hex(), 16)}"
        self.data.append(doc)
        self._save()
        class InsertResult:
            def __init__(self, inserted_id):
                self.inserted_id = inserted_id
        return InsertResult(doc["_id"])

    def delete_one(self, query):
        self._load()
        target_id = str(query.get("_id"))
        initial_len = len(self.data)
        self.data = [doc for doc in self.data if str(doc.get("_id")) != target_id]
        deleted_count = initial_len - len(self.data)
        if deleted_count > 0:
            self._save()
        class DeleteResult:
            def __init__(self, count):
                self.deleted_count = count
        return DeleteResult(deleted_count)

    def update_one(self, query, update):
        self._load()
        target_id = str(query.get("_id"))
        set_fields = update.get("$set", {})
        modified_count = 0
        for doc in self.data:
            if str(doc.get("_id")) == target_id:
                doc.update(set_fields)
                modified_count = 1
                break
        if modified_count > 0:
            self._save()
        class UpdateResult:
            def __init__(self, count):
                self.modified_count = count
        return UpdateResult(modified_count)

class DatabaseManager:
    def __init__(self):
        self.client = None
        self.db = None
        self.is_connected = False
        self._init_db()

    def _init_db(self):
        try:
            self.client = MongoClient(MONGO_URI, serverSelectionTimeoutMS=2000)
            self.client.admin.command('ping')
            self.db = self.client[DB_NAME]
            self.is_connected = True
            logger.info("Successfully connected to MongoDB database.")

            # Seed MongoDB if doctors collection is empty
            if self.db["doctors"].count_documents({}) == 0:
                self.db["doctors"].insert_many(SEED_DOCTORS)
                logger.info("Seeded 50 doctors into MongoDB.")

        except (ConnectionFailure, ServerSelectionTimeoutError, Exception) as e:
            logger.warning(f"MongoDB connection failed ({e}). Falling back to persistent JSON storage.")
            self.is_connected = False
            self.db = {
                "patients": JSONCollection("patients.json", [
                    { "_id": "p1", "name": "Aarav Sharma", "age": 34, "gender": "Male", "blood_group": "A+", "contact": "+91 98765 43210", "condition": "Routine Checkup", "status": "Stable" },
                    { "_id": "p2", "name": "Priya Patel", "age": 28, "gender": "Female", "blood_group": "O+", "contact": "+91 98123 45678", "condition": "Hypertension", "status": "Monitoring" }
                ]),
                "doctors": JSONCollection("doctors.json", SEED_DOCTORS),
                "appointments": JSONCollection("appointments.json", [
                    { "_id": "a1", "patient_name": "Aarav Sharma", "doctor_name": "Dr. Vikram Sethi", "date": "2026-09-24", "time": "10:30 AM", "department": "Cardiology", "status": "Scheduled" }
                ])
            }

    def get_collection(self, name):
        if self.is_connected:
            return self.db[name]
        return self.db.get(name)

db_manager = DatabaseManager()

def get_patients_collection():
    return db_manager.get_collection("patients")

def get_doctors_collection():
    return db_manager.get_collection("doctors")

def get_appointments_collection():
    return db_manager.get_collection("appointments")
