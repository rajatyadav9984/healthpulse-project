/* ==========================================================================
   HEALTHPULSE CLIENT JAVASCRIPT
   API Gateway, Dynamic 50 Specialty Rendering, Modal & Event Controllers
   ========================================================================== */

const API_BASE_URL = 'http://127.0.0.1:5000';

let selectedTimeSlot = ''; // Global tracker for appointment slot choice

// Mock dataset fallback covering 3 doctors per department and weekly shifts
const MOCK_DATA = {
    patients: [
        { _id: 'p1', name: 'Aarav Sharma', age: 34, gender: 'Male', blood_group: 'A+', contact: '+91 98765 43210', condition: 'Routine Checkup', status: 'Stable' },
        { _id: 'p2', name: 'Priya Patel', age: 28, gender: 'Female', blood_group: 'O+', contact: '+91 98123 45678', condition: 'Hypertension', status: 'Monitoring' },
        { _id: 'p3', name: 'Rajesh Kumar', age: 52, gender: 'Male', blood_group: 'B+', contact: '+91 97890 12345', condition: 'Post Surgery', status: 'Recovering' }
    ],
    doctors: [
        {
            _id: "d1", name: "Dr. Vikram Sethi", specialization: "Cardiologist", department: "Cardiology",
            focus: "Heart & Cardiovascular / HRT", experience: "14 Yrs", room: "302", status: "Available",
            schedule: {
                "Monday": {"start": "10:00", "end": "12:30"}, "Tuesday": {"start": "10:00", "end": "12:30"},
                "Wednesday": {"start": "10:00", "end": "12:30"}, "Thursday": {"start": "10:00", "end": "12:30"},
                "Friday": {"start": "10:00", "end": "12:30"}, "Saturday": {"start": "10:00", "end": "12:30"},
                "Sunday": {"start": "10:00", "end": "13:00"}
            }
        },
        {
            _id: "d2", name: "Dr. Raj Malhotra", specialization: "Interventional Cardiologist", department: "Cardiology",
            focus: "Angioplasty & Heart Failure", experience: "16 Yrs", room: "304", status: "Available",
            schedule: {
                "Monday": {"start": "14:00", "end": "16:30"}, "Tuesday": {"start": "14:00", "end": "16:30"},
                "Wednesday": {"start": "14:00", "end": "16:30"}, "Thursday": {"start": "14:00", "end": "16:30"},
                "Friday": {"start": "14:00", "end": "16:30"}, "Saturday": {"start": "14:00", "end": "16:30"}, "Sunday": null
            }
        },
        {
            _id: "d3", name: "Dr. Ananya Sharma", specialization: "Electrophysiologist", department: "Cardiology",
            focus: "Heart Rhythm & Pacemaker", experience: "11 Yrs", room: "306", status: "Available",
            schedule: {
                "Monday": {"start": "17:00", "end": "19:30"}, "Tuesday": {"start": "17:00", "end": "19:30"},
                "Wednesday": {"start": "17:00", "end": "19:30"}, "Thursday": {"start": "17:00", "end": "19:30"},
                "Friday": {"start": "17:00", "end": "19:30"}, "Saturday": {"start": "17:00", "end": "19:30"}, "Sunday": null
            }
        },
        {
            _id: "d4", name: "Dr. Meera Kapoor", specialization: "Dermatologist", department: "Dermatology",
            focus: "Skin & Hair Care", experience: "9 Yrs", room: "205", status: "Available",
            schedule: {
                "Monday": {"start": "10:00", "end": "13:00"}, "Tuesday": {"start": "10:00", "end": "13:00"},
                "Wednesday": {"start": "10:00", "end": "13:00"}, "Thursday": null,
                "Friday": {"start": "10:00", "end": "13:00"}, "Saturday": {"start": "10:00", "end": "13:00"}, "Sunday": null
            }
        },
        {
            _id: "d5", name: "Dr. Priya Sharma", specialization: "Cosmetic Dermatologist", department: "Dermatology",
            focus: "Laser & Aesthetic Dermatology", experience: "12 Yrs", room: "207", status: "On Leave",
            schedule: {
                "Monday": null, "Tuesday": {"start": "14:00", "end": "18:00"},
                "Wednesday": null, "Thursday": {"start": "14:00", "end": "18:00"},
                "Friday": {"start": "14:00", "end": "18:00"}, "Saturday": {"start": "11:00", "end": "15:00"}, "Sunday": null
            }
        },
        {
            _id: "d6", name: "Dr. Amit Verma", specialization: "Pediatric Dermatologist", department: "Dermatology",
            focus: "Eczema & Skin Infections", experience: "10 Yrs", room: "209", status: "Available",
            schedule: {
                "Monday": {"start": "11:00", "end": "14:00"}, "Tuesday": {"start": "11:00", "end": "14:00"},
                "Wednesday": {"start": "11:00", "end": "14:00"}, "Thursday": {"start": "11:00", "end": "14:00"},
                "Friday": null, "Saturday": null, "Sunday": null
            }
        },
        {
            _id: "d7", name: "Dr. Sunita Mehta", specialization: "Neurologist", department: "Neurology",
            focus: "Brain & Nerves", experience: "12 Yrs", room: "415", status: "In Surgery",
            schedule: {
                "Monday": {"start": "10:00", "end": "13:00"}, "Tuesday": {"start": "10:00", "end": "13:00"},
                "Wednesday": null, "Thursday": {"start": "10:00", "end": "13:00"},
                "Friday": {"start": "10:00", "end": "13:00"}, "Saturday": {"start": "10:00", "end": "12:00"}, "Sunday": null
            }
        },
        {
            _id: "d8", name: "Dr. Rahul Singh", specialization: "Stroke Specialist", department: "Neurology",
            focus: "Stroke & Epilepsy Care", experience: "15 Yrs", room: "417", status: "Available",
            schedule: {
                "Monday": {"start": "14:00", "end": "17:00"}, "Tuesday": {"start": "14:00", "end": "17:00"},
                "Wednesday": {"start": "14:00", "end": "17:00"}, "Thursday": null,
                "Friday": {"start": "14:00", "end": "17:00"}, "Saturday": null, "Sunday": null
            }
        },
        {
            _id: "d9", name: "Dr. Arjun Gupta", specialization: "Neuro-Physiologist", department: "Neurology",
            focus: "Nerve Conduction & EEG", experience: "8 Yrs", room: "419", status: "On Leave",
            schedule: {
                "Monday": null, "Tuesday": {"start": "09:00", "end": "12:00"},
                "Wednesday": null, "Thursday": {"start": "09:00", "end": "12:00"},
                "Friday": null, "Saturday": {"start": "09:00", "end": "13:00"}, "Sunday": null
            }
        },
        {
            _id: "d10", name: "Dr. Rohan Deshmukh", specialization: "Orthopedic Specialist", department: "Orthopedics",
            focus: "Bones, Joints & Muscles", experience: "10 Yrs", room: "108", status: "Available",
            schedule: {
                "Monday": {"start": "10:00", "end": "13:00"}, "Tuesday": {"start": "10:00", "end": "13:00"},
                "Wednesday": {"start": "10:00", "end": "13:00"}, "Thursday": {"start": "10:00", "end": "13:00"},
                "Friday": {"start": "10:00", "end": "13:00"}, "Saturday": null,
                "Sunday": {"start": "10:00", "end": "13:00"}
            }
        },
        {
            _id: "d11", name: "Dr. Varun Tej", specialization: "Spine & Joint Replacement", department: "Orthopedics",
            focus: "Knee Replacement & Spine Surgery", experience: "15 Yrs", room: "110", status: "Available",
            schedule: {
                "Monday": null, "Tuesday": {"start": "14:00", "end": "18:00"},
                "Wednesday": null, "Thursday": {"start": "14:00", "end": "18:00"},
                "Friday": {"start": "14:00", "end": "18:00"}, "Saturday": {"start": "10:00", "end": "14:00"}, "Sunday": null
            }
        },
        {
            _id: "d12", name: "Dr. Siddharth Kaul", specialization: "Sports Medicine Specialist", department: "Orthopedics",
            focus: "Ligament Tear & Sports Rehab", experience: "9 Yrs", room: "106", status: "On Leave",
            schedule: {
                "Monday": {"start": "15:00", "end": "19:00"}, "Tuesday": null,
                "Wednesday": {"start": "15:00", "end": "19:00"}, "Thursday": null,
                "Friday": {"start": "15:00", "end": "19:00"}, "Saturday": {"start": "10:00", "end": "13:00"}, "Sunday": null
            }
        },
        {
            _id: "d13", name: "Dr. Neha Gupta", specialization: "Pediatrician", department: "Pediatrics",
            focus: "Child Healthcare & Vaccination", experience: "11 Yrs", room: "204", status: "Available",
            schedule: {
                "Monday": {"start": "09:00", "end": "13:00"}, "Tuesday": {"start": "09:00", "end": "13:00"},
                "Wednesday": {"start": "09:00", "end": "13:00"}, "Thursday": {"start": "09:00", "end": "13:00"},
                "Friday": {"start": "09:00", "end": "13:00"}, "Saturday": null,
                "Sunday": {"start": "10:00", "end": "12:30"}
            }
        },
        {
            _id: "d14", name: "Dr. Ajay Rastogi", specialization: "Pediatric Surgeon", department: "Pediatrics",
            focus: "Children's Surgical Care", experience: "12 Yrs", room: "OR-4", status: "In Surgery",
            schedule: {
                "Monday": null, "Tuesday": {"start": "14:00", "end": "17:00"},
                "Wednesday": {"start": "14:00", "end": "17:00"}, "Thursday": null,
                "Friday": {"start": "14:00", "end": "17:00"}, "Saturday": {"start": "10:00", "end": "13:00"}, "Sunday": null
            }
        },
        {
            _id: "d15", name: "Dr. Ritu Verma", specialization: "Neonatologist", department: "Pediatrics",
            focus: "Newborn & ICU Care", experience: "10 Yrs", room: "206", status: "Available",
            schedule: {
                "Monday": {"start": "15:00", "end": "18:00"}, "Tuesday": {"start": "15:00", "end": "18:00"},
                "Wednesday": null, "Thursday": {"start": "15:00", "end": "18:00"},
                "Friday": {"start": "15:00", "end": "18:00"}, "Saturday": null, "Sunday": null
            }
        },
        {
            _id: "d16", name: "Dr. Arvind Swamy", specialization: "Ophthalmologist", department: "Ophthalmology",
            focus: "Eyes & Vision Care", experience: "13 Yrs", room: "309", status: "Available",
            schedule: {
                "Monday": {"start": "10:00", "end": "13:00"}, "Tuesday": {"start": "10:00", "end": "13:00"},
                "Wednesday": null, "Thursday": {"start": "10:00", "end": "13:00"},
                "Friday": {"start": "10:00", "end": "13:00"}, "Saturday": {"start": "10:00", "end": "12:00"}, "Sunday": null
            }
        },
        {
            _id: "d17", name: "Dr. Abhinav Reddy", specialization: "Retina Specialist", department: "Ophthalmology",
            focus: "Retina & Laser Surgery", experience: "12 Yrs", room: "310", status: "On Leave",
            schedule: {
                "Monday": null, "Tuesday": {"start": "14:00", "end": "17:00"},
                "Wednesday": {"start": "10:00", "end": "13:00"}, "Thursday": null,
                "Friday": {"start": "14:00", "end": "17:00"}, "Saturday": {"start": "10:00", "end": "13:00"}, "Sunday": null
            }
        },
        {
            _id: "d18", name: "Dr. Kunal Singhal", specialization: "Cataract Surgeon", department: "Ophthalmology",
            focus: "Cataract & LASIK Surgery", experience: "15 Yrs", room: "OR-5", status: "Available",
            schedule: {
                "Monday": {"start": "14:00", "end": "18:00"}, "Tuesday": null,
                "Wednesday": {"start": "14:00", "end": "18:00"}, "Thursday": {"start": "14:00", "end": "18:00"},
                "Friday": null, "Saturday": null, "Sunday": null
            }
        },
        {
            _id: "d19", name: "Dr. Pooja Singhania", specialization: "Dentist", department: "Dentistry",
            focus: "Teeth & Dental Health", experience: "8 Yrs", room: "112", status: "Available",
            schedule: {
                "Monday": {"start": "10:00", "end": "14:00"}, "Tuesday": {"start": "10:00", "end": "14:00"},
                "Wednesday": {"start": "10:00", "end": "14:00"}, "Thursday": null,
                "Friday": {"start": "10:00", "end": "14:00"}, "Saturday": {"start": "10:00", "end": "13:00"}, "Sunday": null
            }
        },
        {
            _id: "d20", name: "Dr. Farhan Qureshi", specialization: "Maxillofacial Surgeon", department: "Dentistry",
            focus: "Jaw Surgery & Dental Implants", experience: "13 Yrs", room: "114", status: "On Leave",
            schedule: {
                "Monday": null, "Tuesday": {"start": "15:00", "end": "19:00"},
                "Wednesday": null, "Thursday": {"start": "15:00", "end": "19:00"},
                "Friday": {"start": "15:00", "end": "19:00"}, "Saturday": null, "Sunday": null
            }
        },
        {
            _id: "d21", name: "Dr. Tanya Mittal", specialization: "Orthodontist", department: "Dentistry",
            focus: "Braces & Teeth Alignment", experience: "7 Yrs", room: "113", status: "Available",
            schedule: {
                "Monday": {"start": "14:00", "end": "17:00"}, "Tuesday": null,
                "Wednesday": {"start": "14:00", "end": "17:00"}, "Thursday": null,
                "Friday": {"start": "14:00", "end": "17:00"}, "Saturday": {"start": "11:00", "end": "14:00"}, "Sunday": null
            }
        },
        {
            _id: "d22", name: "Dr. Alok Verma", specialization: "ENT Specialist", department: "ENT",
            focus: "Ear, Nose & Throat Care", experience: "14 Yrs", room: "218", status: "Available",
            schedule: {
                "Monday": {"start": "10:00", "end": "13:00"}, "Tuesday": {"start": "10:00", "end": "13:00"},
                "Wednesday": null, "Thursday": {"start": "10:00", "end": "13:00"},
                "Friday": {"start": "10:00", "end": "13:00"}, "Saturday": {"start": "10:00", "end": "12:00"}, "Sunday": null
            }
        },
        {
            _id: "d23", name: "Dr. Shrikant Shinde", specialization: "Rhinologist", department: "ENT",
            focus: "Nose & Sinus Surgery", experience: "10 Yrs", room: "219", status: "Available",
            schedule: {
                "Monday": null, "Tuesday": {"start": "14:00", "end": "17:00"},
                "Wednesday": {"start": "10:00", "end": "13:00"}, "Thursday": null,
                "Friday": {"start": "14:00", "end": "17:00"}, "Saturday": {"start": "10:00", "end": "13:00"}, "Sunday": null
            }
        },
        {
            _id: "d24", name: "Dr. Radhika Sen", specialization: "Otologist", department: "ENT",
            focus: "Ear & Hearing Disorders", experience: "11 Yrs", room: "220", status: "On Leave",
            schedule: {
                "Monday": {"start": "14:00", "end": "17:00"}, "Tuesday": null,
                "Wednesday": {"start": "14:00", "end": "17:00"}, "Thursday": {"start": "14:00", "end": "17:00"},
                "Friday": null, "Saturday": null, "Sunday": null
            }
        },
        {
            _id: "d25", name: "Dr. Karan Thapar", specialization: "Emergency Medicine Lead", department: "Emergency",
            focus: "Trauma & ER Command Center", experience: "12 Yrs", room: "ER-1", status: "Available",
            schedule: {
                "Monday": {"start": "08:00", "end": "20:00"}, "Tuesday": {"start": "08:00", "end": "20:00"},
                "Wednesday": {"start": "08:00", "end": "20:00"}, "Thursday": {"start": "08:00", "end": "20:00"},
                "Friday": {"start": "08:00", "end": "20:00"}, "Saturday": {"start": "08:00", "end": "20:00"},
                "Sunday": {"start": "08:00", "end": "20:00"}
            }
        },
        {
            _id: "d26", name: "Dr. Vandana Tripathi", specialization: "Critical Care Specialist", department: "Emergency",
            focus: "ICU & Ventilator Management", experience: "15 Yrs", room: "ICU-3", status: "Available",
            schedule: {
                "Monday": {"start": "10:00", "end": "18:00"}, "Tuesday": {"start": "10:00", "end": "18:00"},
                "Wednesday": {"start": "10:00", "end": "18:00"}, "Thursday": {"start": "10:00", "end": "18:00"},
                "Friday": {"start": "10:00", "end": "18:00"}, "Saturday": {"start": "10:00", "end": "14:00"},
                "Sunday": {"start": "10:00", "end": "16:00"}
            }
        },
        {
            _id: "d27", name: "Dr. Suresh Nambiar", specialization: "Pulmonologist", department: "Pulmonology",
            focus: "Asthma, COPD & Lung Care", experience: "14 Yrs", room: "312", status: "Available",
            schedule: {
                "Monday": {"start": "10:00", "end": "13:00"}, "Tuesday": {"start": "10:00", "end": "13:00"},
                "Wednesday": {"start": "10:00", "end": "13:00"}, "Thursday": {"start": "10:00", "end": "13:00"},
                "Friday": {"start": "10:00", "end": "13:00"}, "Saturday": {"start": "10:00", "end": "12:00"}, "Sunday": null
            }
        },
        {
            _id: "d28", name: "Dr. Kavita Pillai", specialization: "Sleep Medicine Specialist", department: "Pulmonology",
            focus: "Sleep Apnea & Respiratory Rehab", experience: "9 Yrs", room: "314", status: "Available",
            schedule: {
                "Monday": null, "Tuesday": {"start": "14:00", "end": "17:00"},
                "Wednesday": null, "Thursday": {"start": "14:00", "end": "17:00"},
                "Friday": {"start": "14:00", "end": "17:00"}, "Saturday": null, "Sunday": null
            }
        },
        {
            _id: "d29", name: "Dr. Manish Saxena", specialization: "Interventional Pulmonologist", department: "Pulmonology",
            focus: "Bronchoscopy & Pleural Diseases", experience: "11 Yrs", room: "316", status: "In Surgery",
            schedule: {
                "Monday": {"start": "15:00", "end": "18:00"}, "Tuesday": null,
                "Wednesday": {"start": "15:00", "end": "18:00"}, "Thursday": null,
                "Friday": {"start": "15:00", "end": "18:00"}, "Saturday": null, "Sunday": null
            }
        },
        {
            _id: "d30", name: "Dr. Sameer Joshi", specialization: "Gastroenterologist", department: "Gastroenterology",
            focus: "Endoscopy & Gut Health", experience: "13 Yrs", room: "222", status: "Available",
            schedule: {
                "Monday": {"start": "10:00", "end": "13:00"}, "Tuesday": {"start": "10:00", "end": "13:00"},
                "Wednesday": {"start": "10:00", "end": "13:00"}, "Thursday": {"start": "10:00", "end": "13:00"},
                "Friday": {"start": "10:00", "end": "13:00"}, "Saturday": null, "Sunday": null
            }
        },
        {
            _id: "d31", name: "Dr. Shalini Roy", specialization: "Hepatologist", department: "Gastroenterology",
            focus: "Liver Cirrhosis & Fatty Liver", experience: "16 Yrs", room: "224", status: "Available",
            schedule: {
                "Monday": null, "Tuesday": {"start": "14:00", "end": "17:00"},
                "Wednesday": null, "Thursday": {"start": "14:00", "end": "17:00"},
                "Friday": {"start": "14:00", "end": "17:00"}, "Saturday": {"start": "10:00", "end": "13:00"}, "Sunday": null
            }
        },
        {
            _id: "d32", name: "Dr. Harish Bhasin", specialization: "GI Endoscopist", department: "Gastroenterology",
            focus: "Colonoscopy & Ulcer Management", experience: "10 Yrs", room: "226", status: "On Leave",
            schedule: {
                "Monday": {"start": "14:00", "end": "17:00"}, "Tuesday": null,
                "Wednesday": {"start": "14:00", "end": "17:00"}, "Thursday": null, "Friday": null, "Saturday": null, "Sunday": null
            }
        },
        {
            _id: "d33", name: "Dr. Vivek Anand", specialization: "Nephrologist", department: "Nephrology",
            focus: "Kidney Care & Dialysis", experience: "15 Yrs", room: "402", status: "Available",
            schedule: {
                "Monday": {"start": "10:00", "end": "13:00"}, "Tuesday": {"start": "10:00", "end": "13:00"},
                "Wednesday": {"start": "10:00", "end": "13:00"}, "Thursday": {"start": "10:00", "end": "13:00"},
                "Friday": {"start": "10:00", "end": "13:00"}, "Saturday": {"start": "10:00", "end": "12:00"}, "Sunday": null
            }
        },
        {
            _id: "d34", name: "Dr. Geeta Kulkarni", specialization: "Transplant Nephrologist", department: "Nephrology",
            focus: "Renal Transplant & Chronic Kidney Disease", experience: "12 Yrs", room: "404", status: "Available",
            schedule: {
                "Monday": null, "Tuesday": {"start": "14:00", "end": "17:00"},
                "Wednesday": {"start": "14:00", "end": "17:00"}, "Thursday": null, "Friday": {"start": "14:00", "end": "17:00"}, "Saturday": null, "Sunday": null
            }
        },
        {
            _id: "d35", name: "Dr. Deepak Dave", specialization: "Dialysis Specialist", department: "Nephrology",
            focus: "Hemodialysis & Kidney Failure", experience: "8 Yrs", room: "406", status: "Available",
            schedule: {
                "Monday": {"start": "15:00", "end": "19:00"}, "Tuesday": {"start": "15:00", "end": "19:00"},
                "Wednesday": null, "Thursday": {"start": "15:00", "end": "19:00"}, "Friday": {"start": "15:00", "end": "19:00"}, "Saturday": null, "Sunday": null
            }
        },
        {
            _id: "d36", name: "Dr. Pankaj Mishra", specialization: "Urologist", department: "Urology",
            focus: "Kidney Stones & Prostate Care", experience: "14 Yrs", room: "408", status: "Available",
            schedule: {
                "Monday": {"start": "10:00", "end": "13:00"}, "Tuesday": {"start": "10:00", "end": "13:00"},
                "Wednesday": {"start": "10:00", "end": "13:00"}, "Thursday": {"start": "10:00", "end": "13:00"},
                "Friday": {"start": "10:00", "end": "13:00"}, "Saturday": null, "Sunday": null
            }
        },
        {
            _id: "d37", name: "Dr. Nikhil Bajaj", specialization: "Andrologist & Robotic Urologist", department: "Urology",
            focus: "Robotic Surgery & Men's Health", experience: "11 Yrs", room: "410", status: "In Surgery",
            schedule: {
                "Monday": null, "Tuesday": {"start": "14:00", "end": "18:00"},
                "Wednesday": null, "Thursday": {"start": "14:00", "end": "18:00"},
                "Friday": {"start": "14:00", "end": "18:00"}, "Saturday": {"start": "10:00", "end": "13:00"}, "Sunday": null
            }
        },
        {
            _id: "d38", name: "Dr. Tarun Nanda", specialization: "Endourologist", department: "Urology",
            focus: "Laser Lithotripsy & Urinary Tract", experience: "9 Yrs", room: "412", status: "On Leave",
            schedule: {
                "Monday": {"start": "14:00", "end": "17:00"}, "Tuesday": null,
                "Wednesday": {"start": "14:00", "end": "17:00"}, "Thursday": null, "Friday": null, "Saturday": null, "Sunday": null
            }
        },
        {
            _id: "d39", name: "Dr. Rashmi Hegde", specialization: "Medical Oncologist", department: "Oncology",
            focus: "Chemotherapy & Tumour Care", experience: "16 Yrs", room: "502", status: "Available",
            schedule: {
                "Monday": {"start": "10:00", "end": "13:00"}, "Tuesday": {"start": "10:00", "end": "13:00"},
                "Wednesday": {"start": "10:00", "end": "13:00"}, "Thursday": {"start": "10:00", "end": "13:00"},
                "Friday": {"start": "10:00", "end": "13:00"}, "Saturday": {"start": "10:00", "end": "12:00"}, "Sunday": null
            }
        },
        {
            _id: "d40", name: "Dr. Ashok Chawla", specialization: "Surgical Oncologist", department: "Oncology",
            focus: "Cancer Surgery & Tumour Resection", experience: "18 Yrs", room: "OR-2", status: "In Surgery",
            schedule: {
                "Monday": null, "Tuesday": {"start": "14:00", "end": "17:00"},
                "Wednesday": {"start": "14:00", "end": "17:00"}, "Thursday": null, "Friday": {"start": "14:00", "end": "17:00"}, "Saturday": null, "Sunday": null
            }
        },
        {
            _id: "d41", name: "Dr. Swati Deshmukh", specialization: "Radiation Oncologist", department: "Oncology",
            focus: "Radiotherapy & Target Therapy", experience: "10 Yrs", room: "504", status: "Available",
            schedule: {
                "Monday": {"start": "14:00", "end": "18:00"}, "Tuesday": null,
                "Wednesday": {"start": "14:00", "end": "18:00"}, "Thursday": {"start": "14:00", "end": "18:00"}, "Friday": null, "Saturday": null, "Sunday": null
            }
        },
        {
            _id: "d42", name: "Dr. Naresh Trehan", specialization: "Endocrinologist", department: "Endocrinology",
            focus: "Diabetes & Thyroid Disorder", experience: "15 Yrs", room: "318", status: "Available",
            schedule: {
                "Monday": {"start": "10:00", "end": "13:00"}, "Tuesday": {"start": "10:00", "end": "13:00"},
                "Wednesday": {"start": "10:00", "end": "13:00"}, "Thursday": {"start": "10:00", "end": "13:00"},
                "Friday": {"start": "10:00", "end": "13:00"}, "Saturday": {"start": "10:00", "end": "13:00"}, "Sunday": null
            }
        },
        {
            _id: "d43", name: "Dr. Sunayana Sen", specialization: "Diabetologist", department: "Endocrinology",
            focus: "Type-1 & Type-2 Diabetes Care", experience: "9 Yrs", room: "320", status: "Available",
            schedule: {
                "Monday": null, "Tuesday": {"start": "14:00", "end": "17:00"},
                "Wednesday": null, "Thursday": {"start": "14:00", "end": "17:00"}, "Friday": {"start": "14:00", "end": "17:00"}, "Saturday": null, "Sunday": null
            }
        },
        {
            _id: "d44", name: "Dr. Kabir Bedi", specialization: "Psychiatrist", department: "Psychiatry",
            focus: "Anxiety, Depression & Mental Wellness", experience: "13 Yrs", room: "510", status: "Available",
            schedule: {
                "Monday": {"start": "11:00", "end": "15:00"}, "Tuesday": {"start": "11:00", "end": "15:00"},
                "Wednesday": {"start": "11:00", "end": "15:00"}, "Thursday": {"start": "11:00", "end": "15:00"},
                "Friday": {"start": "11:00", "end": "15:00"}, "Saturday": null, "Sunday": null
            }
        },
        {
            _id: "d45", name: "Dr. Smita Patil", specialization: "Clinical Psychologist", department: "Psychiatry",
            focus: "Cognitive Behavior & Counseling", experience: "8 Yrs", room: "512", status: "On Leave",
            schedule: {
                "Monday": null, "Tuesday": {"start": "14:00", "end": "18:00"},
                "Wednesday": null, "Thursday": {"start": "14:00", "end": "18:00"},
                "Friday": {"start": "14:00", "end": "18:00"}, "Saturday": {"start": "10:00", "end": "13:00"}, "Sunday": null
            }
        },
        {
            _id: "d46", name: "Dr. Balram Bhargava", specialization: "General Surgeon", department: "General Surgery",
            focus: "Hernia, Gallbladder & Laparoscopy", experience: "17 Yrs", room: "OR-1", status: "Available",
            schedule: {
                "Monday": {"start": "10:00", "end": "13:00"}, "Tuesday": {"start": "10:00", "end": "13:00"},
                "Wednesday": {"start": "10:00", "end": "13:00"}, "Thursday": {"start": "10:00", "end": "13:00"},
                "Friday": {"start": "10:00", "end": "13:00"}, "Saturday": {"start": "10:00", "end": "12:00"}, "Sunday": null
            }
        },
        {
            _id: "d47", name: "Dr. Vinod Paul", specialization: "Laparoscopic Surgeon", department: "General Surgery",
            focus: "Minimally Invasive Surgery", experience: "14 Yrs", room: "OR-3", status: "In Surgery",
            schedule: {
                "Monday": null, "Tuesday": {"start": "14:00", "end": "17:00"},
                "Wednesday": {"start": "14:00", "end": "17:00"}, "Thursday": null, "Friday": {"start": "14:00", "end": "17:00"}, "Saturday": null, "Sunday": null
            }
        },
        {
            _id: "d48", name: "Dr. Anuj Bhatia", specialization: "Trauma Surgeon", department: "General Surgery",
            focus: "Emergency & Acute Surgical Care", experience: "11 Yrs", room: "OR-6", status: "Available",
            schedule: {
                "Monday": {"start": "15:00", "end": "19:00"}, "Tuesday": null,
                "Wednesday": {"start": "15:00", "end": "19:00"}, "Thursday": null, "Friday": {"start": "15:00", "end": "19:00"}, "Saturday": null, "Sunday": null
            }
        },
        {
            _id: "d49", name: "Dr. Randeep Guleria", specialization: "Internal Medicine Lead", department: "General Medicine",
            focus: "Chronic Fever, Diabetes & Hypertension", experience: "20 Yrs", room: "101", status: "Available",
            schedule: {
                "Monday": {"start": "09:00", "end": "13:00"}, "Tuesday": {"start": "09:00", "end": "13:00"},
                "Wednesday": {"start": "09:00", "end": "13:00"}, "Thursday": {"start": "09:00", "end": "13:00"},
                "Friday": {"start": "09:00", "end": "13:00"}, "Saturday": {"start": "09:00", "end": "13:00"}, "Sunday": null
            }
        },
        {
            _id: "d50", name: "Dr. Soumya Swaminathan", specialization: "General Physician", department: "General Medicine",
            focus: "Preventive Care & Infectious Diseases", experience: "18 Yrs", room: "103", status: "Available",
            schedule: {
                "Monday": {"start": "14:00", "end": "18:00"}, "Tuesday": {"start": "14:00", "end": "18:00"},
                "Wednesday": {"start": "14:00", "end": "18:00"}, "Thursday": {"start": "14:00", "end": "18:00"},
                "Friday": {"start": "14:00", "end": "18:00"}, "Saturday": null, "Sunday": null
            }
        }
    ],
    appointments: [
        { _id: 'a1', patient_name: 'Aarav Sharma', doctor_name: 'Dr. Vikram Sethi', date: '2026-09-24', time: '10:30 AM', department: 'Cardiology', status: 'Scheduled' }
    ]
};

// Specialty Emoji Mapping Helper
function getSpecialtyEmoji(spec) {
    const s = (spec || '').toLowerCase();
    if (s.includes('cardio') || s.includes('heart')) return '🫀';
    if (s.includes('derma') || s.includes('skin')) return '🧴';
    if (s.includes('neuro') || s.includes('brain') || s.includes('psychiatry')) return '🧠';
    if (s.includes('ortho') || s.includes('bone') || s.includes('rheuma') || s.includes('spine')) return '🦴';
    if (s.includes('pedia') || s.includes('child')) return '👶';
    if (s.includes('ophthalm') || s.includes('eye') || s.includes('retina')) return '👁️';
    if (s.includes('dent') || s.includes('oral') || s.includes('orthodont') || s.includes('periodont')) return '🦷';
    if (s.includes('ent') || s.includes('rhino') || s.includes('oto')) return '👂';
    if (s.includes('pulmono') || s.includes('lung') || s.includes('sleep')) return '🫁';
    if (s.includes('emerg') || s.includes('critical') || s.includes('icu')) return '🚑';
    return '🩺';
}

// Initialize Application State
document.addEventListener('DOMContentLoaded', () => {
    checkHealthStatus();
    initCurrentPage();
    populateDepartmentDropdown();
});

// Check Flask API Server Status
async function checkHealthStatus() {
    const statusPill = document.getElementById('healthStatusPill');
    if (!statusPill) return;

    try {
        const response = await fetchWithTimeout(`${API_BASE_URL}/health`, { method: 'GET' }, 1500);
        if (response.ok) {
            const data = await response.json();
            statusPill.innerHTML = `<span class="status-dot"></span> API ${data.status.toUpperCase()}`;
            statusPill.style.color = '#10b981';
            statusPill.style.borderColor = 'rgba(16, 185, 129, 0.3)';
        } else {
            throw new Error('API server returned non-200');
        }
    } catch (err) {
        statusPill.innerHTML = `<span class="status-dot" style="background: #f59e0b; box-shadow: 0 0 8px #f59e0b;"></span> DEMO MODE (Offline API)`;
        statusPill.style.color = '#f59e0b';
        statusPill.style.borderColor = 'rgba(245, 158, 11, 0.3)';
    }
}

// Router for Page Initialization
function initCurrentPage() {
    const page = document.body.dataset.page;
    if (page === 'dashboard') {
        loadDashboardMetrics();
        loadRecentActivity();
    } else if (page === 'patients') {
        loadPatientsTable();
    } else if (page === 'doctors') {
        loadDoctorsGrid();
    } else if (page === 'appointments') {
        loadAppointmentsTable();
    }
}

/* ==========================================================================
   API FETCH HELPERS WITH MOCK FALLBACKS
   ========================================================================== */
async function fetchWithTimeout(url, options = {}, timeoutMs = 1500) {
    const controller = new AbortController();
    const id = setTimeout(() => controller.abort(), timeoutMs);
    try {
        const response = await fetch(url, { ...options, signal: controller.signal });
        clearTimeout(id);
        return response;
    } catch (err) {
        clearTimeout(id);
        throw err;
    }
}

async function fetchPatientsData() {
    try {
        const res = await fetchWithTimeout(`${API_BASE_URL}/api/patients?t=${Date.now()}`);
        if (!res.ok) throw new Error();
        return await res.json();
    } catch {
        return MOCK_DATA.patients;
    }
}

async function fetchDoctorsData() {
    try {
        const res = await fetchWithTimeout(`${API_BASE_URL}/api/doctors?t=${Date.now()}`);
        if (!res.ok) throw new Error();
        return await res.json();
    } catch {
        return MOCK_DATA.doctors;
    }
}

async function fetchAppointmentsData() {
    try {
        const res = await fetchWithTimeout(`${API_BASE_URL}/api/appointments?t=${Date.now()}`);
        if (!res.ok) throw new Error();
        return await res.json();
    } catch {
        return MOCK_DATA.appointments;
    }
}

/* ==========================================================================
   DASHBOARD LOADERS
   ========================================================================== */
async function loadDashboardMetrics() {
    const patients = await fetchPatientsData();
    const doctors = await fetchDoctorsData();
    const appointments = await fetchAppointmentsData();

    const availableDocsCount = doctors.filter(d => d.status === 'Available').length;

    const elemPatients = document.getElementById('statTotalPatients');
    const elemDoctors = document.getElementById('statActiveDoctors');
    const elemAppointments = document.getElementById('statTodayAppointments');

    if (elemPatients) elemPatients.textContent = patients.length;
    if (elemDoctors) elemDoctors.textContent = `${availableDocsCount} / ${doctors.length}`;
    if (elemAppointments) elemAppointments.textContent = appointments.length;
}

async function loadRecentActivity() {
    const tableBody = document.getElementById('recentActivityBody');
    if (!tableBody) return;

    const appointments = await fetchAppointmentsData();
    if (!appointments || appointments.length === 0) {
        tableBody.innerHTML = `<tr><td colspan="5" style="text-align: center; color: var(--text-muted); padding: 2rem;">No recent appointments</td></tr>`;
        return;
    }

    // Display newest entries at the TOP of the queue
    const newestApts = [...appointments].reverse().slice(0, 5);

    tableBody.innerHTML = newestApts.map(apt => {
        let badgeClass = 'badge-info';
        if (apt.status === 'Completed') badgeClass = 'badge-success';
        if (apt.status === 'Cancelled') badgeClass = 'badge-cancelled';

        return `
            <tr>
                <td style="font-weight: 600;">${apt.patient_name}</td>
                <td style="color: var(--primary);">${apt.doctor_name}</td>
                <td><span class="badge badge-info">${apt.department || 'General'}</span></td>
                <td>${apt.date} at ${apt.time}</td>
                <td><span class="badge ${badgeClass}">${apt.status}</span></td>
            </tr>
        `;
    }).join('');
}

/* ==========================================================================
   PATIENTS PAGE LOADERS
   ========================================================================== */
async function loadPatientsTable(searchTerm = '') {
    const tableBody = document.getElementById('patientsTableBody');
    if (!tableBody) return;

    let patients = await fetchPatientsData();
    if (searchTerm) {
        patients = patients.filter(p => 
            p.name.toLowerCase().includes(searchTerm.toLowerCase()) ||
            p.condition.toLowerCase().includes(searchTerm.toLowerCase())
        );
    }

    if (patients.length === 0) {
        tableBody.innerHTML = `<tr><td colspan="7" style="text-align: center; color: var(--text-muted); padding: 2rem;">No patient records found</td></tr>`;
        return;
    }

    // Newest registered patients at TOP
    const newestPatients = [...patients].reverse();

    tableBody.innerHTML = newestPatients.map(p => {
        let badgeClass = 'badge-success';
        if (p.status === 'Monitoring' || p.status === 'Under Observation') badgeClass = 'badge-warning';
        if (p.status === 'Critical') badgeClass = 'badge-danger';
        if (p.status === 'Discharged' || p.status === 'Recovered') badgeClass = 'badge-info';

        return `
            <tr>
                <td style="font-weight: 600;">${p.name}</td>
                <td>${p.age} yrs / ${p.gender}</td>
                <td><span class="badge badge-info">${p.blood_group}</span></td>
                <td>${p.contact}</td>
                <td>${p.condition}</td>
                <td><span class="badge ${badgeClass}">${p.status || 'Stable'}</span></td>
                <td>
                    <div style="display: flex; gap: 0.4rem; align-items: center; flex-wrap: wrap;">
                        ${p.status !== 'Discharged' ? `<button class="btn btn-secondary btn-sm" onclick="updatePatientStatus('${p._id}', 'Discharged')">✓ Discharge</button>` : `<button class="btn btn-secondary btn-sm" onclick="updatePatientStatus('${p._id}', 'Stable')">🔄 Re-admit</button>`}
                        <button class="btn btn-danger btn-sm" onclick="deletePatient('${p._id}')" title="Delete Patient Record">🗑️</button>
                    </div>
                </td>
            </tr>
        `;
    }).join('');
}

async function updatePatientStatus(patientId, newStatus) {
    try {
        const res = await fetch(`${API_BASE_URL}/api/patients/${patientId}`, {
            method: 'PUT',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ status: newStatus })
        });
        if (!res.ok) throw new Error();
        showToast(`Patient status updated to ${newStatus}`, 'success');
    } catch {
        let p = MOCK_DATA.patients.find(pt => String(pt._id) === String(patientId));
        if (p) p.status = newStatus;
        showToast(`Patient status set to ${newStatus}`, 'info');
    }

    if (document.body.dataset.page === 'patients') {
        loadPatientsTable();
    } else if (document.body.dataset.page === 'dashboard') {
        loadDashboardMetrics();
    }
}

async function deletePatient(patientId) {
    if (!confirm('Are you sure you want to delete this patient record?')) {
        return;
    }

    try {
        const res = await fetch(`${API_BASE_URL}/api/patients/${patientId}`, {
            method: 'DELETE'
        });
        if (!res.ok) throw new Error();
        showToast('Patient record deleted successfully!', 'success');
    } catch {
        showToast('Patient record deleted!', 'info');
    }

    MOCK_DATA.patients = MOCK_DATA.patients.filter(p => String(p._id) !== String(patientId));

    if (document.body.dataset.page === 'patients') {
        loadPatientsTable();
    } else if (document.body.dataset.page === 'dashboard') {
        loadDashboardMetrics();
    }
}

function filterPatients() {
    const input = document.getElementById('patientSearchInput');
    if (input) loadPatientsTable(input.value);
}

/* ==========================================================================
   DOCTORS PAGE LOADERS
   ========================================================================== */
async function loadDoctorsGrid() {
    const grid = document.getElementById('doctorsGrid');
    if (!grid) return;

    const doctors = await fetchDoctorsData();
    const availableDocsCount = doctors.filter(d => d.status === 'Available').length;

    const badge = document.getElementById('doctorsCountBadge');
    if (badge) badge.textContent = `🟢 ${availableDocsCount} Available / Total ${doctors.length} Specialists`;

    renderDoctorsList(doctors);
}

function renderDoctorsList(doctors) {
    const grid = document.getElementById('doctorsGrid');
    if (!grid) return;

    if (doctors.length === 0) {
        grid.innerHTML = `<div style="grid-column: 1/-1; text-align: center; color: var(--text-muted); padding: 3rem;">No doctors found matching search criteria.</div>`;
        return;
    }

    grid.innerHTML = doctors.map(d => {
        let badgeClass = 'badge-success';
        let statusText = '🟢 Available On-Duty';
        if (d.status === 'In Surgery') { badgeClass = 'badge-warning'; statusText = '🟡 In Surgery'; }
        if (d.status === 'On Leave') { badgeClass = 'badge-danger'; statusText = '🔴 Absent / On Leave'; }

        const emoji = getSpecialtyEmoji(d.specialization);
        const focusText = d.focus ? `<div style="font-size: 0.78rem; color: var(--text-dim); margin-top: 0.2rem;">${d.focus}</div>` : '';

        return `
            <div class="doctor-card">
                <div class="doctor-avatar">${emoji}</div>
                <h3 class="doctor-name">${d.name}</h3>
                <div class="doctor-spec">${d.specialization}</div>
                ${focusText}
                <div class="doctor-details" style="margin-top: 0.75rem;">
                    <span>Dept: <strong>${d.department}</strong></span>
                    <span>Experience: <strong>${d.experience}</strong></span>
                    <span>Room: <strong>${d.room}</strong></span>
                </div>
                <div style="margin-bottom: 1rem;">
                    <span class="badge ${badgeClass}">${statusText}</span>
                </div>
                <button class="btn btn-secondary btn-sm" style="width: 100%;" onclick="openAppointmentModalForDoctor('${d.name}', '${d.department}')">Book Consultation</button>
            </div>
        `;
    }).join('');
}

async function filterDoctors() {
    const searchInput = document.getElementById('doctorSearchInput');
    const statusSelect = document.getElementById('doctorStatusFilter');

    const term = (searchInput ? searchInput.value : '').toLowerCase();
    const status = statusSelect ? statusSelect.value : 'ALL';

    let doctors = await fetchDoctorsData();

    if (term) {
        doctors = doctors.filter(d => 
            d.name.toLowerCase().includes(term) ||
            d.specialization.toLowerCase().includes(term) ||
            d.department.toLowerCase().includes(term) ||
            (d.focus && d.focus.toLowerCase().includes(term))
        );
    }

    if (status !== 'ALL') {
        doctors = doctors.filter(d => d.status === status);
    }

    renderDoctorsList(doctors);
}

/* ==========================================================================
   DYNAMIC 2-TIER DEPARTMENT -> DOCTOR -> DATE -> TIME SLOTS ENGINE
   ========================================================================== */
async function populateDepartmentDropdown() {
    const deptSelect = document.getElementById('aptDeptSelect');
    if (!deptSelect) return;

    const doctors = await fetchDoctorsData();
    const departments = [...new Set(doctors.map(d => d.department))].sort();

    deptSelect.innerHTML = `<option value="">-- Select Department --</option>` + 
        departments.map(dept => `<option value="${dept}">${dept}</option>`).join('');
}

async function onDepartmentChange() {
    const deptSelect = document.getElementById('aptDeptSelect');
    const docSelect = document.getElementById('aptDoctorSelect');
    if (!deptSelect || !docSelect) return;

    const selectedDept = deptSelect.value;
    if (!selectedDept) {
        docSelect.innerHTML = `<option value="">-- Select Department First --</option>`;
        docSelect.disabled = true;
        await onDoctorOrDateChange();
        return;
    }

    let doctors = await fetchDoctorsData();
    const filteredDoctors = doctors.filter(d => d.department.toLowerCase() === selectedDept.toLowerCase());

    if (filteredDoctors.length === 0) {
        docSelect.innerHTML = `<option value="">No doctors available in ${selectedDept}</option>`;
        docSelect.disabled = true;
        await onDoctorOrDateChange();
        return;
    }

    docSelect.disabled = false;
    docSelect.innerHTML = `<option value="">-- Select Doctor --</option>` + 
        filteredDoctors.map(d => {
            let statusIcon = '🟢';
            let statusText = 'Available';
            if (d.status === 'In Surgery') { statusIcon = '🟡'; statusText = 'In Surgery'; }
            if (d.status === 'On Leave' || d.status === 'Absent') { statusIcon = '🔴'; statusText = 'On Leave (Absent)'; }
            return `<option value="${d.name}">${statusIcon} ${d.name} (${d.specialization} - ${statusText})</option>`;
        }).join('');

    await onDoctorOrDateChange();
}

async function onDoctorOrDateChange() {
    const docSelect = document.getElementById('aptDoctorSelect');
    const dateInput = document.getElementById('aptDate');
    const slotsContainer = document.getElementById('aptSlotsContainer');

    selectedTimeSlot = ''; // Reset chosen slot

    if (!slotsContainer) return;

    const doctorName = docSelect ? docSelect.value : '';
    const dateStr = dateInput ? dateInput.value : '';

    if (!doctorName || !dateStr) {
        slotsContainer.innerHTML = `<span style="color: var(--text-muted);">Please select both Doctor and Appointment Date to view available time slots.</span>`;
        return;
    }

    // Get Weekday Name (e.g., Monday, Tuesday)
    const dateObj = new Date(dateStr + 'T00:00:00');
    const days = ['Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday'];
    const dayName = days[dateObj.getDay()];

    const doctors = await fetchDoctorsData();
    const doctor = doctors.find(d => d.name === doctorName);

    if (!doctor) {
        slotsContainer.innerHTML = `<span style="color: var(--danger);">Doctor record not found.</span>`;
        return;
    }

    // Check doctor presence status
    let statusNotice = '';
    if (doctor.status === 'In Surgery') {
        statusNotice = `<div style="font-size: 0.8rem; color: #f59e0b; margin-bottom: 0.5rem; background: rgba(245, 158, 11, 0.1); padding: 0.5rem; border-radius: 6px;">🟡 <strong>Note:</strong> ${doctorName} is currently in Surgery. Slots below are for OPD consultations.</div>`;
    } else if (doctor.status === 'On Leave' || doctor.status === 'Absent') {
        slotsContainer.innerHTML = `
            <div style="color: #f87171; background: rgba(239, 68, 68, 0.1); border: 1px solid rgba(239, 68, 68, 0.2); padding: 0.75rem 1rem; border-radius: 10px;">
                🔴 <strong>${doctorName}</strong> is currently <strong>ON LEAVE (Absent)</strong>.<br>
                <span style="font-size: 0.8rem; color: var(--text-muted);">Consultations are unavailable today. Please select another doctor.</span>
            </div>
        `;
        return;
    }

    // Doctor schedule resolution
    const schedule = doctor.schedule || (DOCTOR_SCHEDULES[doctorName] ? DOCTOR_SCHEDULES[doctorName] : null);
    
    let shift = null;
    if (schedule && schedule[dayName]) {
        shift = schedule[dayName];
    }

    if (!shift) {
        let workingDaysStr = 'Mon-Sat';
        if (schedule) {
            const validDays = Object.keys(schedule).filter(k => schedule[k] && schedule[k].start);
            if (validDays.length > 0) workingDaysStr = validDays.join(', ');
        }

        slotsContainer.innerHTML = `
            <div style="color: #f87171; background: rgba(239, 68, 68, 0.1); border: 1px solid rgba(239, 68, 68, 0.2); padding: 0.75rem 1rem; border-radius: 10px;">
                ❌ <strong>${doctorName}</strong> has NO OPD schedule on <strong>${dayName}s</strong>.<br>
                <span style="font-size: 0.8rem; color: var(--text-muted);">Available OPD Days: <strong>${workingDaysStr}</strong>. Please pick another date.</span>
            </div>
        `;
        return;
    }

    // Generate 30-minute interval slots from start to end time
    const slots = generateTimeIntervals(shift.start, shift.end);

    // Fetch existing booked appointments for (doctorName, dateStr)
    const allAppointments = await fetchAppointmentsData();
    const bookedSlots = allAppointments
        .filter(a => a.doctor_name === doctorName && a.date === dateStr && a.status !== 'Cancelled')
        .map(a => a.time);

    const availableSlots = slots.filter(s => !bookedSlots.includes(s));
    
    // If all slots are fully booked for this date
    if (availableSlots.length === 0) {
        selectedTimeSlot = '';
        slotsContainer.innerHTML = `
            ${statusNotice}
            <div style="color: #f87171; background: rgba(239, 68, 68, 0.1); border: 1px solid rgba(239, 68, 68, 0.2); padding: 0.75rem 1rem; border-radius: 10px; margin-top: 0.5rem;">
                ⚠️ <strong>All OPD time slots for ${doctorName} on ${dayName} (${dateStr}) are FULLY BOOKED.</strong><br>
                <span style="font-size: 0.8rem; color: var(--text-muted);">Please pick another date or select a different doctor.</span>
            </div>
            <div class="slot-grid" style="margin-top: 0.75rem;">
                ${slots.map(s => `<button type="button" class="slot-btn disabled" disabled title="Already Booked">${s} ❌</button>`).join('')}
            </div>
        `;
        return;
    }

    // Auto-select the first available (open) slot by default
    selectedTimeSlot = availableSlots[0];

    slotsContainer.innerHTML = `
        ${statusNotice}
        <div style="margin-bottom: 0.5rem; font-size: 0.8rem; color: var(--text-muted);">
            📅 ${dayName} Shift (${formatTime12Hr(shift.start)} - ${formatTime12Hr(shift.end)}):
        </div>
        <div class="slot-grid">
            ${slots.map(s => {
                const isBooked = bookedSlots.includes(s);
                if (isBooked) {
                    return `<button type="button" class="slot-btn disabled" disabled title="Already Booked">${s} ❌</button>`;
                }
                const isActive = (s === selectedTimeSlot) ? 'active' : '';
                return `<button type="button" class="slot-btn ${isActive}" onclick="selectTimeSlot('${s}', this)">${s} ${isActive ? '✅' : ''}</button>`;
            }).join('')}
        </div>
    `;
}

function generateTimeIntervals(startStr, endStr) {
    const slots = [];
    let [startH, startM] = startStr.split(':').map(Number);
    let [endH, endM] = endStr.split(':').map(Number);

    let current = startH * 60 + startM;
    const end = endH * 60 + endM;

    while (current <= end) {
        let h = Math.floor(current / 60);
        let m = current % 60;
        
        let ampm = h >= 12 ? 'PM' : 'AM';
        let displayH = h % 12;
        if (displayH === 0) displayH = 12;
        let displayM = m < 10 ? '0' + m : m;

        slots.push(`${displayH}:${displayM} ${ampm}`);
        current += 30; // 30 mins interval
    }
    return slots;
}

function formatTime12Hr(time24) {
    let [h, m] = time24.split(':').map(Number);
    let ampm = h >= 12 ? 'PM' : 'AM';
    let displayH = h % 12;
    if (displayH === 0) displayH = 12;
    let displayM = m < 10 ? '0' + m : m;
    return `${displayH}:${displayM} ${ampm}`;
}

function selectTimeSlot(slotTime, btnElem) {
    selectedTimeSlot = slotTime;

    // Toggle active state across slot buttons
    const allSlotBtns = document.querySelectorAll('.slot-btn');
    allSlotBtns.forEach(b => {
        b.classList.remove('active');
        b.innerHTML = b.innerText.replace(' ✅', '');
    });

    if (btnElem) {
        btnElem.classList.add('active');
        if (!btnElem.innerText.includes('✅')) {
            btnElem.innerHTML = `${slotTime} ✅`;
        }
    }
    showToast(`Selected slot: ${slotTime}`, 'info');
}

async function openAppointmentModalForDoctor(doctorName, department) {
    await populateDepartmentDropdown();
    const deptSelect = document.getElementById('aptDeptSelect');
    if (deptSelect && department) {
        deptSelect.value = department;
        await onDepartmentChange();
        const docSelect = document.getElementById('aptDoctorSelect');
        if (docSelect) docSelect.value = doctorName;
    }
    openModal('appointmentModal');
}

/* ==========================================================================
   APPOINTMENTS PAGE LOADERS & ACTIONS
   ========================================================================== */
async function loadAppointmentsTable() {
    const tableBody = document.getElementById('appointmentsTableBody');
    if (!tableBody) return;

    const appointments = await fetchAppointmentsData();
    if (!appointments || appointments.length === 0) {
        tableBody.innerHTML = `<tr><td colspan="6" style="text-align: center; color: var(--text-muted); padding: 2rem;">No appointments scheduled</td></tr>`;
        return;
    }

    // Newest appointments at the VERY TOP of table
    const newestApts = [...appointments].reverse();

    tableBody.innerHTML = newestApts.map(a => {
        let badgeClass = 'badge-warning';
        if (a.status === 'Completed') badgeClass = 'badge-success';
        if (a.status === 'Cancelled') badgeClass = 'badge-cancelled';

        return `
            <tr>
                <td style="font-weight: 600;">${a.patient_name}</td>
                <td style="color: var(--primary);">${a.doctor_name}</td>
                <td><span class="badge badge-info">${a.department || 'General'}</span></td>
                <td>${a.date} (${a.time})</td>
                <td><span class="badge ${badgeClass}">${a.status}</span></td>
                <td>
                    <div style="display: flex; gap: 0.4rem; align-items: center; flex-wrap: wrap;">
                        ${a.status !== 'Completed' ? `<button class="btn btn-secondary btn-sm" onclick="updateAppointmentStatus('${a._id}', 'Completed')">✓ Complete</button>` : ''}
                        ${a.status !== 'Cancelled' ? `<button class="btn btn-secondary btn-sm" style="color: #f87171;" onclick="updateAppointmentStatus('${a._id}', 'Cancelled')">🚫 Cancel</button>` : ''}
                        <button class="btn btn-danger btn-sm" onclick="deleteAppointment('${a._id}')" title="Delete Record">🗑️</button>
                    </div>
                </td>
            </tr>
        `;
    }).join('');
}

async function updateAppointmentStatus(aptId, newStatus) {
    try {
        const res = await fetch(`${API_BASE_URL}/api/appointments/${aptId}`, {
            method: 'PUT',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ status: newStatus })
        });
        if (!res.ok) throw new Error();
        showToast(`Appointment status changed to ${newStatus}`, 'success');
    } catch {
        let apt = MOCK_DATA.appointments.find(a => String(a._id) === String(aptId));
        if (apt) apt.status = newStatus;
        showToast(`Appointment set to ${newStatus}`, 'info');
    }

    loadAppointmentsTable();
    if (document.body.dataset.page === 'dashboard') {
        loadRecentActivity();
        loadDashboardMetrics();
    }
}

async function deleteAppointment(aptId) {
    if (!confirm('Are you sure you want to delete this appointment?')) {
        return;
    }

    try {
        const res = await fetch(`${API_BASE_URL}/api/appointments/${aptId}`, {
            method: 'DELETE'
        });
        if (!res.ok) throw new Error();
        showToast('Appointment deleted successfully!', 'success');
    } catch {
        showToast('Appointment record deleted!', 'info');
    }

    MOCK_DATA.appointments = MOCK_DATA.appointments.filter(a => String(a._id) !== String(aptId));

    if (document.body.dataset.page === 'appointments') {
        loadAppointmentsTable();
    } else if (document.body.dataset.page === 'dashboard') {
        loadRecentActivity();
        loadDashboardMetrics();
    }
}

/* ==========================================================================
   MODAL CONTROLLERS & FORM ACTIONS
   ========================================================================== */
async function populatePatientsDatalist() {
    const datalist = document.getElementById('patientsDatalist');
    if (!datalist) return;

    const patients = await fetchPatientsData();
    datalist.innerHTML = patients.map(p => `<option value="${p.name}">${p.name} (${p.contact || 'Registered'})</option>`).join('');
}

async function openModal(modalId) {
    const modal = document.getElementById(modalId);
    if (modal) {
        if (modalId === 'appointmentModal') {
            await populateDepartmentDropdown();
            await populatePatientsDatalist();
            // Prevent past dates
            const dateInput = document.getElementById('aptDate');
            if (dateInput) {
                const today = new Date().toISOString().split('T')[0];
                dateInput.min = today;
                if (!dateInput.value || dateInput.value < today) {
                    dateInput.value = today;
                }
            }
            onDoctorOrDateChange();
        }
        modal.classList.add('active');
    }
}

function closeModal(modalId) {
    const modal = document.getElementById(modalId);
    if (modal) {
        modal.classList.remove('active');
    }
}

// Add Patient Submission Handler
async function submitAddPatient(event) {
    event.preventDefault();
    const name = document.getElementById('pName').value;
    const age = document.getElementById('pAge').value;
    const gender = document.getElementById('pGender').value;
    const blood_group = document.getElementById('pBlood').value;
    const contact = document.getElementById('pContact').value;
    const condition = document.getElementById('pCondition').value;

    const newPatient = { name, age: parseInt(age), gender, blood_group, contact, condition, status: 'Stable' };

    try {
        const res = await fetch(`${API_BASE_URL}/api/patients`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(newPatient)
        });

        if (!res.ok) {
            const errData = await res.json();
            throw new Error(errData.error || 'Failed to register patient');
        }

        const data = await res.json();
        showToast(`Patient ${name} registered successfully!`, 'success');
    } catch (err) {
        console.error("Patient registration failed:", err);
        showToast(err.message || 'Patient could not be saved. Please check server.', 'danger');
        return;
    }

    closeModal('addPatientModal');
    event.target.reset();

    if (document.body.dataset.page === 'patients') {
        loadPatientsTable();
    } else {
        showToast(`Navigating to Patients Directory to view ${name}...`, 'info');
        setTimeout(() => { window.location.href = 'patients.html'; }, 800);
    }
}

// Book Appointment Submission Handler
async function submitAddAppointment(event) {
    event.preventDefault();

    const patient_name = document.getElementById('aptPatientName').value.trim();
    const department = document.getElementById('aptDeptSelect').value;
    const doctor_name = document.getElementById('aptDoctorSelect').value;
    const date = document.getElementById('aptDate').value;

    if (!patient_name) {
        showToast('Please enter patient name.', 'warning');
        return;
    }

    if (!department) {
        showToast('Please select a department.', 'warning');
        return;
    }

    if (!doctor_name) {
        showToast('Please select a doctor.', 'warning');
        return;
    }

    if (!date) {
        showToast('Please select appointment date.', 'warning');
        return;
    }

    if (!selectedTimeSlot) {
        showToast('Please select an available time slot.', 'warning');
        return;
    }

    const newApt = {
        patient_name: patient_name,
        doctor_name: doctor_name,
        date: date,
        time: selectedTimeSlot,
        department: department,
        status: 'Scheduled'
    };

    console.log("Sending appointment:", newApt);

    try {
        const res = await fetch(`${API_BASE_URL}/api/appointments`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(newApt)
        });

        const data = await res.json();

        console.log("Appointment API response:", res.status, data);

        if (!res.ok) {
            throw new Error(
                data.error ||
                data.details ||
                `Appointment booking failed (${res.status})`
            );
        }

        // Backend ne successfully save kiya
        const aptObj = data.appointment || newApt;

        MOCK_DATA.appointments.unshift(aptObj);

        showToast(
            `Appointment booked successfully for ${patient_name} at ${selectedTimeSlot}.`,
            'success'
        );

        // Reset
        selectedTimeSlot = '';

        const form = event.target;
        form.reset();

        closeModal('appointmentModal');

        // Fresh data reload
        if (document.body.dataset.page === 'appointments') {
            await loadAppointmentsTable();
        } else if (document.body.dataset.page === 'dashboard') {
            await loadRecentActivity();
            await loadDashboardMetrics();
        } else {
            setTimeout(() => {
                window.location.href = 'appointments.html';
            }, 800);
        }

    } catch (err) {
        console.error("Appointment booking failed:", err);

        if (err.message && err.message.includes('already booked')) {
            showToast(err.message, 'danger');

            // Fresh slots reload
            await onDoctorOrDateChange();
            return;
        }

        showToast(
            err.message || 'Appointment could not be scheduled. Please try again.',
            'danger'
        );
    }
}

// Emergency Alert Action
function triggerEmergencyAlert() {
    showToast('🚨 EMERGENCY CODE BLUE TRIGGERED! Alerting Duty Doctors...', 'danger');
}

/* ==========================================================================
   TOAST NOTIFICATION HELPER
   ========================================================================== */
function showToast(message, type = 'info') {
    let container = document.getElementById('toastContainer');
    if (!container) {
        container = document.createElement('div');
        container.id = 'toastContainer';
        container.className = 'toast-container';
        document.body.appendChild(container);
    }

    const toast = document.createElement('div');
    toast.className = `toast toast-${type}`;
    toast.innerHTML = `<span>${message}</span>`;
    container.appendChild(toast);

    setTimeout(() => {
        toast.style.opacity = '0';
        toast.style.transform = 'translateX(100%)';
        setTimeout(() => toast.remove(), 300);
    }, 4000);
}
