# coding=utf-8
__author__ = 'olesya'
import unittest
import json
import datetime
from engine.api_request import ApiRequest
from sources_wrapper import SearchEventsUsingAPI
from engine.meetup_api import MeetupApi
from google.appengine.ext import ndb
from google.appengine.ext import testbed

class MeetupEventsTester(unittest.TestCase):
    def setUp(self):
        self.api_object = ApiRequest()
        self.wrapper_object = SearchEventsUsingAPI()
        self.meetup_object = MeetupApi()

        self.testbed = testbed.Testbed()
        self.testbed.activate()
        self.testbed.init_datastore_v3_stub()
        self.testbed.init_memcache_stub()
        ndb.get_context().clear_cache()

    def test_get_category(self):
        self.assertEqual(self.api_object.get_category("Career", "meetup"), 2)

    def test_get_wrong_category(self):
        self.assertEqual( self.api_object.get_category("Car", "meetup"), 401)

    def test_require_bad_category_exception_thrown(self):
        events = self.wrapper_object.meetup_response(category="Music")
        self.assertEqual(events, 401)

    def test_get_json_events_meetup(self):
        events = self.wrapper_object.meetup_response(category="Career")
        print events

        self.assertTrue(json.loads(events))
        events_list = json.loads(events)
        for ev in events_list:
            print ev
            print '\n'

    def test_get_empty_json(self):
        events = self.wrapper_object.meetup_response(category="Transport")
        self.assertEqual(events, '[]')

    def test_get_events_by_time(self):
        events = self.wrapper_object.meetup_response(date_and_time="3m")
        events_list = json.loads(events)

        for ev in events_list:
            sec = ev['date'] /1000
            print datetime.datetime.fromtimestamp(sec).strftime('%Y-%m-%d %H:%M:%S')
        self.assertTrue(True)

    def test_get_cities(self):
        cities = self.meetup_object.request_city(10)
        print cities

    def test_unicode(self):
        flag = False
        if 'ירושלים' in ["Jerusalem", "jerusalem", 'ירושלים']:
           flag = True
        self.assertTrue(flag)



if __name__ == "__main__":
    unittest.main()