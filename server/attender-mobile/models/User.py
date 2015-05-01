__author__ = 'olesya'

from google.appengine.ext import ndb

class User(ndb.Model):
    user_name = ndb.StringProperty()
    first_name = ndb.StringProperty()
    last_name = ndb.StringProperty()
    email = ndb.StringProperty()
    user_password = ndb.StringProperty()

