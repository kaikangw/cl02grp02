import argparse

from app import app, db
from app.models import Comments

def get_comment_arg():
    parser = argparse.ArgumentParser(description="Upload a comment")
    parser.add_argument("--auditid", required=True, help="audit id")
    parser.add_argument("--sectionname", required=True, help="Name of the section")
    return parser.parse_args()

def pull_comments(userid: int, auditid: int, section: String):
    for comment in Comments.query.filter(db.and_(Comments.audit_id == auditid, Comments.section == section)).order_by(Comments.path):
        print("{}{}: {}".format('    '*comment.level(), comment.sender_id, comment.body))
