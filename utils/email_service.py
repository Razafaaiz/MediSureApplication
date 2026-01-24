import smtplib
from email.mime.text import MIMEText

EMAIL = "yourgmail@gmail.com"
APP_PASSWORD = "your_app_password"

def send_email(to_email, zoom_link):
    msg = MIMEText(f"Your doctor consultation Zoom link:\n\n{zoom_link}")
    msg["Subject"] = "Doctor Appointment - Zoom Link"
    msg["From"] = EMAIL
    msg["To"] = to_email

    server = smtplib.SMTP_SSL("smtp.gmail.com", 465)
    server.login(EMAIL, APP_PASSWORD)
    server.send_message(msg)
    server.quit()
