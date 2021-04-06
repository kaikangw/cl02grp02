import argparse
import json
import os
import requests
import pprint
from app.models import User

FIREBASE_WEB_API_KEY = "AIzaSyBXCtNbzv8EOVmvl4TVnsWmKLU5RYNF__8"
#os.environ.get("FIREBASE_WEB_API_KEY")
rest_api_url = f"https://identitytoolkit.googleapis.com/v1/accounts:signInWithPassword"


def get_args():
    parser = argparse.ArgumentParser(description="Sign in a Firebase user with email and password")

    parser.add_argument("--email", required=True, help="The email address which the user wants to sign in with.")
    parser.add_argument("--password", required=True, help="The password of the user.")

    return parser.parse_args()


def sign_in_with_email_and_password(email: str, password: str, return_secure_token: bool = True):
    payload = json.dumps({
        "email": email,
        "password": password,
        "returnSecureToken": return_secure_token
    })

    r = requests.post(rest_api_url,
                      params={"key": FIREBASE_WEB_API_KEY},
                      data=payload)

    return r.json()

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

if __name__ == "__main__":
    args = get_args()
    token = sign_in_with_email_and_password(args.email, args.password)
    pprint.pprint(token.get("localId")) #local id to be returned and used throughout the login session
