from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail

def send_otp_email(to_email, otp, api_key, sender_email):
    try:
        message = Mail(
            from_email=sender_email,
            to_emails=to_email,
            subject="HealthCare System - Password Reset OTP",
            plain_text_content=f"Your OTP is: {otp}"
        )

        sg = SendGridAPIClient(api_key)
        sg.send(message)

        return True
    except Exception as e:
        print("SENDGRID ERROR:", e)
        return False
