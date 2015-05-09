__author__ = 'itamar and olesya'

import codecs
import sys
import json
from DAL import DAL
from datetime import datetime, timedelta
from time import mktime
from models.Event import Event
import logging

sys.path.insert(0, 'lib')	#we need these two lines in order to make libraries imported from lib folder work properly
import requests

# Meetup.com documentation here: http://www.meetup.com/meetup_api/docs/2/groups/

UTF8Writer = codecs.getwriter('utf8')
sys.stdout = UTF8Writer(sys.stdout)
URL_PATTERN =  "https://api.meetup.com/find/open_events?"
URL_PATTERN_CITIES = "http://api.meetup.com/2/cities"
API_KEY = "185c2b3e44c4b4644365a3022d5a2f"

#TODO: Scheduale for each day to pull events and save in local DB. Pull new events every day

class SearchUsingAPI():
    topics = {"Career & Business": 2,
             "Community & Environment": 4,
             "Games": 11,
             "Fitness": 9,
             "Health & Wellbeing": 14,
             "Language & Ethnic Identity": 16,
             "New Age & Spirituality": 22,
             "Socializing": 31,
             "Tech": 34,
             "Cars & Motorcycles": 3}

    def request_events(self, city=None, category=None, date_and_time=None, city_num=10):
        events_list = []
        per_page = 200
        offset = 0
        cities = []
        request = {}

        logging.info("Starting connection to meetup.api")
        if category is not None:
            topic = self.topics.get(category)
            t = {"category": topic}
            request.update(t)
        if date_and_time is not None:
            date_and_time = ',' + date_and_time
            ti = {"time": date_and_time}
            request.update(ti)
        if city is not None:
            cities.append(city)
        else:
            cities = self.request_city(city_num)

        for city in cities:
            request.update({"sign": "true", "country": "il", "key": API_KEY,
                                    "page": per_page, "offset": offset, "fields": "event_hosts", "city": city})

            response = get_results("http://api.meetup.com/2/open_events", request)
            offset += 1

            if response is not None:
                for res in response['results']:
                    event = {}

                    check_valid(event, res, 'id', 'id')
                    check_valid(event, res, 'name', 'name')
                    check_valid(event, res, 'date', 'time')
                    check_valid(event, res, 'city', 'venue', 'city')
                    check_valid(event, res, 'address', 'venue', 'address_1')
                    check_valid(event, res, 'description', 'description')
                    check_valid(event, res, 'event_url', 'event_url')

                    try:
                        for host in res['event_hosts']:  #Owner
                            event['host'] = host['member_name']
                    except:
                        event['host'] = 'Unknown'
                    try:
                        event['attendees'] = res['yes_rsvp_count'] #Attendees
                    except:
                        event['attendees'] = 'Unknown'
                    try:
                        event['price'] = res['fee']['amount'] + res['fee']['currency']
                    except:
                        event['price'] = "free"

                    events_list.append(event)
                    save_in_db(event, category)

        event_json = json.dumps(events_list)
        return event_json

    def request_city(self, city_num):
        cities = []
        request = {"sign": "true", "country": "il", "key": API_KEY,
                                   "page": city_num, "offset": 0}
        response = get_results(URL_PATTERN_CITIES, request)
        for res in response["results"]:
            cities.append(res["city"])
        return cities




def get_results(request_url, params):
    request = requests.get(request_url, params=params)
    data = request.json()
    return data


# Surround with try and catch for each requested field in case the information is not available
def check_valid(event, res, key, params, params2=None):
    try:
        if params2 is None:
            event[key] = res[params]
        else:
            event[key] = res[params][params2]
        return event
    except:
        event[key] = "Unknown"


def save_in_db(event, category):
    mydb = DAL()
    sec = event['date'] / 1000
    e = Event()
    date = datetime.fromtimestamp(sec)
    if not e.check_event_exist(event['id']):
        mydb.set_event_details(event['id'], event['name'], date, event['city'], event['address'],
                               event['description'], event['host'], event['event_url'], event['attendees'], event['price'], category)




class EventSearch():
    def get_events(self, city=None, category=None, date_and_time=None):
        se = SearchUsingAPI()
        events_list = []

        results = self.pull_from_db(city, category, date_and_time)
        if city is None and results.count() < 5: # add more cities so will be more results for topics
            logging.info("Not enough results found")
            event_json = se.request_events(city, category, date_and_time, city_num=100)
            return event_json

        for res in results:
            event = dict()
            event['id'] = res.id
            event['name'] = res.name
            date_time = mktime(res.date.utctimetuple()) * 1000
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