from dotenv import load_dotenv
load_dotenv()
import os
import requests
import base64
import time
import sqlite3
from functools import wraps
from flask import session, redirect, url_for
from utils.zoom import create_zoom_meeting
from utils.email_service import send_email
from email_utils import send_otp_email
from auth import generate_otp, get_db, update_password, email_exists

from flask import session
from auth import update_password, email_exists, generate_otp
from flask import session, redirect, url_for
from auth import create_user_table, register_user, login_user
from flask import Flask, render_template, request
import numpy as np
import pandas as pd
from utils.model_loader import *
from utils.preprocess import *
from flask import Flask, render_template, request, redirect, url_for, session
import random

from flask import Flask, render_template, request, redirect, session, url_for
from werkzeug.security import generate_password_hash, check_password_hash
from flask import session, url_for
import requests, base64, os
from datetime import datetime
from dotenv import load_dotenv
from chat_data import DISEASE_REMEDIES
from flask import jsonify
from pdf_reader import extract_values_from_pdf, extract_breast_pdf,extract_heart_pdf,extract_alzheimer_pdf,extract_migraine_pdf,extract_typhoid_pdf
import os








app = Flask(__name__)
app.secret_key = "super_secret_key_123"
sqlite3.connect("database.db", timeout=10)

#EMAIL_ADDRESS = "razafaiz003@gmail.com"
#EMAIL_PASSWORD = "zjphoxqsdhejsgvf"
#RESEND_API_KEY = re_J5A1KkHB_8gpprJVn6BHGG7Gv2bBJs4ss

# ================= ZOOM INTEGRATION ================= #
ZOOM_ACCOUNT_ID = "4De-CZigQj-6wfHOXRvgUA"
ZOOM_CLIENT_ID = "vhxEvQbVTnmfiK_3P1fang"
ZOOM_CLIENT_SECRET = "ipPPcfz1Pcx6b57ddpop8EtYyDvjBZAt"





def get_access_token():
    credentials = f"{ZOOM_CLIENT_ID}:{ZOOM_CLIENT_SECRET}"
    encoded_credentials = base64.b64encode(credentials.encode()).decode()

    url = "https://zoom.us/oauth/token"
    headers = {
        "Authorization": f"Basic {encoded_credentials}"
    }
    data = {
        "grant_type": "account_credentials",
        "account_id": ZOOM_ACCOUNT_ID
    }

    response = requests.post(url, headers=headers, data=data)
    result = response.json()

    if "access_token" not in result:
        print("ZOOM TOKEN ERROR:", result)
        raise Exception("Zoom access token not received")

    return result["access_token"]


def create_zoom_meeting(topic, start_time):
    token = get_access_token()

    url = "https://api.zoom.us/v2/users/me/meetings"
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }

    payload = {
        "topic": topic,
        "type": 2,
        "start_time": start_time,
        "duration": 30,
        "settings": {
            "join_before_host": True,
            "waiting_room": False
        }
    }

    response = requests.post(url, headers=headers, json=payload)
    meeting = response.json()

    if "join_url" not in meeting:
        print("ZOOM MEETING ERROR:", meeting)
        raise Exception("Zoom meeting not created")

    return meeting["join_url"]








# ================= EMAIL (MAILERSEND) ================= #

import os
import requests

RESEND_API_KEY = os.getenv("RESEND_API_KEY")

def send_email(to_email, subject, html):
    response = requests.post(
        "https://api.resend.com/emails",
        headers={
            "Authorization": f"Bearer {RESEND_API_KEY}",
            "Content-Type": "application/json",
        },
        json={
            "from": "onboarding@resend.dev",
            "to": [to_email],
            "subject": subject,
            "html": html,
        },
        timeout=10
    )

    print("RESEND STATUS:", response.status_code)
    print("RESEND RESPONSE:", response.text)

    return response.status_code == 200



def send_otp_email(email, otp):
    html = f"""
    <h2>Password Reset OTP</h2>
    <h1>{otp}</h1>
    <p>This OTP is valid for 5 minutes.</p>
    """
    return send_email(email, "Your OTP Code", html)















# ================= LOAD ALL MODELS ================= #

# Diabetes
diabetes_model = load_model("ml_models/diabetes/diabetes_model.pkl")
diabetes_scaler = load_scaler("ml_models/diabetes/scaler.pkl")

# Heart
heart_model = load_model("ml_models/heart/heart_disease_model.pkl")

# Breast Cancer
breast_model = load_model("ml_models/breastcancer/breast_cancer_model.pkl")

# Alzheimer
alz_model = load_model("ml_models/alzheimer/alzheimers_model.pkl")
alz_scaler = load_scaler("ml_models/alzheimer/alzheimers_scaler.pkl")

# Migraine
migraine_model = load_model("ml_models/migraine/migraine_model.pkl")
migraine_encoder = load_encoder("ml_models/migraine/migraine_label_encoder.pkl")
migraine_features = load_features("ml_models/migraine/migraine_important_features.pkl")

# Typhoid
typhoid_model = load_model("ml_models/typhoid/typhoid_model.pkl")
typhoid_features = load_features("ml_models/typhoid/typhoid_important_features.pkl")

# Disease NLP
disease_nlp_model = load_model("ml_models/disease_nlp/disease_nlp_xgboost.pkl")
disease_label_encoder = load_encoder("ml_models/disease_nlp/disease_label_encoder.pkl")



# ================= ROUTES ================= #
@app.route("/")
def home():
    return redirect("/login")


@app.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]

        hashed = generate_password_hash(password)

        try:
            with sqlite3.connect("database.db") as conn:
                cur = conn.cursor()
                cur.execute(
                    "INSERT INTO users (email, password) VALUES (?, ?)",
                    (email, hashed)
                )
                conn.commit()
            return redirect("/login")
        except sqlite3.IntegrityError:
            return "Email already exists"

    return render_template("signup.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]

        with sqlite3.connect("database.db") as conn:
            cur = conn.cursor()
            cur.execute("SELECT * FROM users WHERE email = ?", (email,))
            user = cur.fetchone()

        print("DEBUG USER:", user)  # ← IMPORTANT

        if user and check_password_hash(user[2], password):
            session["user_id"] = user[0]
            return redirect("/dashboard")

        return "❌ Invalid email or password"

    return render_template("login.html")


@app.route("/dashboard")
def dashboard():
    if "user_id" not in session:
        return redirect("/login")
    return render_template("index.html")


@app.route("/logout")
def logout():
    session.clear()
    return redirect("/login")

@app.route("/forgot-password", methods=["GET", "POST"])
def forgot_password():
    if request.method == "POST":
        email = request.form["email"]
        otp = random.randint(100000, 999999)
        session["otp"] = otp
        session["email"] = email

        ok = send_email(
            email,
            "Your OTP – MediSure",
            f"<h2>Your OTP is {otp}</h2><p>Valid for 5 minutes.</p>"
        )

        if not ok:
            return "Email sending failed"

        return redirect(url_for("verify_otp"))








@app.route("/verify-otp", methods=["GET", "POST"])
def verify_otp():
    if request.method == "POST":
        user_otp = request.form["otp"].strip()
        saved_otp = session.get("otp")
        otp_time = session.get("otp_time")

        if not saved_otp or not otp_time:
            return "OTP expired"

        if time.time() - otp_time > 300:
            return "OTP expired"

        if user_otp == saved_otp:
            session["reset_email"] = session["email"]
            return redirect(url_for("reset_password"))

        return "INVALID OTP"

    return render_template("verify_otp.html")








@app.route("/reset-password", methods=["GET", "POST"])
def reset_password():
    if "reset_email" not in session:
        return redirect(url_for("login"))

    if request.method == "POST":
        email = session["reset_email"]
        password = request.form["password"]

        users = []
        try:
            with open("users.txt", "r") as f:
                users = f.readlines()
        except:
            pass

        with open("users.txt", "w") as f:
            updated = False
            for u in users:
                e, p = u.strip().split(",")
                if e == email:
                    f.write(f"{email},{password}\n")
                    updated = True
                else:
                    f.write(u)
            if not updated:
                f.write(f"{email},{password}\n")

        session.pop("otp", None)
        session.pop("reset_email", None)
        session.pop("email", None)

        return redirect(url_for("login"))

    return render_template("reset_password.html")

@app.route("/consult-doctor")
def consult_doctor():
    if "user_id" not in session:
        return redirect("/login")

    with sqlite3.connect("database.db") as conn:
        cur = conn.cursor()
        cur.execute("SELECT * FROM doctors")
        doctors = cur.fetchall()

    return render_template("consult_doctor.html", doctors=doctors)

@app.route("/doctors")
def doctors():
    if "user_id" not in session:
        return redirect(url_for("login"))

    db = get_db()
    doctors = db.execute("SELECT * FROM doctors").fetchall()
    return render_template("doctors.html", doctors=doctors)

@app.route("/book/<int:doctor_id>", methods=["GET", "POST"])
def book_appointment(doctor_id):
    if "user_id" not in session:
        return redirect("/login")

    with sqlite3.connect("database.db") as conn:
        cur = conn.cursor()
        cur.execute("SELECT name, email FROM doctors WHERE id=?", (doctor_id,))
        doctor = cur.fetchone()

    if request.method == "POST":
        date = request.form["date"]
        time_ = request.form["time"]

        # Zoom needs ISO format
        start_time = f"{date}T{time_}:00"

        # 🔥 AUTO CREATE ZOOM MEETING
        zoom_link = create_zoom_meeting(
            topic=f"Doctor Consultation - {doctor[0]}",
            start_time=start_time
        )

        conn = sqlite3.connect("database.db")
        cur = conn.cursor()

        cur.execute("""
            INSERT INTO appointments
            (user_id, doctor_id, appointment_date, appointment_time, zoom_link)
            VALUES (?, ?, ?, ?, ?)
        """, (session["user_id"], doctor_id, date, time_, zoom_link))

        conn.commit()

        cur.execute("SELECT email FROM users WHERE id=?", (session["user_id"],))
        patient_email = cur.fetchone()[0]

        conn.close()

        subject = "Doctor Appointment Confirmed"

        patient_body = f"""
Your appointment is confirmed ✅

Doctor: {doctor[0]}
Date: {date}
Time: {time_}

Join Zoom Call:
{zoom_link}
"""

        doctor_body = f"""
New appointment booked.

Patient Email: {patient_email}
Date: {date}
Time: {time_}

Zoom Link:
{zoom_link}
"""

        send_email(patient_email, subject, patient_body)
        send_email(doctor[1], subject, doctor_body)

        return redirect("/appointment-success")

    return render_template("book_appointment.html", doctor_id=doctor_id)


@app.route("/appointment-success")
def appointment_success():
    if "user_id" not in session:
        return redirect("/login")
    return render_template("appointment_success.html")




@app.route("/my-appointments")
def my_appointments():
    if "user_id" not in session:
        return redirect("/login")

    conn = sqlite3.connect("database.db")
    cur = conn.cursor()

    cur.execute("""
        SELECT 
            d.name,
            a.appointment_date,
            a.appointment_time,
            a.zoom_link
        FROM appointments a
        JOIN doctors d ON a.doctor_id = d.id
        WHERE a.user_id = ?
    """, (session["user_id"],))

    appointments = cur.fetchall()
    conn.close()
    appointments = appointments[5:]
    return render_template(
        "my_appointments.html",
        appointments=appointments
    )

@app.route("/chat", methods=["POST"])
def chat():
    data = request.get_json()
    user_msg = data.get("message", "").lower()
    disease = data.get("disease", "").strip().title()

    disease_data = DISEASE_REMEDIES.get(disease)

    if not disease_data:
        return jsonify({"reply": "Please consult a doctor for proper guidance."})

    if "remedy" in user_msg or "treatment" in user_msg or "care" in user_msg:
        reply = disease_data["intro"] + "\n\n" + "\n".join(
            f"• {tip}" for tip in disease_data["tips"]
        )
    else:
        reply = "You can ask me about remedies, diet, precautions, or treatment."

    return jsonify({"reply": reply})



@app.route("/home")
def public_home():
    return render_template("index.html")


@app.route("/about")
def about():
    return render_template("about.html")


@app.route("/")
def index():
    if "user" not in session:
        return redirect(url_for("login"))
    return render_template("index.html")


# ---------------- DIABETES ---------------- #
@app.route("/diabetes", methods=["GET", "POST"])
def diabetes():
    extracted = {}
    pdf_uploaded = False

    if request.method == "POST":

        # PDF upload button clicked
        if "upload_pdf" in request.form:
            pdf = request.files.get("report")

            if pdf and pdf.filename:
                pdf_path = os.path.join("uploads", pdf.filename)
                pdf.save(pdf_path)

                extracted = extract_values_from_pdf(pdf_path)
                pdf_uploaded = True

            return render_template(
                "diabetes.html",
                extracted=extracted,
                pdf_uploaded=pdf_uploaded
            )


        Age = request.form.get("Age")
        Gender = request.form.get("Gender")
        BMI = request.form.get("BMI")
        Glucose_Level = request.form.get("Glucose_Level")
        Blood_Pressure = request.form.get("Blood_Pressure")
        Insulin = request.form.get("Insulin")
        Physical_Activity = request.form.get("Physical_Activity")
        Family_History = request.form.get("Family_History")

        values = [
            int(Age),
            str(Gender),
            float(BMI),
            int(Glucose_Level),
            int(Blood_Pressure),
            float(Insulin),
            int(Physical_Activity),
            str(Family_History)
        ]

        prediction = diabetes_model.predict([values])[0]
        result = "Diabetes Detected" if prediction == 1 else "No Diabetes"

        return render_template(
            "result.html",
            disease="diabetes",
            result=result
        )

    return render_template("diabetes.html")





# Models dictionary
models = {
    'diabetes': diabetes_model
}

# ---------------- HEART ---------------- #
@app.route("/heart", methods=["GET", "POST"])
def heart():
    extracted = {}
    pdf_uploaded = False

    if request.method == "POST":

        # PDF upload button clicked
        if "upload_pdf" in request.form:
            pdf = request.files.get("report")

            if pdf and pdf.filename:
                pdf_path = os.path.join("uploads", pdf.filename)
                pdf.save(pdf_path)

                extracted = extract_heart_pdf(pdf_path)
                pdf_uploaded = True

            return render_template(
                "heart.html",
                extracted=extracted,
                pdf_uploaded=pdf_uploaded
            )


        Age = request.form.get("Age")
        Cholesterol_Total = request.form.get("Cholesterol_Total")
        Hypertension = request.form.get("Hypertension")
        Diabetes = request.form.get("Diabetes")
        Previous_Heart_Attack = request.form.get("Previous_Heart_Attack")
        BMI = request.form.get("BMI")
        values = [
            int(Age),
            int(Cholesterol_Total),
            int(Hypertension),
            int(Diabetes),
            int(Previous_Heart_Attack),
            float(BMI)
        ]

        
        pred = heart_model.predict([values])[0]
        result = "Heart Disease Detected" if pred == 1 else "No Heart Disease"

        return render_template(
            "result.html",
            disease="Heart Disease",
            result=result
        )

    return render_template("heart.html")









# ---------------- BREAST CANCER ---------------- #
@app.route("/breastcancer", methods=["GET", "POST"])
def breast_cancer():
    extracted = {}
    pdf_uploaded = False

    if request.method == "POST":

        # PDF upload button clicked
        if "upload_pdf" in request.form:
            pdf = request.files.get("report")

            if pdf and pdf.filename:
                pdf_path = os.path.join("uploads", pdf.filename)
                pdf.save(pdf_path)

                extracted = extract_breast_pdf(pdf_path)
                pdf_uploaded = True

            return render_template(
                "breastcancer.html",
                extracted=extracted,
                pdf_uploaded=pdf_uploaded
            )


        radius_mean = float(request.form.get("radius_mean"))
        texture_mean = float(request.form.get("texture_mean"))
        perimeter_mean = float(request.form.get("perimeter_mean"))
        area_mean = float(request.form.get("area_mean"))
        smoothness_mean = float(request.form.get("smoothness_mean"))

        values = [
            float(radius_mean),
            float(texture_mean),
            float(perimeter_mean),
            float(area_mean),
            float(smoothness_mean)
        ]

        pred = breast_model.predict([values])[0]
        result = "Breast Cancer Detected" if pred == 1 else "No Breast Cancer"

        return render_template(
            "result.html",
            disease="Breast Cancer",
            result=result
        )

    return render_template("breastcancer.html")


# ---------------- ALZHEIMER ---------------- #
@app.route("/alzheimer", methods=["GET", "POST"])
def alzheimer():
    extracted = {}
    pdf_uploaded = False

    if request.method == "POST":

        # PDF upload button clicked
        if "upload_pdf" in request.form:
            pdf = request.files.get("report")

            if pdf and pdf.filename:
                pdf_path = os.path.join("uploads", pdf.filename)
                pdf.save(pdf_path)

                extracted = extract_alzheimer_pdf(pdf_path)
                pdf_uploaded = True

            return render_template(
                "alzheimer.html",
                extracted=extracted,
                pdf_uploaded=pdf_uploaded
            )


        Age = request.form.get("Age")
        MMSE=request.form.get("MMSE")
        FunctionalAssessment=request.form.get("FunctionalAssessment")
        MemoryComplaints=request.form.get("MemoryComplaints")
        BehavioralProblems=request.form.get("BehavioralProblems")
        ADL=request.form.get("ADL")
        Confusion=request.form.get("Confusion")
        Disorientation=request.form.get("Disorientation")
        DifficultyCompletingTasks=request.form.get("DifficultyCompletingTasks")
        Forgetfulness=request.form.get("Forgetfulness")
        FamilyHistoryAlzheimers=request.form.get("FamilyHistoryAlzheimers")
        values = [
            int(Age),
            int(MMSE),
            int(FunctionalAssessment),
            int(MemoryComplaints),
            int(BehavioralProblems),
            int(ADL),
            int(Confusion),
            int(Disorientation),
            int(DifficultyCompletingTasks),
            int(Forgetfulness),
            int(FamilyHistoryAlzheimers)
        
        ]
        scaled = alz_scaler.transform([values])
        pred = alz_model.predict(scaled)[0] 
        result = "Alzheimer's Detected" if pred == 1 else "No Alzheimer's"

        return render_template(
            "result.html",
            disease="Alzheimer's",
            result=result
        )

    return render_template("alzheimer.html")





# Models dictionary
models = {
    'alzheimer': alz_model
}



# ---------------- MIGRAINE ---------------- #
@app.route("/migraine", methods=["GET", "POST"])
def migraine():
    extracted = {}
    pdf_uploaded = False

    if request.method == "POST":

        # PDF upload button clicked
        if "upload_pdf" in request.form:
            pdf = request.files.get("report")

            if pdf and pdf.filename:
                pdf_path = os.path.join("uploads", pdf.filename)
                pdf.save(pdf_path)

                extracted = extract_migraine_pdf(pdf_path)
                pdf_uploaded = True

            return render_template(
                "migraine.html",
                extracted=extracted,
                pdf_uploaded=pdf_uploaded
            )



        Visual = request.form.get("Visual")
        Intensity = request.form.get("Intensity")
        Age = request.form.get("Age")
        Vertigo = request.form.get("Vertigo")
        Frequency = request.form.get("Frequency")
        Character = request.form.get("Character")
        Sensory = request.form.get("Sensory")
        Duration = request.form.get("Duration")
        Vomit = request.form.get("Vomit")
        Nausea = request.form.get("Nausea")
        DPF = request.form.get("DPF")
        

        values = [
            int(Visual),
            int(Intensity),
            int(Age),
            int(Vertigo),
            int(Frequency),
            int(Character),
            int(Sensory),
            int(Duration),
            int(Vomit),
            int(Nausea),
            int(DPF),
            
        ]

        pred = migraine_model.predict([values])[0]
        result = "Migraine Detected" if pred == 1 else "No Migraine"

        return render_template(
            "result.html",
            disease="Migraine",
            result=result
        )

    return render_template("migraine.html")





# Models dictionary
models = {
    
    'migraine': migraine_model
}


# ---------------- TYPHOID ---------------- #
@app.route("/typhoid", methods=["GET", "POST"])
def typhoid():
    extracted = {}
    pdf_uploaded = False

    if request.method == "POST":

        # PDF upload button clicked
        if "upload_pdf" in request.form:
            pdf = request.files.get("report")

            if pdf and pdf.filename:
                pdf_path = os.path.join("uploads", pdf.filename)
                pdf.save(pdf_path)

                extracted = extract_typhoid_pdf(pdf_path)
                pdf_uploaded = True

            return render_template(
                "typhoid.html",
                extracted=extracted,
                pdf_uploaded=pdf_uploaded
            )


        PlateletCount = int(request.form.get("PlateletCount"))
        Age = int(request.form.get("Age"))
        Hemoglobin = float(request.form.get("Hemoglobin"))
        Calcium = float(request.form.get("Calcium"))
        Potassium = float(request.form.get("Potassium"))
        TreatmentDuration = int(request.form.get("TreatmentDuration"))
        BloodCulture_Bacteria = int(request.form.get("BloodCultureBacteria"))
        SymptomsSeverity = int(request.form.get("SymptomsSeverity"))
        UrineCultureBacteria = int(request.form.get("UrineCultureBacteria"))
        CurrentMedication = int(request.form.get("CurrentMedication"))
        Gender = int(request.form.get("Gender"))
        

        values = [
            int(PlateletCount),
            int(Age),
            float(Hemoglobin),
            float(Calcium),
            float(Potassium),
            int(TreatmentDuration),
            int(BloodCulture_Bacteria),
            int(SymptomsSeverity),
            int(UrineCultureBacteria),
            int(CurrentMedication),
            str(Gender)
        ]
                     
        pred = typhoid_model.predict([values])[0]
        result = "Typhoid Detected" if pred == 1 else "No Typhoid"

        return render_template(
            "result.html",
            disease="Typhoid",
            result=result
        )

    return render_template("typhoid.html")







# ---------------- DISEASE NLP ---------------- #
def predict_disease(age, gender, symptoms, symptom_count):
    input_df = pd.DataFrame([{
        "Age": age,
        "Gender": gender,
        "Symptoms": symptoms,
        "Symptom_Count": symptom_count
    }])

    pred_encoded = disease_nlp_model.predict(input_df)[0]
    return disease_label_encoder.inverse_transform([pred_encoded])[0]
@app.route('/disease_nlp', methods=['GET', 'POST'])
def disease():
    if request.method == 'POST':
        age = int(request.form.get('age', 0))
        gender = request.form.get('gender', '').lower()
        symptoms = request.form.get('symptoms', '')
        symptom_count = int(
            request.form.get('symptom_count', len(symptoms.split()))
        )

        disease_name = predict_disease(
            age, gender, symptoms, symptom_count
        )

        return render_template(
            "result.html",
            disease="Predicted Disease",
            result=disease_name
        )

    return render_template("disease_nlp.html")


# ================= RUN ================= #
import os

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)

