from flask_mail import Message
from app import mail
from flask import render_template
from app import app

def send_email(subject, sender, recipients, html_body):
    msg = Message(subject, sender=sender, recipients=recipients)
    msg.html = html_body
    mail.send(msg)

def send_password_reset_email(html):
    send_email('Audit',
               sender=app.config['ADMINS'][0],
               recipients=['itskkang@gmail.com'],
               html_body=render_template(html))
                
