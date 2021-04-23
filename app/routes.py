from re import I
from flask import render_template, redirect, url_for, request,session, flash, Response, send_file
import os
from os.path import join, dirname, realpath
import pandas as pd
from io import BytesIO
from app import app, db, mail
from app.adminstrator import adminstrator
from app.models import Audit, Messages, Comments, Broadcasts, User
from app.forms import AuditForm, ResultForm, NewForm, ShopForm, GraphForm
from datetime import datetime
from sqlalchemy import func, extract
from app.email import send_audit_mail
from app.generalFunctions import create_account, accountType, getusername, getuserid, login, send_msg, pull_msg, makeList, get_user_list, new_broadcast, get_broadcast_list, getinstitution, gettenancy, add_to_database, upload_image, pull_comments,get_images, getaudits, getTenants, auditTenant, getTaudits

#Images Folder
UPLOAD_FOLDER = join(dirname(realpath(__file__)), 'static','images')
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
    #broadcast_message = {"Auditor 1":{"title":"Reminder", "timestamp":"19:00:00", "content":"jgsdjiojfs"},"Auditor 2":{"title":"Warning", "timestamp":"20:00:00", "content":"Please comply!!"}, "Auditor 3": {"title":"Time to Eat", "timestamp":"22:00:00", "content":"Food's ready!"},"Auditor 4":{"title":"Tellonme", "timestamp":"19:00:00", "content":"hello world, I am here"},"Auditor 5":{"title":"Alert", "timestamp":"19:00:00", "content":"hello world, I am here"}}
    broadcast_message = get_broadcast_list(session["clearance"])
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
    user = session["username"]
    uid = session["userId"]
    clearance = session["clearance"]
    institution = getinstitution(user)
    
    if clearance == "tenant":
        tenancy = gettenancy(user)
    else:
        tenancy = "NIL"

    return render_template("main/settings.html", user = user, uid = uid, clearance = clearance, institution = institution, tenancy = tenancy)
    #return render_template("main/settings.html", user = user, uid = uid, clearance = clearance)

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
            part1 = "Professionalism & Staff Hygiene 10"
            part2 = "Housekeeping & General Cleanliness 20"
            part3 = "Food Hygiene 35"
            part4 = "Healthier Choice in line with HPB’s Healthy Eating’s Initiative 25"
            part5 = "Workplace Safety & Health  20"
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
        if len(score) == 4:
            break
        score.append(tenant.total_score)
    return {'tenant':score, 'tenant_name':tenant_name}

@app.route('/data/frequency', methods=['GET', 'POST'])
def data_frequency():
    
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
        user = User.query.filter(User.username == a.tenant).first()
        if user.institution == title1:
            cgh.append([a.timestamp,a.auditor, a.tenant])
        if user.institution == title2:
            kkh.append([a.timestamp,a.auditor, a.tenant])
        if user.institution == title3:
            sgh.append([a.timestamp,a.auditor, a.tenant])
        if user.institution== title4:
            skh.append([a.timestamp,a.auditor, a.tenant])

    return render_template("frequency.html",  title1=title1, title2=title2, title3=title3, title4=title4, cgh = cgh, kkh = kkh, sgh = sgh, skh = skh)


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
        broadcast = request.form["broadcastMsg"]
        new_broadcast(session["userId"], recipient, broadcast)

        render_template("broadcast/broadcast.html")
    return render_template("broadcast/broadcast.html")



@app.route('/download', methods=["GET","POST"])
def download():
    month = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
    tenant_name = request.form['auditee']
    tenants = Audit.query.filter(Audit.tenant==tenant_name).order_by(Audit.timestamp.asc()).all()    
    result = []
    for tenant in tenants:
        if len(result) >= 4 and len(result)<13:
            result.append(0)
        elif len(result) >11:
            break
        else:
            result.append(tenant.total_score)
        

    data = []
    for i in range(len(month)):
        data.append([month[i], result[i]])
        if i == (len(result)-1):
            break
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


##Audits

@app.route("/choose", methods=["GET", "POST"])
def choose_tenant():
    tenants = getTenants()

    if request.method == "POST":
        #initialise the sessions
        tags = ["PSH", "HGC", "FH", "HC", "WSH"]

        for t in tags:
            session[t] = {"section":t, "images":"", "comments":"No Comment"}

        tenant = request.form.get("availTenants")
        session["currentT"] = tenant
        return redirect(url_for("create_audit"))

    return render_template("audit/chooseTenant.html", tenants= tenants)

@app.route("/create", methods=["GET","POST"])
def create_audit():    
    form = AuditForm()
    auditor = session["username"]
    tenant = session["currentT"]
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
        audit = Audit(part1_score = int(part1_score), part2_score = int(part2_score), part3_score= int(part3_score), part4_score = int(part4_score), part5_score = int(part5_score), total_score = int(total), auditor = auditor, tenant = tenant, rectification = form.rectification.data, timestamp = datetime.now(), remarks = form.remarks.data)
        db.session.add(audit)
        db.session.commit()
        send_audit_mail('audit/audit_w.html', form)
        result =  Audit.query.order_by(Audit.id.desc()).first()

        PSH = session["PSH"]
        HGC = session["HGC"]
        FH = session["FH"]
        HC = session["HC"]
        WSH = session["WSH"]

        auditorId = session["userId"]
        tenantId = getuserid(tenant)

        PSH_additional = add_to_database(audit.id, PSH.get("comments"), "PSH", PSH.get("images"), auditorId, tenantId)
        HGC_additional = add_to_database(audit.id, HGC.get("comments"), "HGC", HGC.get("images"), auditorId, tenantId)
        FH_additional = add_to_database(audit.id, FH.get("comments"), "FH", FH.get("images"), auditorId, tenantId)
        HC_additional = add_to_database(audit.id, HC.get("comments"), "HC", HC.get("images"), auditorId, tenantId)
        WSH_additional = add_to_database(audit.id, WSH.get("comments"), "WSH", WSH.get("images"), auditorId, tenantId)

        upload_image(audit.id, PSH.get("section"), PSH_additional, PSH.get("images"))
        upload_image(audit.id, HGC.get("section"), HGC_additional, HGC.get("images"))
        upload_image(audit.id, FH.get("section"), FH_additional, FH.get("images"))
        upload_image(audit.id, HC.get("section"), HC_additional, HC.get("images"))
        upload_image(audit.id, WSH.get("section"), WSH_additional, WSH.get("images"))

        section_list = ["PSH","HGC","FH","HC","WSH"]
        remarks_list = {}
        for section in section_list:
            remarks = pull_comments(result.id, section)
            remarks_list.update({section:remarks})
 
        latest_audit = {tenant:{"PSH": result.part1_score, "HGC":result.part2_score, "FH":result.part3_score, "HEI": result.part4_score, "WSH":result.part5_score, "Total": result.total_score, "Remarks":remarks_list, "Due":result.rectification}}

        image_list = {}

        for section in section_list:
            images = get_images(result.id, section)
            image_list.update({section: images})
        
        return render_template("audit/audit_result.html",results = latest_audit, images = image_list, remarks = remarks_list, sections = section_list)
        
    return render_template('audit/audit_w.html', form=form, auditor = auditor, tenant = tenant,)

@app.route("/comments-for-<heading>", methods=["GET", "POST"])
def audit_comments(heading):
    #Making information to be passed
    section = {"Professionalism & Staff Hygiene":"PSH", "Housekeeping & General Cleanliness":"HGC", "Food Hygiene":"FH", "Healthier Choice":"HC","Workplace Safety & Health":"WSH"}
    
    if request.method == "POST":
        images_list = request.files.getlist("files")
        comments = request.form["audit-comments"]   
        images_path = []
        images_names = []
        info = {"section":section.get(heading), "images":"", "comments":"No Comment"}

        if images_list:
            for each in images_list:
                if each.filename != '':
                    images_names.append(each.filename)
                    path = os.path.join(app.config['UPLOAD_FOLDER'], each.filename)
                    images_path.append(path)
                    each.save(path)
                
        info["images"] = images_path
        info["comments"] = comments
        session[section.get(heading)] = info

        return redirect(url_for("create_audit"))

    return render_template("audit/audit_additional_info.html", heading = heading)
    

@app.route("/result/<audit_id>", methods=["GET", "POST"])
def audit_result(audit_id):
    result = Audit.query.get(audit_id)
    section_list = ["PSH","HGC","FH","HC","WSH"]
    remarks_list = {}
    for section in section_list:
        remarks = pull_comments(result.id, section)
        remarks_list.update({section:remarks})
       
    audit_details = {result.tenant:{"PSH": result.part1_score, "HGC":result.part2_score, "FH":result.part3_score, "HEI": result.part4_score, "WSH":result.part5_score, "Total": result.total_score, "Remarks":remarks_list, "Due":result.rectification}}
   
    image_list = {}

    for section in section_list:
        images = get_images(result.id, section)
        image_list.update({section: images})

    if request.method == "POST":
        section = request.form["sectionComment"]
        images_list = request.files.getlist("files")
        comments = request.form["audit-comments"]   
        images_path = []
        images_names = []
        if images_list:
            for each in images_list:
                if each.filename != '':
                    images_names.append(each.filename)
                    path = os.path.join(app.config['UPLOAD_FOLDER'], each.filename)
                    images_path.append(path)
                    each.save(path)
                
        cid = add_to_database(audit_id, comments, section, images_path, session["userId"], auditTenant(audit_id))
 
        upload_image(audit_id, section, cid, images_path)
        return redirect(url_for("audit_result", audit_id = audit_id))

    return render_template('audit/audit_result.html', results = audit_details, images = image_list, remarks = remarks_list, sections = section_list, audit_id = audit_id )


@app.route("/view-all")
def view_audits():
    if session["clearance"] == "tenant":
        audits = getTaudits(session["username"])

    else:
        audits = getaudits()

    return render_template("audit/view_audits.html", audits = audits)


#blues
app.register_blueprint(adminstrator, url_prefix="/admin")
