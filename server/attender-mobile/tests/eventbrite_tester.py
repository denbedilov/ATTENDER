__author__ = 'olesya'

import unittest
from api_request import ApiRequest
from sources_wrapper import SearchEventsUsingAPI
from eventbrite_api import EventbriteApi
import json

from google.appengine.ext import ndb
from google.appengine.ext import testbed
from google.appengine.api import apiproxy_stub_map


try:
    from google.appengine.api import urlfetch
    _httplib = 'urlfetch'
except ImportError:
    pass



class MeetupEventsTester(unittest.TestCase):
    def setUp(self):
        self.api_object = ApiRequest()
        self.wrapper_object = SearchEventsUsingAPI()
        self.eventbrite_object = EventbriteApi()

        self.testbed = testbed.Testbed()
        self.testbed.activate()
        self.testbed.init_datastore_v3_stub()
        self.testbed.init_memcache_stub()

        ndb.get_context().clear_cache()

        self.testbed.init_urlfetch_stub()

    def test_get_category(self):
        self.assertEqual(self.api_object.get_category("Career", "eventbrite"), 101)
        self.assertEqual(self.api_object.get_category("Community", "eventbrite"), 113)
        self.assertEqual(self.api_object.get_category("Entertainment", "eventbrite"), 104)
        self.assertEqual(self.api_object.get_category("Fitness", "eventbrite"), 108)
        self.assertEqual(self.api_object.get_category("Health", "eventbrite"), 107)
        self.assertEqual(self.api_object.get_category("New Age", "eventbrite"), 114)
        self.assertEqual(self.api_object.get_category("Politics", "eventbrite"), 112)
        self.assertEqual(self.api_object.get_category("Socializing", "eventbrite"), 109)
        self.assertEqual(self.api_object.get_category("Tech", "eventbrite"), 102)
        self.assertEqual(self.api_object.get_category("Transport", "eventbrite"), 118)

    def test_get_wrong_category(self):
        self.assertEqual( self.api_object.get_category("Car", "eventbrite"), 401)

    def test_cities_list(self):
        print self.api_object.possible_cities("eventbrite")
        self.assertIsNotNone(self.api_object.possible_cities("eventbrite"))

    def test_get_events_by_category(self):
        events = self.wrapper_object.eventbrite_response(category="Career")
        print events

        self.assertTrue(json.loads(events))
        events_list = json.loads(events)
        for ev in events_list:
            print ev
            print '\n'

    def test_get_events_by_city(self):
        events = self.wrapper_object.eventbrite_response(city="Jerusalem")
        print events

        self.assertTrue(json.loads(events))
        events_list = json.loads(events)
        for ev in events_list:
            print ev
            print '\n'

    def test_get_events_by_time(self):
        events = self.wrapper_object.eventbrite_response(date_and_time="1d")
        self.assertTrue(json.loads(events))
        events_list = json.loads(events)
        for ev in events_list:
            print ev
            print '\n'