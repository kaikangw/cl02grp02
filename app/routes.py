from re import I
from flask import render_template, redirect, url_for, request,session, flash
import os
from app import app, db, mail
from app.adminstrator import adminstrator
from app.audits import audits
from app.models import Audit, Messages, Comments, Broadcasts, User
from app.forms import AuditForm, ResultForm
from datetime import datetime
from sqlalchemy import func, extract
from app.email import send_audit_mail
from app.generalFunctions import create_account, accountType, getusername, getuserid, login, send_msg, pull_msg, makeList

#Images Folder
UPLOAD_FOLDER = os.path.join('static','images')
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
currentFriend = 0

def check_admin():
    if session["clearance"] != "tenant":
        return True

#route for home
@app.route('/', methods=["GET", "POST"])
def login_page():

    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        token = login(username,password)
        user_id = token.get("localId")
        if( user_id is not None ):
            ##query database to check
            session['userId'] = user_id
            session['username'] = getusername(user_id)
            session['clearance'] = accountType(user_id).strip()
            print(session['clearance'])

            if session['clearance'] == "admin":
                print("is admin")
                return redirect(url_for('admin.admin_page'))
        
            else:
                print("ran this")
                return redirect(url_for('main_page'))
        else:
            return render_template("login/login.html", alert = "Incorrect Username or Password")
    
    return render_template("login/login.html", alert = None)
    

@app.route('/main')
def main_page():
    broadcast_message = {"Auditor 1":{"title":"Reminder", "timestamp":"19:00:00", "content":"jgsdjiojfs"},"Auditor 2":{"title":"Warning", "timestamp":"20:00:00", "content":"Please comply!!"}, "Auditor 3": {"title":"Time to Eat", "timestamp":"22:00:00", "content":"Food's ready!"},"Auditor 4":{"title":"Tellonme", "timestamp":"19:00:00", "content":"hello world, I am here"},"Auditor 5":{"title":"Alert", "timestamp":"19:00:00", "content":"hello world, I am here"}}
    return render_template("main/main.html", broadcast= broadcast_message, alert=[])


#directory
@app.route('/directory')
def directory_page():
    data = {"Shop A":{"location":"#01-01", "description":"A is a pastry shop"},"Shop B":{"location":"#01-02", "description":"B is a mechanical shop"},"Shop C":{"location":"#01-03", "description":"C is a pasta shop"},"Shop D":{"location":"#01-04", "description":"D is a clothing shop"},"Shop E":{"location":"#01-05", "description":"E is a steak shop"},"Shop F":{"location":"#01-06", "description":"F is a sports shop"}}
    return render_template("directory/directory_1.html", data=data)

#chatpage
@app.route('/chat')
def chat_page():
    chat_recipients = makeList(session["userId"])
    print(chat_recipients)
    return render_template("chat/chat_main.html", chatRecipients = chat_recipients)

@app.route('/chat/<user>', methods=["POST", "GET"])
def chat(user):
    global currentFriend
    #query for particular recipient
    my_id = session["userId"]
    friend = getuserid(user)
    currentFriend = friend
    message = pull_msg(my_id, friend)
    for k in message:
        k["currentUser"] = session["username"]
    return render_template("chat/chat_private.html", chatContent = message, me = session["username"], convoPartner = user )
    

@app.route('/update', methods=["POST"])
def update_chat():
    if request.method == "POST":
        msg = request.form['message']
        id = session["userId"]
        send_msg(id,currentFriend,msg)
        return redirect(url_for("chat", user=getusername(currentFriend)))
    
#settings
@app.route('/settings')
def settings():
    session.pop('username')
    session.pop('clearance')
    return render_template("login/login.html")


# ajax request url
@app.route('/search_query', methods=['GET', 'POST'])
def search_query():
    auditor1 = request.form['auditee1']
    auditor2 = request.form['auditee2']
    result1 = Audit.query.filter_by(auditor=auditor1)
    result2 = Audit.query.filter_by(auditor=auditor2)
    mo = []
    for data in result1:
        datetime_in_data = str(data.timestamp)
        dates_data = datetime_in_data.split(' ')
        m = dates_data[0].split('-')
        mo.append(m[1])
    months = []
    for data in result2:
        datestime_in_data = str(data.timestamp)
        dates_in_data = datestime_in_data.split(' ')
        month = dates_in_data[0].split('-')
        months.append(month[1])
    print(mo)
    print(months)
    audtr1 = []
    audtr2 = []
    if '01' in mo:
        ts = Audit.query.filter(extract('month', Audit.timestamp) == 1).order_by(Audit.id.desc()).first()
        audtr1.append(ts.total_score)

    else:
        audtr1.append(0)

    if '02' in mo:
        ts = Audit.query.filter(extract('month', Audit.timestamp) == 2).order_by(Audit.id.desc()).first()
        audtr1.append(ts.total_score)

    else:
        audtr1.append(0)

    if '03' in mo:
        ts = Audit.query.filter(extract('month', Audit.timestamp) == 3).order_by(Audit.id.desc()).first()
        audtr1.append(ts.total_score)

    else:
        audtr1.append(0)

    if '04' in mo:
        ts = Audit.query.filter(extract('month', Audit.timestamp) == 4).order_by(Audit.id.desc()).first()
        audtr1.append(ts.total_score)

    else:
        audtr1.append(0)

    if '05' in mo:
        ts = Audit.query.filter(extract('month', Audit.timestamp) == 5).order_by(Audit.id.desc()).first()
        audtr1.append(ts.total_score)

    else:
        audtr1.append(0)

    if '06' in mo:
        ts = Audit.query.filter(extract('month', Audit.timestamp) == 6).order_by(Audit.id.desc()).first()
        audtr1.append(ts.total_score)

    else:
        audtr1.append(0)

    if '07' in mo:
        ts = Audit.query.filter(extract('month', Audit.timestamp) == 7).order_by(Audit.id.desc()).first()
        audtr1.append(ts.total_score)

    else:
        audtr1.append(0)

    if '08' in mo:
        ts = Audit.query.filter(extract('month', Audit.timestamp) == 8).order_by(Audit.id.desc()).first()
        audtr1.append(ts.total_score)

    else:
        audtr1.append(0)

    if '09' in mo:
        ts = Audit.query.filter(extract('month', Audit.timestamp) == 9).order_by(Audit.id.desc()).first()
        audtr1.append(ts.total_score)

    else:
        audtr1.append(0)

    if '10' in mo:
        ts = Audit.query.filter(extract('month', Audit.timestamp) == 10).order_by(Audit.id.desc()).first()
        audtr1.append(ts.total_score)
    else:
        audtr1.append(0)

    if '11' in mo:
        ts = Audit.query.filter(extract('month', Audit.timestamp) == 11).order_by(Audit.id.desc()).first()
        audtr1.append(ts.total_score)
    else:
        audtr1.append(0)

    if '12' in mo:
        ts = Audit.query.filter(extract('month', Audit.timestamp) == 12).order_by(Audit.id.desc()).first()
        audtr1.append(ts.total_score)
    else:
        audtr1.append(0)


    if '01' in months:
        ts = Audit.query.filter(extract('month', Audit.timestamp) == 1).order_by(Audit.id.desc()).first()
        audtr2.append(ts.total_score)

    else:
        audtr2.append(0)

    if '02' in months:
        ts = Audit.query.filter(extract('month', Audit.timestamp) == 2).order_by(Audit.id.desc()).first()
        audtr2.append(ts.total_score)

    else:
        audtr2.append(0)

    if '03' in months:
        ts = Audit.query.filter(extract('month', Audit.timestamp) == 3).order_by(Audit.id.desc()).first()
        audtr2.append(ts.total_score)

    else:
        audtr2.append(0)

    if '04' in months:
        ts = Audit.query.filter(extract('month', Audit.timestamp) == 4).order_by(Audit.id.desc()).first()
        audtr2.append(ts.total_score)

    else:
        audtr2.append(0)

    if '05' in months:
        ts = Audit.query.filter(extract('month', Audit.timestamp) == 5).order_by(Audit.id.desc()).first()
        audtr2.append(ts.total_score)

    else:
        audtr2.append(0)

    if '06' in months:
        ts = Audit.query.filter(extract('month', Audit.timestamp) == 6).order_by(Audit.id.desc()).first()
        audtr2.append(ts.total_score)

    else:
        audtr2.append(0)

    if '07' in months:
        ts = Audit.query.filter(extract('month', Audit.timestamp) == 7).order_by(Audit.id.desc()).first()
        audtr2.append(ts.total_score)

    else:
        audtr2.append(0)

    if '08' in months:
        ts = Audit.query.filter(extract('month', Audit.timestamp) == 8).order_by(Audit.id.desc()).first()
        audtr2.append(ts.total_score)

    else:
        audtr2.append(0)

    if '09' in months:
        ts = Audit.query.filter(extract('month', Audit.timestamp) == 9).order_by(Audit.id.desc()).first()
        audtr2.append(ts.total_score)

    else:
        audtr2.append(0)

    if '10' in months:
        ts = Audit.query.filter(extract('month', Audit.timestamp) == 10).order_by(Audit.id.desc()).first()
        audtr2.append(ts.total_score)
    else:
        audtr2.append(0)

    if '11' in months:
        ts = Audit.query.filter(extract('month', Audit.timestamp) == 11).order_by(Audit.id.desc()).first()
        audtr2.append(ts.total_score)
    else:
        audtr2.append(0)

    if '12' in months:
        ts = Audit.query.filter(extract('month', Audit.timestamp) == 12).order_by(Audit.id.desc()).first()
        audtr2.append(ts.total_score)
    else:
        audtr2.append(0)

    return {'audtr1':audtr1, 'audtr2':audtr2, 'auditor1_name':auditor1, 'auditor2_name':auditor2}

@app.route('/data', methods=['GET', 'POST'])
def data_page():
    if check_admin():
        form = ResultForm()
        return render_template("data.html", form=form)
    else:
        alert = ["You don't have the clearance to view this!"]
        broadcast_message = {"Auditor 1":{"title":"Reminder", "timestamp":"19:00:00", "content":"jgsdjiojfs"},
            "Auditor 2":{"title":"Warning", "timestamp":"20:00:00", "content":"Please comply!!"}, 
            "Auditor 3": {"title":"Time to Eat", "timestamp":"22:00:00", "content":"Food's ready!"},
            "Auditor 4":{"title":"Tellonme", "timestamp":"19:00:00", "content":"hello world, I am here"},
            "Auditor 5":{"title":"Alert", "timestamp":"19:00:00", "content":"hello world, I am here"}}
            
        return render_template("main/main.html",broadcast= broadcast_message, alert = alert)

@app.route('/saved', methods=['GET', 'POST'])
def saved_audit():
    audit = Audit.query.all()
    dates = []
    for data in audit:
        date = str(data.timestamp)
        date = date.split(' ')
        date = date[0]
        d = {'date':date, 'auditor':data.auditor, 'tenant': data.tenant}
        dates.append(d)
    return render_template("saved_audit.html", dates=dates)


#blueprints
app.register_blueprint(adminstrator, url_prefix="/admin")
app.register_blueprint(audits, url_prefix="/audits")