import smtplib
import schedule
import time


def send_mail(sender_email: str, receiver_email: str, password: str, message: str):
    # Email details
    with smtplib.SMTP("smtp.gmail.com", 587) as server:
        server.starttls()
        server.login(sender_email, password)
        server.sendmail(sender_email, receiver_email, message)




    
