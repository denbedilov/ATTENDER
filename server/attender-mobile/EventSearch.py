__author__ = 'itamar and olesya'

import webapp2
import requests
import time
import codecs
import sys
import json

# Meetup.com documentation here: http://www.meetup.com/meetup_api/docs/2/groups/

UTF8Writer = codecs.getwriter('utf8')
sys.stdout = UTF8Writer(sys.stdout)
URL_PATTERN =  "https://api.meetup.com/find/open_events?"
URL_PATTERN_CITIES = "http://api.meetup.com/2/cities"
API_KEY = "185c2b3e44c4b4644365a3022d5a2f"

#TODO: Scheduale for each day to pull events and save in local DB. Pull new events every day


class SearchHandler(webapp2.RequestHandler):
    def get_events(self, city=None, category=None, datetime=None):
        events_list = []
        per_page = 10
        offset = 0
        cities = []
        request = {}

        if category is not None:
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

                    try:
                        event['id'] = res['id']
                    except:
                        event['id'] = 'Unknown'
                    try:
                        event['name'] = res['name']
                    except:
                        event['name'] = 'Unknown'
                    try:
                        event['date'] = res['time']
                    except:
                        event['date'] = 'Unknown'
                    try:
                        event['city'] = res['venue']['city']
                    except:
                        event['city'] = 'Unknown'
                    try:
                        event['address'] = res['venue']['address_1']
                    except:
                        event['address'] = 'Unknown'
                    try:
                        event['description'] = res['description'] #description
                    except:
                        event['description'] = 'Unknown'
                    try:
                        event['event_url'] = res['event_url']
                    except:
                        event['event_url'] = 'Unknown'
                    try:
                        for host in res['event_hosts']: #Owner
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
        for ev in events_list:
            print ev
            print '\n'

        event_json = json.dumps(events_list)
        print event_json
        return event_json

    def request_city(self):
        cities = []
        city_num = 50
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


if __name__=="__main__":
    temp = SearchHandler()
    temp.get_events(category=28)


search = webapp2.WSGIApplication([
    ('/search', SearchHandler)
], debug=True)


'''

topics = [  {"Career & Business": 2},
            {"Community & Environment": 4},
            {"Games": 11},
            {"Fitness": 9},
            {"Health & Wellbeing": 14},
            {"Language & Ethnic Identity": 16},
            {"New Age & Spirituality": 22},
            {"Socializing" : 31}
            {"Tech" : 34}]


'''
