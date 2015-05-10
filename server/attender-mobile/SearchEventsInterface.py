__author__ = 'itamar and olesya'

import sys
import json
from DAL import DAL
from datetime import datetime, timedelta
from time import mktime
from models.Event import Event
import logging

sys.path.insert(0, 'lib')  #we need this line in order to make libraries imported from lib folder work properly
import requests  #Used for http requests

# Meetup.com documentation here: http://www.meetup.com/meetup_api/docs/2/groups/

URL_PATTERN = "https://api.meetup.com/find/open_events?"
URL_PATTERN_CITIES = "http://api.meetup.com/2/cities"
API_KEY = "185c2b3e44c4b4644365a3022d5a2f"


class SearchUsingAPI():
    topics = {"Career": 2,                           #Career & Business"
              "Community": 4,                        #Community & Environment
              "Games": 11,
              "Fitness": 9,
              "Health": 14,                          #Health & Wellbeing"
              "Language & Ethnic Identity": 16,      #Language & Ethnic Identity"
              "New Age": 22,                         #New Age & Spirituality
              "Socializing": 31,
              "Tech": 34,
              "Cars": 3}                             #Cars & Motorcycles

    def request_events(self, city=None, category=None, date_and_time=None, city_num=10):
        events_list = []
        per_page = 200
        offset = 0
        cities = []
        request = {}

        logging.info("Starting connection to meetup.api")
        if category is not None:
            category = category.strip()
            catg = self.topics.get(category)  #find in dictionary
            if catg is not None:
                t = {"category": catg}
                request.update(t)
            else:
                logging.info("There is no such category {}".format(category))
                return
        if date_and_time is not None:
            date_and_time = ',' + date_and_time
            ti = {"time": date_and_time}
            request.update(ti)
        if city is not None:
            cities.append(city)
        else:
            cities = self.request_city(city_num)

        for city in cities:  #for each city requst info from meetup
            request.update({"sign": "true", "country": "il", "key": API_KEY,
                                    "page": per_page, "offset": offset, "fields": "event_hosts", "city": city, "text_format": "plain"})

            response, status_code = get_results("http://api.meetup.com/2/open_events", request)
            offset += 1
            logging.info("Actual meetup respond {}".format(response))
            if status_code == 200:
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
        response, status_code = get_results(URL_PATTERN_CITIES, request)
        logging.info("In cities request, status code: {}".format(status_code))
        if status_code == 200:
            for res in response["results"]:
                cities.append(res["city"])
            return cities


def get_results(request_url, params):
    request = requests.get(request_url, params=params)
    data = request.json()
    return data, request.status_code


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


def save_in_db(event, category=None):
    mydb = DAL()
    sec = event['date'] / 1000
    e = Event()
    date = datetime.fromtimestamp(sec)
    if category is not None:
        e.update_category(event['id'],category)
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