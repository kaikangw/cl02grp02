import argparse

import firebase_admin
from firebase_admin import credentials, firestore, storage, db

from app import app, db
from app.models import Comments
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


def get_comment_arg():
    parser = argparse.ArgumentParser(description="Upload a comment")
    parser.add_argument("--auditid", required=True, help="audit id")
    parser.add_argument("--senderid", required=True, help="id of the sender")
    parser.add_argument("--receiverid", required=True, help="id of the receiver")
    parser.add_argument("--sectionname", required=True, help="Name of the section")
    parser.add_argument("--body", required=True, help="comment text")
    parser.add_argument("--imagepaths", required=True, help="path of images to be uploaded")
    return parser.parse_args()

def add_to_database(audit_id: int, body: str, image_path: str, section: str, sender_id: int, receiver_id: int):
    comment = Comments(audit_id = audit_id, body = body, image_path = image_path, section = section, sender_id = sender_id, receiver_id = receiver_id)
    comment.save()


 
def upload_image(audit_id: int, section: str, image_path: list):
    current_path = 0
    #image_path should be a list
    for x in image_path:
        storage_path = str(audit_id) + "/" + section + str(current_path)
        bucket = storage.bucket()
        file_name = x
        blob = bucket.blob(storage_path)
        blob.upload_from_filename(file_name)
        current_path += 1
    return str(audit_id) + "/" + section
    
if __name__ == "__main__":
    arg = get_comment_arg()
    initialize()
    image_path = upload_image(arg.auditid, arg.sectionname, arg.imagepaths)
    add_to_database(arg.auditid, arg.body, arg.imagepaths, arg.section, arg.senderid, arg.receiverid)

