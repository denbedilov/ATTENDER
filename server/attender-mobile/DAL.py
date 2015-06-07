__author__ = 'olesya'
#This class is suppose to access to DB and transfer answers to other classes

from models.user import User
from models.event import Event
from models.attendings import Attendings
import json
from time import mktime
from facebook_logic import fb_logic
import logging

class DAL():
    @staticmethod
    def set_user_details(user_id,  name, last_name, email):
        user1 = User()
        if not user1.check_fb_logged_in(user_id):
            user1.fb_id = user_id
            user1.first_name = name
            user1.last_name = last_name
            user1.email = email
            user1.put()

    @staticmethod
    def get_user_details(user_id, fbf="false"):
        user_details = dict()
        user = User.get_by_id(user_id)
        if user is not None:
            user_details['name'] = user.first_name
            user_details['lastname'] = user.last_name
            user_details['fbf'] = fbf
            return user_details

    @staticmethod
    def user_login(email, password):
        #check all credentials are right
        qry = User.query(User.email == email, User.password == password).get()
        if qry:
            return qry.key.id()
        else:
            #check password wrong
            q = User.query(User.email == email).get()
            if q and q.password == "None":
                return 2
            elif q:
                return 1
            elif q is None:
                return False

    @staticmethod
    def register(email, hashed_password, first, last):
        user1 = User()
        qry = user1.check_user_exist_by_email(email)
        try:
            qry.password = hashed_password
            token = qry.put()
            return token.id()
        except:
            user1.email = email
            user1.password = hashed_password
            user1.first_name = first
            user1.last_name = last
            token = user1.put()
            return token.id()

    @staticmethod
    def set_event_details(e_id, name, date, city,  add, descr, host, url, attendees, price, category, source):
        event1 = Event()
        qry = event1.check_event_exist(e_id) or event1.check_event_exist_by_name(name)
        if qry is False:
            event1.id = e_id
            event1.name = name
            event1.date = date
            event1.city = city
            event1.address = add
            event1.description = descr
            event1.host = host
            event1.event_url = url
            event1.source = source
            if (attendees != "Unknown"):
                event1.attendees = attendees
            event1.price = price
            if category is not None:
                event1.category = category
            key = event1.put()
            return key
        else:
            results = Attendings.query(Attendings.event_id == qry.get_by_id(e_id))
            if results is not None:
                qry.attendees = attendees + results.count()
            else:
                qry.attendees = attendees

    @staticmethod
    def get_event_details(event_id):
        res = Event.get_by_id(event_id)
        if res is not None:
            event = dict()
            event['id'] = res.key.id()
            event['name'] = res.name
            date_time = int(mktime(res.date.utctimetuple()) * 1000)
            event['date'] = date_time
            event['city'] = res.city
            event['address'] = res.address
            event['description'] = res.description
            event['host'] = res.host
            event['event_url'] = res.event_url
            event['attendees'] = res.attendees
            event['price'] = res.price
            return event

    def get_attendings(self, ev_id, user_id):
        us = User.get_by_id(user_id)
        token = None
        if us is not None:
            token = us.fb_id
        if Event.get_by_id(ev_id) is None:
            return 1
        results = Attendings.query(Attendings.event_id == ev_id)
        if results is None:
            return 0
        return self.json_format_attendees(results, token, user_id)

    def json_format_attendees(self, query_res, token, my_id):
        users = list()
        fb_friends = fb_logic.get_fb_friends(token)
        logging.info(fb_friends)
        if fb_friends is None:
            fb_friends = []
        for res in query_res:
            fbf = "false"
            for f in fb_friends:
                if int(f) == res.user_id:
                    fbf = "true"
            if res.user_id != my_id: #do not return myself!
                users.append(self.get_user_details(res.user_id, fbf))
        return json.dumps(users)

    @staticmethod
    def attend(u_key, e_key):
        event1 = Event()
        attendings1 = Attendings()

        qry = User.get_by_id(u_key)
        if qry is None:
            return 1
        else:
            attendings1.user_id = u_key
        if Event.get_by_id(e_key) is None:
            return 2
        else:
            attendings1.event_id = e_key
        if attendings1.check_attend_exist(u_key, e_key) is False:
            attendings1.put()
            event1.update_attendees(e_key, action="add")
        return 0

    @staticmethod
    def unattend(u_key, e_key):
        event1 = Event()
        qry = User.get_by_id(u_key)
        if qry is None:
            return 1
        if Event.get_by_id(e_key) is None:
            return 2
        attendings1 = Attendings()
        q = attendings1.check_attend_exist(u_key, e_key)
        if q:
            q.key.delete()
            event1.update_attendees(e_key, action="sub")
        return 0

    def get_all_user_events(self, u_id):
        events_list = []
        results = Attendings.query(Attendings.user_id == u_id)
        for res in results:
            if self.get_event_details(res.event_id) is not None:
                events_list.append(self.get_event_details(res.event_id))
        return json.dumps(events_list)

    def check_token(self, token):
        if User.get_by_id(token) is None:
            return False
        else:
            return True

