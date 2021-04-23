from operator import pos
import os
import unittest

from config import basedir
from app import app, db
from app.models import Audit
from datetime import date, datetime
import random
from random import randint
import sys

class TestCase(unittest.TestCase):
    def setUp(self):
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'test.db')
        self.app = app.test_client()
        db.create_all()
    inp = open("/Users/kaikang/Downloads/flask/fuzzer.txt")
    line_array = inp.read().splitlines()
    def swap(line):
        if (len(line) < 2):
            #print("can't swap if only 1 char")
            return
        # implementation from ex.3 (mutation.py)
        position = randint(0,len(line)-2)
        left = line[:position] + line[position+1]
        right = line[position] + line[position+2:]
        #print("swapped: "+line+ " -> "+left+right)
        return left+right

    def trim(line):
        if (len(line) < 2):
            #print("can't trim if only 1 char")
            return
        position = randint(0,len(line)-2)
        trimmed = "trimmed: " + line + " -> " + line[:position]
        #print(trimmed)
        return line[:position]

    def flip(line):
        flipped = ""
        for char in line:
            # choose random index to flip
            index = randint(0,6)
            binary = bin(ord(char))[2:]
            # ascii space is 32=2^5, so need to add a 0 in front
            if (len(binary) == 6):
                binary = "0" + binary
            if (binary[index] == '0'):
                binary = binary[:index] + '1' + binary[index+1:]
            elif (binary[index] == '1'):
                binary = binary[:index] + '0' + binary[index+1:]
            flipped += chr(int(binary,2))
        return flipped
        #print("flipped: " + line + " -> "+ flipped)

    mutations = {
        0: swap,
        1: trim,
        2: flip
    }
    global my_lit
    my_lit = []

    for line in line_array:
        mut = randint(0,len(mutations)-1)
        one = mutations[mut](line)
        my_lit.append(one)


    
    def test_make_unique_nickname(self):
        u = Audit(tenant=random.choice(my_lit),timestamp= datetime.now(),auditor =random.choice(my_lit),part1_score=randint(0,sys.maxsize),part2_score=randint(0,sys.maxsize),part3_score=randint(0,sys.maxsize),part4_score=randint(0,sys.maxsize),part5_score=randint(0,sys.maxsize),total_score=randint(0,sys.maxsize),remarks=random.choice(my_lit),rectification=randint(0,sys.maxsize))
        db.session.add(u)
        db.session.commit()
    def test_make_unique_nickname2(self):
        u = Audit(tenant=random.choice(my_lit),timestamp= datetime.now(),auditor =random.choice(my_lit),part1_score=randint(0,sys.maxsize),part2_score=randint(0,sys.maxsize),part3_score=randint(0,sys.maxsize),part4_score=randint(0,sys.maxsize),part5_score=randint(0,sys.maxsize),total_score=randint(0,sys.maxsize),remarks=random.choice(my_lit),rectification=randint(0,sys.maxsize))
        db.session.add(u)
        db.session.commit()
    def test_make_unique_nickname3(self):
        u = Audit(tenant=random.choice(my_lit),timestamp= datetime.now(),auditor =random.choice(my_lit),part1_score=randint(0,sys.maxsize),part2_score=randint(0,sys.maxsize),part3_score=randint(0,sys.maxsize),part4_score=randint(0,sys.maxsize),part5_score=randint(0,sys.maxsize),total_score=randint(0,sys.maxsize),remarks=random.choice(my_lit),rectification=randint(0,sys.maxsize))
        db.session.add(u)
        db.session.commit()
    def test_make_unique_nickname4(self):
        u = Audit(tenant=random.choice(my_lit),timestamp= datetime.now(),auditor =random.choice(my_lit),part1_score=randint(0,sys.maxsize),part2_score=randint(0,sys.maxsize),part3_score=randint(0,sys.maxsize),part4_score=randint(0,sys.maxsize),part5_score=randint(0,sys.maxsize),total_score=randint(0,sys.maxsize),remarks=random.choice(my_lit),rectification=randint(0,sys.maxsize))
        db.session.add(u)
        db.session.commit()
    def test_make_unique_nickname5(self):
        u = Audit(tenant=random.choice(my_lit),timestamp= datetime.now(),auditor =random.choice(my_lit),part1_score=randint(0,sys.maxsize),part2_score=randint(0,sys.maxsize),part3_score=randint(0,sys.maxsize),part4_score=randint(0,sys.maxsize),part5_score=randint(0,sys.maxsize),total_score=randint(0,sys.maxsize),remarks=random.choice(my_lit),rectification=randint(0,sys.maxsize))
        db.session.add(u)
        db.session.commit()
    def test_make_unique_nickname6(self):
        u = Audit(tenant=random.choice(my_lit),timestamp= datetime.now(),auditor =random.choice(my_lit),part1_score=randint(0,sys.maxsize),part2_score=randint(0,sys.maxsize),part3_score=randint(0,sys.maxsize),part4_score=randint(0,sys.maxsize),part5_score=randint(0,sys.maxsize),total_score=randint(0,sys.maxsize),remarks=random.choice(my_lit),rectification=randint(0,sys.maxsize))
        db.session.add(u)
        db.session.commit()
    def test_make_unique_nickname7(self):
        u = Audit(tenant=random.choice(my_lit),timestamp= datetime.now(),auditor =random.choice(my_lit),part1_score=randint(0,sys.maxsize),part2_score=randint(0,sys.maxsize),part3_score=randint(0,sys.maxsize),part4_score=randint(0,sys.maxsize),part5_score=randint(0,sys.maxsize),total_score=randint(0,sys.maxsize),remarks=random.choice(my_lit),rectification=randint(0,sys.maxsize))
        db.session.add(u)
        db.session.commit()
    def test_make_unique_nickname8(self):
        u = Audit(tenant=random.choice(my_lit),timestamp= datetime.now(),auditor =random.choice(my_lit),part1_score=randint(0,sys.maxsize),part2_score=randint(0,sys.maxsize),part3_score=randint(0,sys.maxsize),part4_score=randint(0,sys.maxsize),part5_score=randint(0,sys.maxsize),total_score=randint(0,sys.maxsize),remarks=random.choice(my_lit),rectification=randint(0,sys.maxsize))
        db.session.add(u)
        db.session.commit()
    def test_make_unique_nickname9(self):
        u = Audit(tenant=random.choice(my_lit),timestamp= datetime.now(),auditor =random.choice(my_lit),part1_score=randint(0,sys.maxsize),part2_score=randint(0,sys.maxsize),part3_score=randint(0,sys.maxsize),part4_score=randint(0,sys.maxsize),part5_score=randint(0,sys.maxsize),total_score=randint(0,sys.maxsize),remarks=random.choice(my_lit),rectification=randint(0,sys.maxsize))
        db.session.add(u)
        db.session.commit()
    def test_make_unique_nickname10(self):
        u = Audit(tenant=random.choice(my_lit),timestamp= datetime.now(),auditor =random.choice(my_lit),part1_score=randint(0,sys.maxsize),part2_score=randint(0,sys.maxsize),part3_score=randint(0,sys.maxsize),part4_score=randint(0,sys.maxsize),part5_score=randint(0,sys.maxsize),total_score=randint(0,sys.maxsize),remarks=random.choice(my_lit),rectification=randint(0,sys.maxsize))
        db.session.add(u)
        db.session.commit()


if __name__ == '__main__':
    unittest.main()