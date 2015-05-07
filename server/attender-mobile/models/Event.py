__author__ = 'olesya'

from google.appengine.ext import ndb
from datetime import datetime

class Event(ndb.Model):
    id = ndb.StringProperty()
    name = ndb.StringProperty()
    date = ndb.DateTimeProperty()
    city = ndb.StringProperty()
    address = ndb.StringProperty()
    description = ndb.TextProperty()
    host = ndb.StringProperty()
    event_url = ndb.StringProperty()
    attendees = ndb.IntegerProperty()
    price = ndb.StringProperty()
    category = ndb.StringProperty(default="All")

    @staticmethod
    def check_event_exist(e_id):
        if Event.query(Event.id == e_id).get():
            return True
        else:
            return False

    def return_all_events(self):
        return Event.query()

    def return_by_values(self, city, category, date):
        q = res = self.return_all_events()

        if city is not None:
            res = q.filter(Event.city == city)
        if category is not None:
            res = res.filter(Event.category == category)
        if date is not None:
           res = res.filter(Event.date < date)
        res = res.filter(Event.date > datetime.now())
        return res



