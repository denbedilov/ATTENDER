# __author__ = 'itamar'
from __future__ import unicode_literals
import webapp2
import requests
from bs4 import BeautifulSoup
import time
import codecs
import sys
# https://docs.python.org/2/howto/urllib2.html
import urllib2
from urllib import urlopen
# http://www.w3.org/TR/css3-selectors/#selectors
from models.Attendings import Attendings
import json




# Meetup.com documentation here: http://www.meetup.com/meetup_api/docs/2/groups/

UTF8Writer = codecs.getwriter('utf8')
#parse_json = lambda s: simplejson.loads(s.decode('utf8'))


sys.stdout = UTF8Writer(sys.stdout)

URL_PATTERN =  "https://api.meetup.com/find/open_events?"

#TODO: Scheduale for each day to pull events and save in local DB. Pull new events every day
API_KEY = "185c2b3e44c4b4644365a3022d5a2f"
#TODO: close connection

class SearchHandler(webapp2.RequestHandler):
    def query(self, city=None, topic=None, datetime=None):
        if city is not None:
            cities = [(str(city),"IL")] #case choise was given
        else: #'default cities'
            cities =[("Jerusalem", "IL"),("Tel Aviv", "IL"),("Haifa", "IL")]

        for (city, state) in cities:
            per_page = 200
            results_we_got = per_page
            offset = 0

            request = {"sign": "true", "country": "IL", "city": city, "state": state, "key": API_KEY,
                                       "page": per_page, "offset": offset, "fields":"event_hosts"}
            if topic is not None:
                t = {"topic": topic}
                request.update(t)
            if datetime is not None:
                ti = {"time": datetime}
                request.update(ti)

            while (results_we_got == per_page):
                response = get_results(request)
                time.sleep(1)
                offset += 1

               # print response
                print 100*"-"
                for res in response['results']:
                    print res['name']  #name
                    print res['time'] #miliseconds
                    try: #Address
                        address = res['venue']['address_1']
                        print address
                    except:
                        pass
                    print res['yes_rsvp_count'] #Attendees
                    print res['description'] #description
                    print res['event_url'] #link

                    for host in res['event_hosts']: #Owner
                        print host['member_name']





                print 100*"-"
                # if response is not None:
                    # results_we_got = response['meta']['count']
                    # for res in response['results']:
                    #     category = ""
                    #     if "topic" in res:
                    #         category = res['topic']['name']
                    #     print "\n"+"," .join(map(unicode, [city, res['name'].replace(","," "), res['description'], category]))

 # group['topic'], category,group['members'],group['status'],group.get('organizer_id',""),,group.get('who',"").replace(","," ")
                time.sleep(1)


def get_results(params):
    request = requests.get("http://api.meetup.com/2/open_events",params=params)
    data = request.json()
    return data

if __name__=="__main__":
    temp = SearchHandler()
    temp.query("Jerusalem")


search = webapp2.WSGIApplication([
    ('/search', SearchHandler)
], debug=True)




"""
self.categories = [{"Arts & Culture": 1},
                            {"Career & Business": 2},
                            {"Cars & Motorcycles": 3},
                            {"Community & Environment": 4},
                            {"Dancing": 5},
                            {"Education & Learning": 6},
                            {"Fashion & Beauty": 8},
                            {"Fitness": 9},
                            {"Food & Drink": 10},
                            {"Games": 11},
                            {"Movements & Politics": 13},
                            {"Health & Wellbeing": 14},
                            {"Hobbies & Crafts": 15},
                            {"Language & Ethnic Identity": 16},
                            {"LGBT": 12},
                            {"Lifestyle": 17},
                            {"Literature & Writing": 18},
                            {"Movies & Film": 20},
                            {"Music": 21},
                            {"New Age & Spirituality": 22}]
"""