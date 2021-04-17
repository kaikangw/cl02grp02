from flask_mail import Message
import pdfkit
import os
from app import mail
from flask import render_template
from app import app

def send_email(subject, sender, recipients, html_body):
    msg = Message(subject, sender=sender, recipients=recipients)
    msg.html = html_body
    with open("audit.pdf", "rb") as fh:
        msg.attach('audit.pdf','application/pdf',fh.read())
        mail.send(msg)
    mail.send(msg)

def send_audit_mail(html,form):
    output_from_parsed_template = render_template(html,form=form)
    os.remove('output.html') if os.path.exists('output.html') else None
    os.remove('audit.pdf') if os.path.exists('audit.pdf') else None
    with open("output.html", "w") as fh:
        fh.write(output_from_parsed_template)
    options = {"enable-local-file-access": None}
    path_wkhtmltopdf = r'C:\Program Files\wkhtmltopdf\bin\wkhtmltopdf.exe'
    config = pdfkit.configuration(wkhtmltopdf=path_wkhtmltopdf)
    pdfkit.from_file('output.html', 'audit.pdf', options = options,configuration=config)

    send_email('Audit', 
               sender=app.config['ADMINS'][0],
               recipients=['ezchecksg@gmail.com'],
               html_body=render_template(html,form=form))
                
