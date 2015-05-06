__author__ = 'olesya'

import unittest
from DAL import DAL
from SearchEventsInterface import SearchUsingAPI
from google.appengine.ext.ndb import query

class UserDetails(unittest.TestCase):
    def setUp(self):
        self.d = DAL()
        self.obj = SearchUsingAPI()

    def test_get_name(self):
        self.assertEqual(self.d.get_user_details("user_name"),"oles_ka")

    def test_set_name(self):
        us_list = self.d.set_user_details("itamar", "sn@dd.com", "123")
        self.assertEqual(us_list.pop().user_name ,"itamar")

    def test_set_event(self):
        events = self.obj.request_events(category="Fitness")
        print events
        self.assertTrue(True)

    def test_pull_from_db(self):
        e = SearchUsingAPI()
        result = e.pull_from_db(category="Fitness", date_and_time="1w")
        self.assertIsInstance(result, query.Query)

def main():
    unittest.main()

if __name__ == "__main__":
    main()