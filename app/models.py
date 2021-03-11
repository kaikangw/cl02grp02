from datetime import datetime
from app import db

#db of the audit
class Audit(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    timestamp = db.Column(db.DateTime, index=True)
    auditor = db.Column(db.String(64), nullable=False)
    tenant = db.Column(db.String(64), nullable=False)
    part1_score = db.Column(db.Integer)
    part2_score = db.Column(db.Integer)
    part3_score = db.Column(db.Integer)
    part4_score = db.Column(db.Integer)
    part5_score = db.Column(db.Integer)
    total_score = db.Column(db.Integer)
    remarks = db.Column(db.String(64), nullable=False)
    rectification = db.Column(db.Integer)

    def __repr__(self):
        return '<Time {time}, Score {score}, part 1 {part1}, part 2 {part2}, part 3 {part3}, part 4 {part4}, part 5 {part5}>'.format(score = self.total_score, part2= self.part2_score, part1 = self.part1_score, part3 = self.part3_score, part4 = self.part4_score, part5 = self.part5_score, time = self.timestamp)