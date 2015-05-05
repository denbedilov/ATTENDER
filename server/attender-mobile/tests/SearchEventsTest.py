__author__ = 'olesya'

import unittest
from EventSearch import SearchHandler
import json


class SearchEvents(unittest.TestCase):
    def setUp(self):
        self.obj = SearchHandler()

    def test_get_json_events(self):

        events = self.obj.get_events(category="Tech")
        print events
        self.assertTrue(json.loads(events))

    def test_get_empty_result(self):
        events = self.obj.get_events(category="Tech")
        self.assertRaises(json.loads(events))

def main():
    unittest.main()

if __name__ == "__main__":
    main()