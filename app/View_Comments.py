import argparse

from app import app, db
from app.models import Comments, User

import firebase_admin
from firebase_admin import credentials, firestore, storage, db

import os

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
    parser.add_argument("--sectionname", required=True, help="Name of the section")
    return parser.parse_args()

def pull_comments(auditid: int, section: str):
    # ok so i'll need to return like the child comments somehow tied to the parent comment right
    # so like each thread separately 

    comments = []
    for comment in Comments.query.filter(db.and_(Comments.audit_id == auditid, Comments.section == section)).order_by(Comments.path):
        print("{}{}: {}".format('    '*comment.level(), comment.sender_id, comment.body))
        senderName = User.query.get(comment.sender_id).username
        each = {"senderId":senderName, "comment":comment.body, "level":comment.level()}
        comments.append(each)
    return comments

def get_images(auditid: int, section:str):
    image_paths = []
    for comment in Comments.query.filter(db.and_(Comments.audit_id == auditid, Comments.section == section)).order_by(Comments.path):
        image_path = comment.image_path

        for path in image_path:
            #download_image(auditid, section, path)
            print(path)


def download_image(audit_id: int, section: str, image_path: str):
    list_of_paths = image_path.split(",")
    current_path = 0
    folder_name = "downloads/" + str(audit_id) + "/" + section
    if not os.path.exists(folder_name):
            os.makedirs(folder_name)
    for x in list_of_paths:
        storage_path = str(audit_id) + "/" + section + str(current_path) #should just be x but i'll double check once yansiew gets back to me
        image_name = folder_name + str(current_path) + ".jpg"
        bucket = storage.bucket()
        blob = bucket.blob(storage_path)
        blob.download_to_filename(image_name)
        current_path += 1
    return storage_path
