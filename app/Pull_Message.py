import argparse

from app import app, db
from app.models import Messages, User
from sqlalchemy import or_, and_


def pull_messages(my_id: int, their_id: int):
    query = Messages.query.filter(db.or_(db.and_(Messages.sender_id == my_id, Messages.recipient_id == their_id), db.and_(Messages.sender_id == their_id, Messages.recipient_id == my_id))).order_by(Messages.timestamp)
    convo = []
    for i in query:
        date_time = i.timestamp.strftime("%m/%d/%Y, %H:%M:%S")
        senderName = User.query.get(i.sender_id).username
        print("{} \n{}: {}".format(date_time, senderName, i.body))
        msg = {"timestamp":date_time, "senderId": senderName, "content":i.body }
        convo.append(msg)
    
    return convo
    