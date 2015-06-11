__author__ = 'olesya'

from google.appengine.ext import ndb


class User(ndb.Model):
    fb_id = ndb.IntegerProperty()
    first_name = ndb.StringProperty()
    last_name = ndb.StringProperty()
    password = ndb.StringProperty(default="None")
    email = ndb.StringProperty()

    def check_fb_logged_in(self, fb_id):
        qry = User.query(User.fb_id == fb_id).get()
        if qry:
            return qry
        else:
            return False

    def check_user_exist_by_email(self, email):
        qry = User.query(User.email == email).get()
        if qry:
            return qry
        else:
            return False








