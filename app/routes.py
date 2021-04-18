from re import I
from flask import render_template, redirect, url_for, request,session, flash, Response, send_file
import os
import pandas as pd
from io import BytesIO
from app import app, db, mail
from app.adminstrator import adminstrator
from app.audits import audits
from app.models import Audit, Messages, Comments, Broadcasts, User
from app.forms import AuditForm, ResultForm, NewForm, ShopForm, GraphForm
from datetime import datetime
from sqlalchemy import func, extract
from app.email import send_audit_mail
from app.generalFunctions import create_account, accountType, getusername, getuserid, login, send_msg, pull_msg, makeList, get_user_list

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
            

            if session['clearance'] == "admin":
                return redirect(url_for('admin.admin_page'))
        
            else:
                return redirect(url_for('main_page'))
                
        else:
            return render_template("login/login.html", alert = "Incorrect Username or Password")
    
    return render_template("login/login.html", alert = None)
    

@app.route('/main')
def main_page():
    broadcast_message = {"Auditor 1":{"title":"Reminder", "timestamp":"19:00:00", "content":"jgsdjiojfs"},"Auditor 2":{"title":"Warning", "timestamp":"20:00:00", "content":"Please comply!!"}, "Auditor 3": {"title":"Time to Eat", "timestamp":"22:00:00", "content":"Food's ready!"},"Auditor 4":{"title":"Tellonme", "timestamp":"19:00:00", "content":"hello world, I am here"},"Auditor 5":{"title":"Alert", "timestamp":"19:00:00", "content":"hello world, I am here"}}
    return render_template("main/main.html", broadcast= broadcast_message, alert=[])


#directory
@app.route('/directory',methods=['GET', 'POST'])
def directory_page():
    form = ShopForm()
    if form.validate_on_submit():
        institution = form.institution.data
        tenants = User.query.filter(User.institution==institution).order_by(User.username.asc()).all()
        tenants_list = []
        title = institution
        for t in tenants:
            tenants_list.append([t.username,t.location,t.description,t.tenancy])
        return render_template("directory/directory_1.html", title = title, tenants_list = tenants_list)
    '''
    data = {"Shop A":{"location":"#01-01", "description":"A is a pastry shop"},"Shop B":{"location":"#01-02", "description":"B is a mechanical shop"},"Shop C":{"location":"#01-03", "description":"C is a pasta shop"},"Shop D":{"location":"#01-04", "description":"D is a clothing shop"},"Shop E":{"location":"#01-05", "description":"E is a steak shop"},"Shop F":{"location":"#01-06", "description":"F is a sports shop"}}
    '''
    return render_template("directory/directory_2.html", form = form )

#chatpage
@app.route('/chat')
def chat_page():
    chat_recipients = makeList(session["userId"])
    avail_recipients = get_user_list(session["userId"])
    return render_template("chat/chat_main.html", chatRecipients = chat_recipients, availRecipients = avail_recipients)

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
        myid = session["userId"]
        send_msg(myid,currentFriend,msg)
        return redirect(url_for("chat", user=getusername(currentFriend)))
    
@app.route('/new_chat', methods=["GET", "POST"])
def create_chat():
    if request.method=="POST":
        recipient = request.form["availRecipients"]
        message = request.form.get("message")
        send_msg(session["userId"], getuserid(recipient), message)
        return redirect(url_for("chat", user=recipient))
    
#settings
@app.route('/settings')
def settings():
    session.pop('username')
    session.pop('clearance')
    return render_template("login/login.html")



@app.route('/data', methods=['GET', 'POST'])
def data_page():
    #if check_admin():
    
    form = ResultForm()
    if form.validate_on_submit():
        option = form.option.data
        if  option == 'tenant':
            title = "TOP 5 WORST PERFORMNG TENANTS"
            month = datetime.now().month
            tenants = Audit.query.filter(extract('month',Audit.timestamp)==month).order_by(Audit.total_score.asc()).all()
            tenants = tenants[1:6]
            tenant_list = []
            for tenant in tenants:
                t = {'score':tenant.total_score,'tenant':tenant.tenant}
                tenant_list.append(t)
            return render_template("audit/compare.html",tenants = tenant_list, title = title)  

        elif option == 'individual':
            title = "TOP 5 WORST PERFORMNG INDIVIDUAL SCORES"
            part1 = "Professionalism & Staff Hygiene"
            part2 = "Housekeeping & General Cleanliness"
            part3 = "Food Hygiene"
            part4 = "Healthier Choice in line with HPB’s Healthy Eating’s Initiative "
            part5 = "Workplace Safety & Health  "
            month = datetime.now().month
            tenants_part1 = Audit.query.filter(extract('month',Audit.timestamp)==month).order_by(Audit.part1_score.asc(),Audit.tenant.asc()).all()
            tenants_part2 = Audit.query.filter(extract('month',Audit.timestamp)==month).order_by(Audit.part2_score.asc(),Audit.tenant.asc()).all()
            tenants_part3 = Audit.query.filter(extract('month',Audit.timestamp)==month).order_by(Audit.part3_score.asc(),Audit.tenant.asc()).all()
            tenants_part4 = Audit.query.filter(extract('month',Audit.timestamp)==month).order_by(Audit.part4_score.asc(),Audit.tenant.asc()).all()           
            tenants_part5 = Audit.query.filter(extract('month',Audit.timestamp)==month).order_by(Audit.part5_score.asc(),Audit.tenant.asc()).all()
            tenants_part1 = tenants_part1[1:6]
            tenants_part2 = tenants_part2[1:6]
            tenants_part3 = tenants_part3[1:6]
            tenants_part4 = tenants_part4[1:6]
            tenants_part5 = tenants_part5[1:6]
            tenant_list1 = []
            tenant_list2 = []
            tenant_list3 = []
            tenant_list4 = []
            tenant_list5 = []
            for tenant in tenants_part1:
                t1 = {'score':tenant.part1_score,'tenant':tenant.tenant}
                tenant_list1.append(t1)            
            for tenant in tenants_part2:
                t2 = {'score':tenant.part2_score,'tenant':tenant.tenant}
                tenant_list2.append(t2)            
            for tenant in tenants_part3:
                t3 = {'score':tenant.part3_score,'tenant':tenant.tenant}
                tenant_list3.append(t3)            
            for tenant in tenants_part4:
                t4 = {'score':tenant.part4_score,'tenant':tenant.tenant}
                tenant_list4.append(t4)           
            for tenant in tenants_part5:
                t5 = {'score':tenant.part5_score,'tenant':tenant.tenant}
                tenant_list5.append(t5)
            return render_template("audit/individual.html", title = title, part1 = part1, part2 = part2, part3 = part3, part4 = part4, part5 = part5,tenant_list1=tenant_list1,tenant_list2=tenant_list2,tenant_list3=tenant_list3,tenant_list4=tenant_list4,tenant_list5=tenant_list5)  

        elif option == 'institution':
            title1 = "CGH"
            title2 = "KKH"
            title3 = "SGH"
            title4 = "SKH"
            cgh = []
            kkh = []
            sgh = []
            skh = []
            month = datetime.now().month
            audits = Audit.query.filter(extract('month',Audit.timestamp)==month).order_by(Audit.total_score.asc(),Audit.tenant.asc()).all()
            audits = audits[1:]
            for a in audits:
                tenant = a.tenant
                user = User.query.filter(User.username == tenant).first()
                if user.institution == title1:
                    if len(cgh)== 5:
                        break
                    cgh.append([tenant,a.total_score])
                if user.institution == title2:
                    if len(kkh )== 5:
                        break
                    kkh.append([tenant,a.total_score])
                if user.institution == title3:
                    if len(sgh) == 5:
                        break
                    sgh.append([tenant,a.total_score])
                if user.institution== title4:
                    if len(skh) == 5:
                        break
                    skh.append([tenant,a.total_score])
            return render_template("institution_compare.html", title1=title1, title2=title2, title3=title3, title4=title4, cgh = cgh, kkh = kkh, sgh = sgh, skh = skh)

    return render_template("data.html", form=form)

@app.route('/data/individual', methods=['GET', 'POST'])
def data_individual():
    form = GraphForm()
    '''
    if form.validate_on_submit():
        option = form.auditee.data
        tenants = Audit.query.filter(Audit.tenant=="kopitiam").order_by(Audit.timestamp.asc()).all()    
        score = []
        for tenant in tenants:
            score.append(tenant.total_score)
'''

    return render_template('individual.html', form=form)

@app.route('/search_query', methods=['GET', 'POST'])
def search_query():
    tenant_name = request.form['auditee']
    tenants = Audit.query.filter(Audit.tenant==tenant_name).order_by(Audit.timestamp.asc()).all()    
    score = []
    for tenant in tenants:
        if len(score) == 12:
            break
        score.append(tenant.total_score)
    return {'tenant':score, 'tenant_name':tenant_name}

@app.route('/data/frequency', methods=['GET', 'POST'])
def data_frequency():
    form = NewForm()
    if form.validate_on_submit():
        auditor = form.auditor.data
        auditor = Audit.query.filter(Audit.auditor==auditor).order_by(Audit.timestamp.desc()).all() 
        month = datetime.now().month
        auditor_dict = []
        audit_list = []   
        small_list = []
        for a in auditor:
            if a.timestamp.month != month :
                small_list.append(month)
                month = a.timestamp.month
                auditor_dict.append( audit_list)
                audit_list = []
                if a == auditor[len(auditor)-1]:
                    audit_list.append([a.tenant,a.timestamp])
                    month = a.timestamp.month
                    small_list.append(month)
                    auditor_dict.append( audit_list)
                    break
            audit_list.append([a.tenant,a.timestamp])
        return render_template("auditor_data.html", auditor = auditor_dict, title = form.auditor.data ) 

    title1 = "CGH"
    title2 = "KKH"
    title3 = "SGH"
    title4 = "SKH"
    cgh = []
    kkh = []
    sgh = []
    skh = []
    month = datetime.now().month
    audits = Audit.query.filter(extract('month',Audit.timestamp)==month).order_by(Audit.timestamp.desc()).all()
    audits = audits[:-1]
    for a in audits:
        tenant = a.tenant
        user = User.query.filter(User.username == tenant).first()
        if user.institution == title1:
            cgh.append([a.timestamp,a.auditor, a.tenant])
        if user.institution == title2:
            kkh.append([a.timestamp,a.auditor, a.tenant])
        if user.institution == title3:
            sgh.append([a.timestamp,a.auditor, a.tenant])
        if user.institution== title4:
            skh.append([a.timestamp,a.auditor, a.tenant])

    return render_template("frequency.html", form = form, title1=title1, title2=title2, title3=title3, title4=title4, cgh = cgh, kkh = kkh, sgh = sgh, skh = skh)

'''

    return render_template("data.html", form=form)
    
    else:
        alert = ["You don't have the clearance to view this!"]
        broadcast_message = {"Auditor 1":{"title":"Reminder", "timestamp":"19:00:00", "content":"jgsdjiojfs"},
            "Auditor 2":{"title":"Warning", "timestamp":"20:00:00", "content":"Please comply!!"}, 
            "Auditor 3": {"title":"Time to Eat", "timestamp":"22:00:00", "content":"Food's ready!"},
            "Auditor 4":{"title":"Tellonme", "timestamp":"19:00:00", "content":"hello world, I am here"},
            "Auditor 5":{"title":"Alert", "timestamp":"19:00:00", "content":"hello world, I am here"}}
            
        return render_template("main/main.html",broadcast= broadcast_message, alert = alert)'''

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

#broadcast message
@app.route('/create_broadcast', methods=["GET","POST"])
def create_broadcast():

    if request.method == "POST":
        recipient = request.form["broadcastTo"]
        print(recipient)
        broadcast = request.form["broadcastMsg"]
        print(broadcast)
        render_template("broadcast/broadcast.html")
    return render_template("broadcast/broadcast.html")



@app.route('/download', methods=["GET","POST"])
def download():
    month = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
    tenant_name = request.form['auditee']
    tenants = Audit.query.filter(Audit.tenant==tenant_name).order_by(Audit.timestamp.asc()).all()    
    result = []
    for tenant in tenants:
        if len(result) == 12:
            break
        result.append(tenant.total_score)
        

    data = []
    for i in range(len(month)):
        data.append([month[i], result[i]])
    df_1 = pd.DataFrame(data, columns=["Month", "Result"])

    #create an output stream
    output = BytesIO()
    writer = pd.ExcelWriter(output, engine='xlsxwriter')

    #taken from the original question
    df_1.to_excel(writer, startrow = 0,merge_cells = False, sheet_name = "Sheet_1", index=False)
    workbook = writer.book
    worksheet = writer.sheets["Sheet_1"]

    #the writer has done its job
    writer.close()

    #go back to the beginning of the stream
    output.seek(0)

    #finally return the file
    return send_file(output, attachment_filename="data.xlsx", as_attachment=True)



#blueprints
app.register_blueprint(adminstrator, url_prefix="/admin")
app.register_blueprint(audits, url_prefix="/audits")