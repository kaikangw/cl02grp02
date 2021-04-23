import unittest
from app import app, db
from app.models import User, Audit, Comments, Broadcasts, Messages
from app.generalFunctions import create_account, accountType, getusername, getuserid, login, send_msg, pull_msg, makeList, get_user_list, new_broadcast, get_broadcast_list, getinstitution, gettenancy, add_to_database, upload_image, pull_comments,get_images, getaudits, getTenants, delete_user, get_user_details


class MyModuleTest(unittest.TestCase):

    def test_duplicate(self):
        print("testing duplicate user")
        for x in range(2):
            if create_account("Johnny", "johnny@gmail.com", "auditor", "password", "CGH", "auditor", "NIL", 100):
                if x == 1:
                    self.fail("Should not be able to create account twice")
                user = User.query.filter(User.username == "Johnny").first()
                print(user.email)
                
            else:
                print("did not make duplicate account")
        user = User.query.filter(User.username == "Johnny").first()
        delete_user(user.id)

    def test_get_user_details(self):
        print("testing get_user_details")
        user = User(username = "Johnny", email = "johnny@gmail.com", type = "auditor", institution = "CGH", description = "auditor", location = "NIL", tenancy =100)
        db.session.add(user)
        db.session.commit()
        details = {
            "User ID" : user.id,
            "Username" : "Johnny",
            "Email" : "johnny@gmail.com",
            "Type" : "auditor",
            "Institution" : "CGH",
            "Tenancy" : 100,
            "Description" : "auditor",
            "Location" : "NIL"
        }
        self.assertEqual(get_user_details("Johnny"), details)
        db.session.delete(user)
        db.session.commit()

    def test_getters(self):
        print("testing getters")
        user = User(username = "Johnny", email = "johnny@gmail.com", type = "auditor", institution = "CGH", description = "auditor", location = "NIL", tenancy =100)
        db.session.add(user)
        db.session.commit()
        #self.assertEqual(accountType(user.id), "auditor")
        #self.assertEqual(getusername(user.id, "Johnny"))
        #self.assertEqual(getuserid("Johnny"), user.id)
        #self.assertEqual(getinstitution("Johnny"), "CGH")
        self.assertEqual(gettenancy("Johnny"), 100)
        db.session.delete(user)
        db.session.commit()


if __name__ == '__main__':
    unittest.main()