import smtplib
from email.mime.text import MIMEText
import os
from dotenv import load_dotenv

def send_mail(ride_id, customer, driver, rating, comments):
    port = 587
    smtp_server = 'smtp.gmail.com'
    login = os.getenv("EMAIL_USER")
    password = os.getenv("EMAIL_PASS")
    message = f"<h3>New Feedback Submission</h3><ul><li>ride_id: {ride_id}</li><li>Customer: {customer}</li><li>Driver: {driver}</li><li>Rating: {rating}</li><li>Comments: {comments}</li></ul>"

    sender_email = os.getenv("EMAIL_USER")
    receiver_email = os.getenv("RCV_EMAIL")
    msg = MIMEText(message, 'html')
    msg['Subject'] = 'KSRide Feedback'
    msg['From'] = sender_email
    msg['To'] = receiver_email

    with smtplib.SMTP(smtp_server, port) as server:
        server.ehlo()
        server.starttls()
        server.ehlo()
        server.login(login, password)
        server.sendmail(sender_email, receiver_email, msg.as_string())

