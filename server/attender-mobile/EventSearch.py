__author__ = 'itamar and olesya'

import requests
import codecs
import sys
import json
from DAL import DAL
import datetime

# Meetup.com documentation here: http://www.meetup.com/meetup_api/docs/2/groups/

sys.path.insert(0, 'lib')	#we need these two lines in order to make libraries imported from lib folder work properly

UTF8Writer = codecs.getwriter('utf8')
sys.stdout = UTF8Writer(sys.stdout)
URL_PATTERN =  "https://api.meetup.com/find/open_events?"
URL_PATTERN_CITIES = "http://api.meetup.com/2/cities"
API_KEY = "185c2b3e44c4b4644365a3022d5a2f"

#TODO: Scheduale for each day to pull events and save in local DB. Pull new events every day

class EventSearch():
    topics = {"Career & Business": 2,
             "Community & Environment": 4,
             "Games": 11,
             "Fitness": 9,
             "Health & Wellbeing": 14,
             "Language & Ethnic Identity": 16,
             "New Age & Spirituality": 22,
             "Socializing": 31,
             "Tech": 34}

    def get_events(self, city=None, category=None, datetime=None):
        events_list = []
        per_page = 200
        offset = 0
        cities = []
        request = {}

        if category is not None:
            category = self.topics.get(category)
            t = {"category": category}
            request.update(t)
        if datetime is not None:
            ti = {"time": datetime}
            request.update(ti)
        if city is not None:
            cities.append(city)
        else:
            cities = self.request_city()

        for city in cities:
            request.update({"sign": "true", "country": "il", "state": "IL", "key": API_KEY,
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
                    add_to_db(event)

        event_json = json.dumps(events_list)
        return event_json

    def request_city(self):
        cities = []
        city_num = 10
        request = {"sign": "true", "country": "il", "key": API_KEY,
                                   "page": city_num, "offset": 0}
        response = get_results(URL_PATTERN_CITIES, request)
        for res in response["results"]:
            cities.append(res["city"])
        return cities


def get_results(request_url,params):
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


def add_to_db(event):
    mydb = DAL()
    sec = event['date'] / 1000
    date = datetime.datetime.fromtimestamp(sec)
    mydb.set_event_details(event['id'], event['name'], date, event['address'], event['description'], event['host'])



