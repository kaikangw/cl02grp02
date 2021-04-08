import firebase_admin, json, os, requests, pprint
from firebase_admin import credentials, firestore, storage, db
from firebase_admin.auth import UserRecord
from typing import Optional
from sqlalchemy import exc, or_, and_
from app import app, db 
from app.models import Comments, User, Messages

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
        user1 = User(username = username, email = email, type = usertype)
        db.session.add(user1)
        db.session.commit()
        userid = str(user1.id)
        auth.create_user(email = email, uid = userid)
        auth.update_user(userid, password = password)
        return True
    except exc.IntegrityError:
        db.session.rollback()
        print("User already exists.")
        return False    

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
