# 🏥 MediSure – AI Health Check‑Up System

A **production‑ready AI‑powered healthcare web application** built with **Flask**, **Machine Learning**, and **secure email workflows**, deployed on **Render** with modern best practices.

This project provides:

* AI disease prediction (Diabetes, Heart, Cancer, Alzheimer’s, Migraine, Typhoid)
* Secure authentication (Login / Signup)
* OTP‑based **Forgot Password** flow (email verified)
* Doctor consultation & appointment booking with **Zoom integration**
* PDF medical report parsing
* Chat‑based disease guidance

---

## ✨ Live Demo

🌐 **Production URL**
👉 [https://medisureapplication.onrender.com](https://medisureapplication.onrender.com)

---

## 🚀 Features

### 🔐 Authentication

* User Signup & Login
* Password hashing using `werkzeug.security`
* Secure session handling

### 📧 Email System (Render‑Compatible)

* OTP email delivery using **Resend API (HTTP – no SMTP)**
* Works perfectly on Render (SMTP is blocked)
* Verified domain sender

### 🧠 AI Disease Prediction

* Diabetes
* Heart Disease
* Breast Cancer
* Alzheimer’s
* Migraine
* Typhoid
* NLP‑based disease prediction from symptoms

### 📄 PDF Report Upload

* Upload lab reports
* Auto‑extract values
* Use extracted data for predictions

### 👨‍⚕️ Doctor Consultation

* Doctor listing
* Appointment booking
* Auto Zoom meeting generation
* Email notifications to doctor & patient

### 💬 AI Chat Assistant

* Disease‑specific remedies
* Precautions & care suggestions

---

## 🛠️ Tech Stack

| Layer      | Technology            |
| ---------- | --------------------- |
| Backend    | Flask (Python)        |
| ML Models  | Scikit‑learn, XGBoost |
| Database   | SQLite                |
| Email      | Resend API            |
| Video      | Zoom API              |
| Frontend   | HTML, CSS, Bootstrap  |
| Deployment | Render                |

---

## 📁 Project Structure

```
HEALTH-CHECK-UP-SYSTEM/
│
├── app.py
├── auth.py
├── email_utils.py
├── pdf_reader.py
├── chat_data.py
├── database.db
├── requirements.txt
├── runtime.txt
├── .gitignore
│
├── templates/
├── static/
├── uploads/
├── ml_models/
│   ├── diabetes/
│   ├── heart/
│   ├── breastcancer/
│   ├── alzheimer/
│   ├── migraine/
│   ├── typhoid/
│   └── disease_nlp/
└── utils/
```

---

## 🔑 Environment Variables (IMPORTANT)

Set these in **Render → Environment Variables** (NOT in code):

```env
RESEND_API_KEY=re_xxxxxxxxxxxxxxxxx
```

❌ Never commit `.env` files to GitHub

---

## 📧 Email (OTP) – How It Works

### Why Resend?

Render blocks SMTP ports (587 / 465). SMTP **will never work**.

✅ Resend uses HTTP → Fully supported

### OTP Flow

1. User enters email
2. Server generates OTP
3. OTP sent via Resend API
4. User verifies OTP
5. Password reset allowed

---

## 🧾 Sample OTP Email Code

```python
import requests, os

RESEND_API_KEY = os.getenv("RESEND_API_KEY")

def send_otp_email(to_email, otp):
    url = "https://api.resend.com/emails"
    headers = {
        "Authorization": f"Bearer {RESEND_API_KEY}",
        "Content-Type": "application/json"
    }
    payload = {
        "from": "MediSure <no-reply@medisure.com>",
        "to": [to_email],
        "subject": "Password Reset OTP",
        "html": f"<h1>Your OTP: {otp}</h1><p>Valid for 5 minutes</p>"
    }
    r = requests.post(url, json=payload, headers=headers)
    return r.status_code == 200
```

---

## 🧪 Local Setup

```bash
git clone https://github.com/yourusername/medisure.git
cd medisure
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
python app.py
```

Visit: [http://127.0.0.1:5000](http://127.0.0.1:5000)

---

## ☁️ Deployment (Render)

1. Push project to GitHub
2. Create **New Web Service** on Render
3. Connect GitHub repo
4. Set build command:

   ```bash
   pip install -r requirements.txt
   ```
5. Start command:

   ```bash
   python app.py
   ```
6. Add environment variables
7. Deploy 🎉

---

## 🔒 Security Notes

* Passwords hashed
* OTP stored in session
* `.env` ignored via `.gitignore`
* API keys never exposed

---

## 📸 Screenshots

*(Add screenshots of UI, predictions, OTP emails here)*

---

## 🧑‍💻 Author

**Faiz Raza**
AI & Full‑Stack Developer

---

## ⭐ If you like this project

* Star ⭐ the repo
* Fork 🍴 it
* Contribute 🤝

---

## 📜 License

This project is licensed for educational and portfolio use.

---

> 💡 *MediSure demonstrates how AI + Web + Secure Infrastructure can be combined into a real‑world healthcare system.*
