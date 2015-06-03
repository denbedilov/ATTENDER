# coding=utf-8
__authors__ = 'itamar and olesya'

import sys
import json
from datetime import datetime, timedelta
from time import mktime
from models.event import Event
from sources_wrapper import SearchEventsUsingAPI
import logging

sys.path.insert(0, 'lib')  # we need this line in order to make libraries imported from lib folder work properly


class EventSearch():
    def get_events(self, city=None, category=None, date_and_time=None):
        se = SearchEventsUsingAPI()
        events_list = []
        results = self.pull_from_db(city, category, date_and_time)
        if results.count() < 5:  # add more cities so will be more results for topics
            logging.info("Not enough results found")
            se.request_events(city, category, date_and_time, city_num=50)
            results = self.pull_from_db(city, category, date_and_time)

        for res in results:
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
            events_list.append(event)

        event_json = json.dumps(events_list)
        return event_json

    def pull_from_db(self, city=None, category=None, date_and_time=None):
        e = Event()
        n = 0
        if date_and_time is not None:
            if date_and_time == "1d":
                n = 1
            elif date_and_time == "1w":
                n = 7
            elif date_and_time == "1m":
                n = 30
            future_day = datetime.now() + timedelta(days=n)
            date_and_time = future_day
        result = e.return_by_values(city, category, date_and_time)
        return result


