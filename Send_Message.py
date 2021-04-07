import argparse

from app import app, db
from app.models import Messages

def get_message_arg():
    parser = argparse.ArgumentParser(description="Upload a comment")
    parser.add_argument("--senderid", required=True, help="id of the sender")
    parser.add_argument("--receiverid", required=True, help="id of the receiver")
    parser.add_argument("--body", required=True, help="comment text")
    return parser.parse_args()


if __name__ == "__main__":
    arg = get_message_arg()
    msg = Messages(sender_id = arg.senderid, recipient_id = arg.receiverid, body = arg.body)
    db.session.add(msg)
    db.session.commit()