import argparse
from firebase_admin import auth
import firebase_admin
from firebase_admin import credentials, firestore, storage
from app import app, db
from app.models import User

FIREBASE_WEB_API_KEY = "AIzaSyBXCtNbzv8EOVmvl4TVnsWmKLU5RYNF__8"
rest_api_url = f"https://identitytoolkit.googleapis.com/v1/accounts:signInWithPassword"

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

## Since we have a function for listing all the names of users (get_user_list)
## as well as a function to get id from username (getuserid)
## I'm assuming we can input the user id for all the functions cos the admin will have access to these anyway

def change_email(userid: int, email: str):
    initialize()
    return auth.update_user(userid, email = email)

def change_password(userid: int, password: str):
    initialize()
    return auth.update_user(userid, password = password)

def change_type(userid: int, type: str):
    user = User.query.get(userid)
    user.type = type
    db.session.commit()

def change_institution(userid: int, institution: str):
    user = User.query.get(userid)
    user.institution = institution
    db.session.commit()

def change_tenancy(userid: int, tenancy: int):
    user = User.query.get(userid)
    user.tenancy = tenancy
    db.session.commit()

def change_location(userid: int, location: str):
    user = User.query.get(userid)
    user.location = location
    db.session.commit()