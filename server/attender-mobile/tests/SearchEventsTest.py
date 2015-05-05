__author__ = 'olesya'

import unittest
from EventSearch import EventSearch
import json
import datetime

class SearchEventsTester(unittest.TestCase):
    def setUp(self):
        self.obj = EventSearch()

    def test_get_json_events(self):
        events = self.obj.get_events(category="Fitness")
        print events

        self.assertTrue(json.loads(events))
        events_list = json.loads(events)
        for ev in events_list:
            print ev
            print '\n'

    def test_get_empty_result(self):
        events = self.obj.get_events(category="Music")
        self.assertRaises(json.loads(events))

    def test_get_events_by_time(self):
        events = self.obj.get_events(datetime=",3m")
        events_list = json.loads(events)

        for ev in events_list:
            sec = ev['date'] /1000
            print datetime.datetime.fromtimestamp(sec).strftime('%Y-%m-%d %H:%M:%S')
        self.assertTrue(True)


def main():
    unittest.main()

if __name__ == "__main__":
    main()