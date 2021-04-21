import firebase_admin, json, os, requests, pprint
from firebase_admin import credentials, firestore, storage, db, auth
from firebase_admin.auth import UserRecord
from typing import Optional
from sqlalchemy import exc, or_, and_
from app import app, db 
from app.models import Comments, User, Messages, Broadcasts

FIREBASE_WEB_API_KEY = "AIzaSyBXCtNbzv8EOVmvl4TVnsWmKLU5RYNF__8"
rest_api_url = f"https://identitytoolkit.googleapis.com/v1/accounts:signInWithPassword"

#Initialize Firebase Application
def initialize():
    try:
        app = firebase_admin.get_app()
        print("app exists")
    except ValueError as e:
        cred=credentials.Certificate("app\Firebase_Service_Account_Key.json")
        firebase_admin.initialize_app(cred, {
            'storageBucket': 'ezcheck-aa2cc.appspot.com',
            'databaseURL': 'https://ezcheck-aa2cc-default-rtdb.firebaseio.com/'
        })
        print("app initialized")

#Adminstrator
##Account Creation
def create_account(username: str, email: str, usertype: str, password:str):
    initialize()
    try:
        auth.create_user(email = email, uid = userid)
        auth.update_user(userid, password = password)
        user1 = User(username = username, email = email, type = usertype)
        db.session.add(user1)
        db.session.commit()
        userid = str(user1.id)
        return True
    except exc.IntegrityError:
        db.session.rollback()
        print("User already exists.")
        return False 

##Account Edit
def get_alluser_list():
    name_list = []
    query = User.query.all()
    for x in query:
        name_list.append(x.username)
    return name_list

def get_user_details(username: str):
    user = User.query.filter(User.username == username).first()
    dic = {
        "User ID" : user.id,
        "Username" : username,
        "Email" : user.email,
        "Type" : user.type,
        "Institution" : user.institution,
        "Tenancy" : user.tenancy,
        "Description" : user.description,
        "Location" : user.location
    }
    return dic

def change_details(userid:int, username: str,  email: str, accountType:str, instituition:str, tenancy:int, description:str, location:str, password:str):
    initialize()
    print(userid)
    user = User.query.get(userid)
    user.tenancy = tenancy
    user.instituition = instituition
    user.location = location
    user.type = accountType
    user.description = description
    user.username = username
    auth.update_user(str(userid), email = email)
    if password:
        print("password isn't empty")
        auth.update_user(str(userid), password = password)
    db.session.commit()
    

##Account Deletion   
def delete_user(user_id: int):
    initialize()
    user = User.query.get(user_id)
    db.session.delete(user)
    db.session.commit()
    auth.delete_user(str(user_id))

##Broadcasts
def new_broadcast(senderid: int, receivertype: str, body: str):
    broadcast = Broadcasts(sender_id = senderid, receiver_type = receivertype, body = body)
    db.session.add(broadcast)
    db.session.commit()

def get_broadcast_list(receivertype: str):
    broadcast_list = []
    query = Broadcasts.query.filter(db.or_(Broadcasts.receiver_type == receivertype, Broadcasts.receiver_type == "both")).order_by(Broadcasts.timestamp)
    for broadcast in query:
        date_time = broadcast.timestamp.strftime("%m/%d/%Y, %H:%M:%S")
        senderName = User.query.get(broadcast.sender_id).username
        details = {"timestamp" : date_time,
                    "senderName" : senderName,
                    "content" : broadcast.body}
        broadcast_list.append(details)
    
    return broadcast_list

#Main

##Getters

def accountType(userid):
    t = User.query.get(userid).type
    return t

def getusername(userid):
    name = User.query.get(userid).username
    return name 

def getuserid(username):
    print(username) 
    thisid = User.query.filter(User.username == username).first()
    return thisid.id

def getinstitution(username):
    user = User.query.filter(User.username == username).first()
    return user.institution

def gettenancy(username):
    user = User.query.filter(User.username == username).first()
    return user.tenancy

##Login
def login(email: str, password: str, return_secure_token: bool = True):
    payload = json.dumps({
        "email": email,
        "password": password,
        "returnSecureToken": return_secure_token
    })

    r = requests.post(rest_api_url,
                      params={"key": FIREBASE_WEB_API_KEY},
                      data=payload)
    return r.json()

##Chat Function

###Messages
def send_msg(senderid, recipientid, body):
    msg = Messages(sender_id = senderid, recipient_id = recipientid, body = body)    
    db.session.add(msg)
    db.session.commit() 


def pull_msg(my_id: int, their_id: int):
    query = Messages.query.filter(db.or_(db.and_(Messages.sender_id == my_id, Messages.recipient_id == their_id), db.and_(Messages.sender_id == their_id, Messages.recipient_id == my_id))).order_by(Messages.timestamp)
    convo = []
    for i in query:
        date_time = i.timestamp.strftime("%m/%d/%Y, %H:%M:%S")
        senderName = User.query.get(i.sender_id).username
        msg = {"timestamp":date_time, "senderId": senderName, "content":i.body }
        convo.append(msg)
    
    return convo

def makeList(userid: int):
    print("reached user id")
    print(userid)
    output = []
    checksender = Messages.query.filter(Messages.sender_id == userid)
    for message in checksender:
        my_name = User.query.get(message.recipient_id).username
        if (my_name not in output) and (message.recipient_id != message.sender_id):
            name = User.query.get(message.recipient_id).username
            output.append(name)
    checkreceiver = Messages.query.filter(Messages.recipient_id == userid)
    for message in checkreceiver:
        my_name = User.query.get(message.sender_id).username
        if (my_name not in output) and (message.sender_id != message.recipient_id):
            name = User.query.get(message.sender_id).username
            output.append(name)
    return output

###NewChat
def get_user_list(current_user_id: int):
    name_list = []
    query = User.query.all()
    for x in query:
        if (x.id != current_user_id):
            name_list.append(x.username)
    return name_list


##Audits

###Audit Results - Comments

def pull_comments(auditid: int, section: str):
    remarks = []
    for comment in Comments.query.filter(db.and_(Comments.audit_id == auditid, Comments.section == section)).order_by(Comments.path):
        print("{}{}: {}".format('    '*comment.level(), comment.sender_id, comment.body))

        m = {}
        m["senderId"] = getusername(comment.sender_id)
        m["comment"] = comment.body
        m["level"] = comment.level()
        remarks.append(m)

    return remarks
