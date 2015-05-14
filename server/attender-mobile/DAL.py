__author__ = 'olesya'

#This class is suppose to access to DB and transfer answers to other classe
#For the time the server is under development it will retrieve fake data

from google.appengine.ext import ndb
from models.User import User
from models.Event import Event
from models.Attendings import Attendings
import logging


class DAL():
    def get_user_details(self, user_id):
        user = User.query(User.user_id == user_id).get()
        user_details = dict()
        user_details['name'] = user.first_name
        user_details['lastname'] = user.last_name
        return user_details

    def get_event_details(self, event_id):
       pass

    def get_attendings(self, ev_id):
        if Event.get_by_id(ev_id) is None:
            return 1
        results = Attendings.query(Attendings.event_id == ev_id).get()
        if results is None:
            return 0
        return results

    def set_user_details(self, user_id,  name, last_name, em=None):
        user1 = User()
        if not user1.check_user_exist(user_id):
            user1.user_id = user_id
            user1.first_name = name
            user1.last_name = last_name
            user1.email = em
            user1.put()

    def set_event_details(self, e_id, name, date, city,  add, descr, host, url, attendees, price, category):
        event1 = Event()
        if not event1.check_event_exist(e_id):
            event1.id = e_id
            event1.name = name
            event1.date = date
            event1.city = city
            event1.address = add
            event1.description = descr
            event1.host = host
            event1.event_url = url
            if (attendees != "Unknown"):
                event1.attendees = attendees
            event1.price = price
            if category is not None:
                event1.category = category
            event1.put()

    def set_attendings(self, u_key, e_key):
        attendings1 = Attendings()

        qry = User.query(User.user_id == u_key).get()
        if qry is None:
            return 1
        else:
            attendings1.user_id = u_key
        if Event.get_by_id(e_key) is None:
            return 2
        else:
            attendings1.event_id = e_key

        attendings1.put()
        return 0


