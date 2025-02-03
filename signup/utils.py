from email.mime.text import MIMEText
import smtplib

from django.conf import settings
import pyotp

def send_otp(email, otp):
    message = MIMEText(f"Your OTP is {otp}. It is valid for 1 minute.")
    message["Subject"] = "Your One-Time Password (OTP)"
    message["From"] = settings.EMAIL_HOST_USER
    message["To"] = email

    try:
        with smtplib.SMTP("smtp.gmail.com", 587) as server:
            server.starttls()
            server.login(settings.EMAIL_HOST_USER, settings.EMAIL_HOST_PASSWORD)
            server.sendmail(settings.EMAIL_HOST_USER, email, message.as_string())
        print("OTP email sent successfully.")
    except Exception as e:
        print(f"Failed to send OTP email. Error: {e}")