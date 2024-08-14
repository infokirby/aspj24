import sklearn 
import joblib
import random
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from dotenv import load_dotenv
import os

from flask import session
from datetime import datetime, timedelta
from customer_order import CustomerOrder

model = joblib.load('fraud_detection_model.pkl')

def generate_otp(length = 6):
    return ''.join([str(random.randint(0, 9)) for _ in range(length)])
def send_otp_email(recipient_email, otp):
    sender_email = os.getenv("EMAIL")
    sender_password = os.getenv("EMAIL_PASSWORD")
    
    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = recipient_email
    msg['Subject'] = "Your OTP Code"
    
    body = f"Your OTP code is {otp}. Please use this code to verify your order."
    msg.attach(MIMEText(body, 'plain'))
    
    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(sender_email, sender_password)
        text = msg.as_string()
        server.sendmail(sender_email, recipient_email, text)
        server.quit()
        return True
    except Exception as e:
        print(f"Failed to send email: {e}")
        return False
    
def is_fraudulent_order(current_order, past_orders):
    current_total = current_order['Total']
    past_totals = [order['Total'] for order in past_orders]
    
    if not past_totals:
        return False  # No past orders to compare with
    
    average_past_total = sum(past_totals) / len(past_totals)
    
    if current_total > 3 * average_past_total:
        otp = generate_otp()
        email_sent = send_otp_email(current_order['CustomerEmail'], otp)
        if email_sent:
            current_order['OTP'] = otp
            session['otp'] = otp
            return True
        else:
            return False
    
    return False