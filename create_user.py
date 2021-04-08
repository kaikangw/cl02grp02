import argparse
from typing import Optional

import firebase_admin
from firebase_admin import auth, credentials
from firebase_admin.auth import UserRecord

from app import app, db
from app.models import User
from sqlalchemy import exc

def initialize():
    try:
        app = firebase_admin.get_app()
        print("app exists")
    except ValueError as e:
        cred=credentials.Certificate('Firebase_Service_Account_Key.json')
        firebase_admin.initialize_app(cred, {
            'storageBucket': 'ezcheck-aa2cc.appspot.com',
            'databaseURL': 'https://ezcheck-aa2cc-default-rtdb.firebaseio.com/'
        })
        print("app initialized")

userid = "0"

def get_email_arg():
    parser = argparse.ArgumentParser(description="Create a new user")
    parser.add_argument("--username", required=True, help="Username of the user to be created")
    parser.add_argument("--email", required=True, help="The email address of the user to be created")
    parser.add_argument("--user-type", required=True, help="Tenant/Auditor/Admin")
    parser.add_argument("--password", required = True, help="Password")
    return parser.parse_args()

def create_user(username: str, email: str, usertype: str):
    try:
        user1 = User(username = username, email = email, type = usertype)
        db.session.add(user1)
        db.session.commit()
        return True
    except exc.IntegrityError:
        db.session.rollback()
        print("User already exists.")
        return False    
    global userid
    userid = user1.id

def create_firebase_user(email: str) -> UserRecord:
    return auth.create_user(email=email, uid=userid)

def set_password(user_id: str, password: str) -> UserRecord:
    return auth.update_user(user_id, password=password)

if __name__ == "__main__":
    initialize()
    arg = get_email_arg()
    check = create_user(arg.username, arg.email, arg.user-type)
    if (check):
        new_user: UserRecord = create_firebase_user(arg.email)
        set_password(userid, arg.password)
    #print(f"Firebase successfully created a new user with email - {new_user.email} and user id - {new_user.uid}")