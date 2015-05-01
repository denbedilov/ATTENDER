__author__ = 'olesya'

from google.appengine.ext import ndb
from Event import Event


class Chat(ndb.Model):
    chat_id = ndb.IntegerProperty()
    event_id = ndb.KeyProperty(kind=Event.name)
    name = ndb.StringProperty()
