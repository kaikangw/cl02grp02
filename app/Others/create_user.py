import argparse
from typing import Optional

import firebase_admin
from firebase_admin import auth, credentials
from firebase_admin.auth import UserRecord

from app import app, db
from app.models import User
from sqlalchemy import exc

userid = "0"

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

def create_account(username: str, email: str, usertype: str, password:str):
    
    initialize()
    #Create User
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
   
    
