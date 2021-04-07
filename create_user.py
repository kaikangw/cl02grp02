import argparse
from typing import Optional

import firebase_admin
from firebase_admin import auth
from firebase_admin.auth import UserRecord

from app import app, db
from app.models import User

firebase_admin.initialize_app()

userid = 0

def get_email_arg():
    parser = argparse.ArgumentParser(description="Create a new user")
    parser.add_argument("--username", required=True, help="Username of the user to be created")
    parser.add_argument("--email", required=True, help="The email address of the user to be created")
    parser.add_argument("--user-type", required=True, help="Tenant/Auditor/Admin")
    return parser.parse_args()

def create_user(username: str, email: str, usertype: str):
    user1 = User(username = username, email = email, type = usertype)
    db.session.add(user1)
    db.session.commit()
    global userid
    userid = user1.id

def create_firebase_user(email: str) -> UserRecord:
    return auth.create_user(email=email, uid=userid)

def update_display_name(user_id: str, display_name: str) -> UserRecord:
    return auth.update_user(user_id, display_name=display_name)

if __name__ == "__main__":
    arg = get_email_arg()
    create_user(arg.username, arg.email, arg.user-type)
    new_user: UserRecord = create_firebase_user(arg.email)
    #print(f"Firebase successfully created a new user with email - {new_user.email} and user id - {new_user.uid}")