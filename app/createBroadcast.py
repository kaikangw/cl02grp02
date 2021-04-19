import argparse

from app import app, db
from app.models import Broadcasts

def get_args():
    parser = argparse.ArgumentParser(description="Create broadcast")
    parser.add_argument("--senderid", required=True, help="id of the sender")
    parser.add_argument("--receivertype", required=True, help="receiver type (auditor, tenant, both)")
    parser.add_argument("--body", required=True, help="Contents of the broadcast")
    return parser.parse_args()

def create_broadcast(senderid: int, receivertype: str, body: str):
    broadcast = Broadcasts(sender_id = senderid, receivertype = receivertype, body = body)
    db.session.add(broadcast)
    db.session.commit()

if __name__ == "__main__":
    args = get_args()
    create_broadcast(args.senderid, args.receivertype, args.body)
