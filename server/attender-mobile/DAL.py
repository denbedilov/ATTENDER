__author__ = 'olesya'

#This class is suppose to access to DB and transfer answers to other classes
import logging
from models.User import User
from models.Event import Event
from models.Attendings import Attendings
import json
from time import mktime
from facebook_logic import fb_logic


class DAL():
    @staticmethod
    def set_user_details(user_id,  name, last_name, em=None):
        user1 = User()
        if not user1.check_user_exist(user_id):
            user1.user_id = user_id
            user1.first_name = name
            user1.last_name = last_name
            user1.email = em
            user1.put()

    @staticmethod
    def get_user_details(user_id, fbf="false"):
        user_details = dict()
        user = User.query(User.user_id == user_id).get()
        if user is not None:
            user_details['name'] = user.first_name
            user_details['lastname'] = user.last_name
            user_details['fbf'] = fbf
            return user_details

    @staticmethod
    def set_event_details(e_id, name, date, city,  add, descr, host, url, attendees, price, category):
        event1 = Event()
        qry = event1.check_event_exist(e_id)
        if qry is False:
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

    def get_attendings(self, ev_id, token):
        if Event.get_by_id(ev_id) is None:
            return 1
        results = Attendings.query(Attendings.event_id == ev_id)
        if results is None:
            return 0
        return self.json_format_attendees(results, token)

    def json_format_attendees(self, query_res, token):
        users = list()
        fb_friends = fb_logic.get_fb_friends(token)
        for res in query_res:
            fbf = "false"
            for f in fb_friends:
                if int(f) == res.user_id:
                    fbf = "true"

            users.append(self.get_user_details(res.user_id, fbf))
        return json.dumps(users)





    @staticmethod
    def attend(u_key, e_key):
        event1 = Event()
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
        if attendings1.check_attend_exist(u_key, e_key) is False:
            attendings1.put()
            event1.update_attendees(e_key, action="add")
        return 0

    @staticmethod
    def unattend(u_key, e_key):
        event1 = Event()
        qry = User.query(User.user_id == u_key).get()
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
        events_list = list()
        results = Attendings.query(Attendings.user_id == u_id)
        for res in results:
            events_list.append(self.get_event_details(res.event_id))
        return json.dumps(events_list)



