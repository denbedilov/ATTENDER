__author__ = 'olesya'

from google.appengine.ext import ndb


class User(ndb.Model):
    user_id = ndb.IntegerProperty()
    first_name = ndb.StringProperty()
    last_name = ndb.StringProperty()
    password = ndb.StringProperty()
    email = ndb.StringProperty(default="None")

    def check_user_exist(self, user_id):
        if User.query(User.user_id == user_id).get():
            return True
        else:
            return False

    def check_email_exist(self, email):
        if User.query(User.email == email).get():
            return True
        else:
            return False




