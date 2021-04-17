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
    output = []
    checksender = Messages.query.filter(Messages.sender_id == userid)
    for message in checksender:
        my_name = User.query.get(message.recipient_id).username
        print(my_name)
        if (my_name not in output) and (message.recipient_id != message.sender_id):
            name = User.query.get(message.recipient_id).username
            output.append(name)
    checkreceiver = Messages.query.filter(Messages.recipient_id == userid)
    for message in checkreceiver:
        my_name = User.query.get(message.sender_id).username
        if (my_name not in output) and (message.sender_id != message.recipient_id):
            name = User.query.get(message.sender_id).username
            output.append(name)
    print(output)
    return output

if __name__ == "__main__":
    arg = get_user_arg()
    makeList(arg.userid)
    