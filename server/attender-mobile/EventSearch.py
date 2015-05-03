# __author__ = 'itamar'
from __future__ import unicode_literals


import webapp2
import requests
# from bs4 import BeautifulSoup
import time
import codecs
import sys
# https://docs.python.org/2/howto/urllib2.html
import urllib2
from urllib import urlopen
# http://www.w3.org/TR/css3-selectors/#selectors
from models.Attendings import Attendings
import json


UTF8Writer = codecs.getwriter('utf8')
sys.stdout = UTF8Writer(sys.stdout)

URL_PATTERN =  "https://api.meetup.com/find/open_events?"
API_KEY = "185c2b3e44c4b4644365a3022d5a2f"

class SearchHandler(webapp2.RequestHandler):

    def query(self, city = None, topic = None, hour = None):
        if city!=None:
            cities = [(str(city),"IL")]#case choise was given
        else:#'stock settings'
            cities =[("Jerusalem","IL"),("Tel Aviv","IL"),("Haifa","IL")]
        # If you want to change the cities to search, do so below

        for (city, state) in cities:
            per_page = 200
            results_we_got = per_page
            offset = 0
            while (results_we_got == per_page):
                # Meetup.com documentation here: http://www.meetup.com/meetup_api/docs/2/groups/
                # You can change search perimeter around each city by changing the "radius" parameter
                response=get_results({"sign":"true","country":"IL","topic":topic, "city":city, "state":state, "key":API_KEY, "page":per_page, "offset":offset })
                time.sleep(1)
                offset += 1
                results_we_got = response['meta']['count']
                # print response
                for group in response['results']:
                    category = ""
                    if "topic" in group:
                        category = group['topic']['name']
                    print "\n"+"," .join(map(unicode, [city, group['name'].replace(","," "), group['description'], category]))

 # group['topic'], category,group['members'],group['status'],group.get('organizer_id',""),,group.get('who',"").replace(","," ")
        time.sleep(1)

def get_results(params):

    request = requests.get("http://api.meetup.com/2/open_events",params=params)
    data = request.json()

    return data

if __name__=="__main__":
    temp = SearchHandler()
    temp.query("Jerusalem", "Games")


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