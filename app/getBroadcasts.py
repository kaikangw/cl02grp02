import argparse

from app import app, db
from app.models import Broadcasts, User
from sqlalchemy import exc, or_, and_

def get_args():
    parser = argparse.ArgumentParser(description="Get all broadcasts for that user")
    parser.add_argument("--receivertype", required=True, help="receiver type (auditor, tenant, both)")
    return parser.parse_args()

# input: current user type ("tenant" or "auditor")
# output: list of all the broadcasts for either specified user type or "both"
#         in the form of a dictionary {timestamp, name, contents of broadcast}

def get_broadcast_list(receivertype: str):
    broadcast_list = []
    query = Broadcasts.query.filter(db.or_(Broadcasts.receiver_type == receivertype, Broadcasts.receiver_type == "both"))
    for broadcast in query:
        date_time = broadcast.timestamp.strftime("%m/%d/%Y, %H:%M:%S")
        senderName = User.query.get(broadcast.sender_id).username
        details = {"timestamp" : date_time,
                    "senderName" : senderName,
                    "content" : broadcast.body}
        list.append(details)
    
    return broadcast_list

if __name__ == "__main__":
    args = get_args()
    list_of_broadcasts = get_broadcast_list(args.receivertype)

