  
from datetime import datetime
from app import db

#db of the audit
class Audit(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    timestamp = db.Column(db.DateTime, index=True)
    #added foreign keys to auditor and tenant
    auditor = db.Column(db.String(64), db.ForeignKey('user.username'), nullable=False)
    tenant = db.Column(db.String(64), db.ForeignKey('user.username'), nullable=False)
    audit_ref = db.relationship("User", foreign_keys = [auditor])
    tenant_ref = db.relationship("User", foreign_keys = [tenant])
    
    part1_score = db.Column(db.Integer)
    part2_score = db.Column(db.Integer)
    part3_score = db.Column(db.Integer)
    part4_score = db.Column(db.Integer)
    part5_score = db.Column(db.Integer)
    total_score = db.Column(db.Integer)
    remarks = db.Column(db.String(64), nullable=False)
    rectification = db.Column(db.Integer)
    #added relationship to comments
    comments = db.relationship("Comments", backref = 'audit', lazy = 'dynamic')

    def __repr__(self):
        return '<Time {time}, Score {score}, part 1 {part1}, part 2 {part2}, part 3 {part3}, part 4 {part4}, part 5 {part5}>'.format(score = self.total_score, part2= self.part2_score, part1 = self.part1_score, part3 = self.part3_score, part4 = self.part4_score, part5 = self.part5_score, time = self.timestamp)

#all stuff i'm adding

class User(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String(64), index = True, unique = True)
    email = db.Column(db.String(120), index = True, unique = True)
    type = db.Column(db.String(20)) #tenant/auditor/admin

    messages_sent = db.relationship('Messages', foreign_keys='Messages.sender_id', backref='author', lazy='dynamic')
    messages_received = db.relationship('Messages', foreign_keys='Messages.recipient_id', backref='recipient', lazy='dynamic')
    
    def __repr__(self):
        return '<User {username}, email {email}, id {id}>'.format(username = self.username, email = self.email, id = self.id)

class Comments(db.Model):
    _N = 6
    #default info
    id = db.Column(db.Integer, primary_key = True)
    audit_id = db.Column(db.Integer, db.ForeignKey('audit.id'), nullable = False)
    body = db.Column(db.String(280), nullable = True)
    image_path = db.Column(db.String(100), nullable = True)
    timestamp = db.Column(db.DateTime, index = True, default = datetime.utcnow)
    section = db.Column(db.String(20), nullable = False)
    #sender/receiver
    sender_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable = False)
    receiver_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable = False)
    sender_ref = db.relationship("User", foreign_keys = [sender_id])
    receiver_ref = db.relationship("User", foreign_keys = [receiver_id])
    #reply path
    path = db.Column(db.Text, index = True)
    parent_id = db.Column(db.Integer, db.ForeignKey('comments.id'))
    replies = db.relationship('Comments', backref = db.backref('parent', remote_side = [id]), lazy = 'dynamic')

    def save(self):
        db.session.add(self)
        db.session.commit()
        prefix = self.parent.path + '.' if self.parent else ''
        self.path = prefix + '{:0{}d}'.format(self.id, self._N)
        db.session.commit()
    
    #use level to determine indentation if necessary 
    def level(self):
        return len(self.path) // self._N - 1 

    def __repr__(self):
        return "<Post by {sender_id} to {receiver_id}: {body}>".format(sender_id = self.sender_id, receiver_id = self.receiver_id, body = self.body)

class Messages(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    sender_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    recipient_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    sender_ref = db.relationship("User", foreign_keys = [sender_id])
    recipient_ref = db.relationship("User", foreign_keys = [recipient_id])
    body = db.Column(db.String(140))
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)

    def __repr__(self):
        return "<Message sent by {sender} to {recipient} at {timestamp}: {body}".format(sender = self.sender_id, recipient = self.recipient_id, timestamp = self.timestamp, body = self.body)

class Broadcasts(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    sender_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    receiver_type = db.Column(db.String(20))
    body = db.Column(db.String(140))
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)