__author__ = 'olesya'

import unittest
from SearchEventsInterface import SearchUsingAPI
import json
import datetime

class SearchEventsTester(unittest.TestCase):
    def setUp(self):
        self.obj = SearchUsingAPI()

    def test_get_json_events(self):
        events = self.obj.request_events(category="Career & Business")
        print events

        self.assertTrue(json.loads(events))
        events_list = json.loads(events)
        for ev in events_list:
            print ev
            print '\n'

    def test_require_bad_category_exception_thrown(self):
        events = self.obj.request_events(category="Music")
        self.assertRaises(json.loads(events))

    def test_get_empty_json(self):
        events = self.obj.request_events(category="Cars & Motorcycles")
        self.assertEqual(events, '[]')

    def test_get_events_by_time(self):
        events = self.obj.request_events(date_and_time=",3m")
        events_list = json.loads(events)

        for ev in events_list:
            sec = ev['date'] /1000
            print datetime.datetime.fromtimestamp(sec).strftime('%Y-%m-%d %H:%M:%S')
        self.assertTrue(True)

    def test_get_cities(self):
        cities = self.obj.request_city(10)
        print cities

def main():
    unittest.main()

if __name__ == "__main__":
    main()