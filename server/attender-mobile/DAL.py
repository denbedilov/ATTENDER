__author__ = 'olesya'

#This class is suppose to access to DB and transfer answers to other classe
#For the time the server is under development it will retrieve fake data

from google.appengine.ext import ndb
from models.User import User
from models.Event import Event
from models.Attendings import Attendings
import datetime


class DAL():
    us_list = []
    ev_list = []
    user1 = User()
    user1.user_name = "oles_ka"
    user1.email = "someemail@gmail.com"
    user1.user_password = "12345"
    user1.first_name = "Olesya"
    user1.last_name = "Shapira"

    us_list.append(user1)

    event1 = Event()
    event1.address = "somesdress"
    event1.date = datetime.date(15, 5, 1)
    event1.description = "some description"
    event1.name = "python meeting"
    event1.owner = "Olesya"
    event1.time = datetime.time(13, 0)

    ev_list.append(event1)

    attendings1 = Attendings()
    attendings1.event_id = attendings1.key
    attendings1.user_id = attendings1.key

    def get_user_details(self, data_type):
        if data_type == "user_name":
            return self.user1.user_name
        elif data_type == "first_name":
            return self.user1.first_name
        elif data_type == "last_name":
            return self.user1.last_name
        elif data_type == "email":
            return self.user1.email
        elif data_type == "user_password":
            return self.user1.user_password


    def get_event_details(self, data_type):
        if data_type == "address":
            return self.event1.address
        elif data_type == "date":
            return self.event1.date
        elif data_type == "description":
            return self.event1.description
        elif data_type == "name":
            return self.event1.name
        elif data_type == "owner":
            return self.event1.owner
        elif data_type == "time":
            return self.event1.time


    def get_attendings(self, data_type):
        if data_type == "event_id":
            return self.attendings1.event_id
        elif data_type == "user_id":
            return self.attendings1.user_id


    def set_user_details(self, un, em, psw, fn=None, ls=None):
        user1 = User()
        user1.user_name = un
        user1.email = em
        user1.user_password = psw
        user1.first_name = fn
        user1.last_name = ls
        self.us_list.append(user1)
        print self.us_list
        return self.us_list
        #user1.put()


    def set_event_details(self, name, date, time, add, descr, own):
        event1 = Event()
        event1.name = name
        event1.date = date
        event1.time = time
        event1.address = add
        event1.description = descr
        event1.owner = own
        self.ev_list.append(event1)
        print self.ev_list
        return self.ev_list
        #event1.put()


    def set_attendings(self, u_key, e_key):
        attendings1 = Attendings()
        attendings1.user_id = u_key
        attendings1.event_id = e_key

        #attendings1.put()


