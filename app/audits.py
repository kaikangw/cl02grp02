from flask import Blueprint, render_template, redirect, request, url_for, flash
import os
from jinja2 import TemplateNotFound
from app import db
from app.models import Audit, Messages, Comments, Broadcasts, User
from app.forms import AuditForm, ResultForm
from app.generalFunctions import pull_comments
from datetime import datetime
from app.email import send_audit_mail

audits = Blueprint('audits', __name__)
#changed back to audit.html as the form is still not working
@audits.route("/create", methods=["GET","POST"])
def create_audit():    
    form = AuditForm()
    if form.validate_on_submit():
        part1 = [form.professionalism1.data, form.professionalism2.data, form.professionalism3.data, form.staffhygiene1.data, form.staffhygiene2.data, form.staffhygiene3.data, form.staffhygiene4.data, form.staffhygiene9.data, form.staffhygiene6.data, form.staffhygiene7.data, form.staffhygiene8.data, form.staffhygiene1.data, form.staffhygiene10.data]
        j = 0
        k = 0
        for score in part1:
            if score == "N/A":
                k +=1
            else:
                j+= int(score)
        part1_score = (j/(len(part1)-k))*0.1*100
        part2 = [form.generalenv1.data, form.generalenv2.data, form.generalenv3.data, form.generalenv4.data, form.generalenv5.data, form.generalenv6.data, form.generalenv7.data, form.generalenv8.data, form.generalenv9.data, form.generalenv10.data, form.generalenv11.data, form.generalenv12.data, form.generalenv13.data, form.generalenv14.data, form.generalenv15.data,
                    form.handhygiene1.data, form.handhygiene2.data]
        
        j = 0
        k = 0
        for score in part2:
            if score == "N/A":
                k +=1
            else:
                j+= int(score)
        part2_score = (j/(len(part2)-k))*0.2*100


        part3 = [form.storageprep1.data, form.storageprep2.data, form.storageprep3.data, form.storageprep4.data, form.storageprep5.data, form.storageprep6.data, form.storageprep7.data, form.storageprep8.data, form.storageprep9.data, form.storageprep10.data, form.storageprep12.data, form.storageprep12.data, form.storageprep13.data, form.storageprep14.data, form.storageprep15.data, form.storageprep16.data, form.storageprep17.data, form.storageprep18.data, form.storageprep19.data, form.storageprep20.data, form.storageprep21.data, form.storageprep22.data, form.storageprep23.data, form.storageprep24.data, form.storageprep25.data, form.storageprep26.data, 
                    form.storagefood1.data, form.storagefood2.data, form.storagefood3.data, form.storagefood4.data, form.storagefood5.data, form.storagefood6.data, form.storagefood7.data, form.storagefood8.data, form.storagefood9.data, form.storagefood10.data, form.storagefood11.data]
        
        j = 0
        k = 0
        for score in part3:
            if score == "N/A":
                k +=1
            else:
                j+= int(score)
        part3_score = (j/(len(part3)-k))*0.35*100

        part4 = [form.food1.data, form.food2.data, form.food3.data, form.food4.data, form.food5.data, form.food6.data, form.food7.data, 
                    form.beverage1.data, form.beverage2.data, form.beverage3.data, form.beverage4.data]
        j = 0
        k = 0
        for score in part4:
            if score == "N/A":
                k +=1
            else:
                j+= int(score)
        part4_score = (j/(len(part4)-k))*0.15*100

        part5 = [form.generalsafety1.data, form.generalsafety2.data, form.generalsafety3.data, form.generalsafety4.data, form.generalsafety5.data, form.generalsafety6.data, form.generalsafety7.data, form.generalsafety8.data, form.generalsafety9.data, form.generalsafety10.data, form.generalsafety11.data, 
                    form.fire1.data, form.fire2.data, form.fire2.data, 
                        form.elect1.data, form.elect2.data, form.elect3.data, form.elect4.data]
        
        j = 0
        k = 0
        for score in part5:
            if score == "N/A":
                k +=1
            else:
                j+= int(score)
        part5_score = (j/(len(part5)-k))*0.2*100

        total = part1_score+part2_score+part3_score+part4_score+part5_score
        audit = Audit(part1_score = int(part1_score), part2_score = int(part2_score), part3_score= int(part3_score), part4_score = int(part4_score), part5_score = int(part5_score), total_score = int(total), auditor = form.auditor.data, tenant = form.auditee.data, rectification = form.rectification.data, timestamp = datetime.now(), remarks = form.remarks.data)
        db.session.add(audit)
        db.session.commit()
        #send_audit_mail('audit/audit.html', form)
        result =  Audit.query.order_by(Audit.id.desc()).first()
        remarks = pull_comments("1", "hygiene")
        latest_audit = {result.tenant:{"PSH": result.part1_score, "HGC":result.part2_score, "FH":result.part3_score, "HEI": result.part4_score, "WSH":result.part5_score, "Total": result.total_score, "Remarks":remarks, "Due":result.rectification}}
        images = os.listdir('./app/static/images')
        return render_template("audit/audit_result.html",results = latest_audit, images = images)
        
    return render_template('audit/audit.html', form=form)

@audits.route("/comments-for-<heading>", methods=["GET"])
def audit_comments(heading):
    return render_template("audit/audit_additional_info.html", heading = heading)

@audits.route("/result/<audit_id>", methods=["GET"])
def audit_result(audit_id):
    result = Audit.query.order_by(Audit.id.desc()).first()
    remarks = pull_comments("1", "hygiene")
    audit_details = {result.tenant:{"PSH": result.part1_score, "HGC":result.part2_score, "FH":result.part3_score, "HEI": result.part4_score, "WSH":result.part5_score, "Total": result.total_score, "Remarks":remarks, "Due":result.rectification}}
    images = os.listdir('./app/static/images')
    return render_template('audit/audit_result.html', results = audit_details, images = images )



@audits.route("/view-all")
def view_audits():
    audits = {"100000":{"done":"19/05/20", "Auditor":"Tom", "non_compliance":10, "tenant":"Kopitiam"}, "100001":{"done":"21/05/20", "Auditor":"Amy", "non_compliance":2, "tenant":"Popular"}}
    return render_template("audit/view_audits.html", audits = audits)
