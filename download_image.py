import argparse

import firebase_admin
from firebase_admin import credentials, firestore, storage, db

from app import app, db
from app.models import Comments
import os

cred=credentials.Certificate('C:/Users/Mathias Koh/Desktop/Account Auth/Firebase_Service_Account_Key.json')
firebase_admin.initialize_app(cred, {
    'storageBucket': 'ezcheck-aa2cc.appspot.com',
    'databaseURL': 'https://ezcheck-aa2cc-default-rtdb.firebaseio.com/'
})

def get_args():
    parser = argparse.ArgumentParser(description="Download an image")
    parser.add_argument("--commentid", required=True, help="id of the comment")
    return parser.parse_args()

def download(comment_id: int):
    c = Comments.query.get(comment_id)
    audit_id = c.audit_id
    section = c.section
    image_path = c.image_path

    ref = db.reference('/')
    bucket = storage.bucket()
    source_blob_name = image_path
    destination_folder_name = "images/" + str(audit_id) + "/" + section
    destination_file_name = "images/" + image_path + ".jpg"
    blob = bucket.blob(source_blob_name)
    if not os.path.exists(destination_folder_name):
        os.makedirs(destination_folder_name)
    blob.download_to_filename(destination_file_name)

if __name__ == "__main__":
    args = get_args()
    download(args.commentid)