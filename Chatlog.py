import argparse

from app import app, db
from app.models import Messages, User
from sqlalchemy import or_, and_

# in: user id
# out: list of other users this user is in a convo with
output = []

def get_user_arg():
    parser = argparse.ArgumentParser(description="Get chat logs")
    parser.add_argument("--userid", required=True, help="current user id")
    return parser.parse_args()

def makeList(userid: int):
    checksender = Messages.query.filter(Messages.sender_id == userid)
    for message in checksender:
        if message.recipient_id not in output:
            output.append(message.recipient_id)
    checkreceiver = Messages.query.filter(Messages.recipient_id == userid)
    for message in checkreceiver:
        if message.sender_id not in output:
            output.append(message.sender_id)
    return output

if __name__ == "__main__":
    arg = get_user_arg()
    makeList(arg.userid)
    