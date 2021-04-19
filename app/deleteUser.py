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

def get_user_id_arg():
    parser = argparse.ArgumentParser(description="Delete user in Firebase")
    parser.add_argument("--user-id", required=True, help="The user id of the user to be deleted.")
    return parser.parse_args()

def delete_user(user_id: str):
    user = User.query.get(user_id)
    db.session.delete(user)
    db.session.commit()
    return auth.delete_user(user_id)

if __name__ == "__main__":
    initialize()
    args = get_user_id_arg()
    delete_user(args.user-id)