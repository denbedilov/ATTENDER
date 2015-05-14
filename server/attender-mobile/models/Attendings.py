__author__ = 'olesya'

from google.appengine.ext import ndb
from User import User
from Event import Event


class Attendings(ndb.Model):
    user_id = ndb.IntegerProperty()
    event_id = ndb.IntegerProperty()

