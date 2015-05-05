__author__ = 'olesya'

from google.appengine.ext import ndb


class Event(ndb.Model):
    id = ndb.StringProperty()
    name = ndb.StringProperty()
    date = ndb.DateTimeProperty()
    address = ndb.StringProperty()
    description = ndb.TextProperty()
    owner = ndb.StringProperty()

