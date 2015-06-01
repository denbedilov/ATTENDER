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
    source = ndb.StringProperty()

    @staticmethod
    def check_event_exist(e_id):
        q = Event.query(Event.id == e_id).get()
        if q:
            return q
        else:
            return False

    def check_event_exist_by_name(self, name):
        q = Event.query(Event.name == name).get()
        if q:
            return q
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

    def update_category(self, e_id,  category):
        res = Event.query(Event.id == e_id).get()
        try:
            res.category = category
            res.put()
        except: #if such event not exist, add it later
            pass

    def update_attendees(self, ev_id, action):
        q = Event.get_by_id(ev_id)
        if q is not False:
            if action == "add":
                q.attendees += 1
            elif action == "sub":
                q.attendees -= 1
            q.put()








