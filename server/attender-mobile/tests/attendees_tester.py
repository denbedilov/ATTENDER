__author__ = 'olesya'


import unittest
from engine.DAL import DAL
from engine.search_events_interface import SearchEventsUsingAPI
from models.user import User
from models.event import Event
from datetime import datetime
import json

from google.appengine.ext import ndb
from google.appengine.ext import testbed


class UserDetails(unittest.TestCase):
    def setUp(self):
        # First, create an instance of the Testbed class.
        self.testbed = testbed.Testbed()
        # Then activate the testbed, which prepares the service stubs for use.
        self.testbed.activate()
        # Next, declare which service stubs you want to use.
        self.testbed.init_datastore_v3_stub(User)
        self.testbed.init_memcache_stub()
        # Clear ndb's in-context cache between tests.
        # This prevents data from leaking between tests.
        # Alternatively, you could disable caching by
        # using ndb.get_context().set_cache_policy(False)
        ndb.get_context().clear_cache()
        self.mydb = DAL()
        self.obj = SearchEventsUsingAPI()
        event_id = self.mydb.set_event_details("222342395", "Hadoop Ecosystem Workshop", datetime.now(),
                                               "Tel Aviv-Yafo",  "Kiryat Atidim", "long-story-short", "rika pedro-shoham", "http://www.meetup.com", 64, "free", "All", "meetup")
        self.ev = event_id.id()

        self.mydb.set_user_details(10204308876621622, 'Itamar', 'Sharify', 'email@gmail.com')
        self.mydb.set_user_details(10204308876621633, 'Olesya', 'Shapira', 'email1@gmail.com')
        self.mydb.set_user_details(10204308876621644, 'Rita', 'Markovich', 'email2@gmail.com')

    def test_get_attendings_after_attend(self):
        self.mydb.attend(2, self.ev)
        self.mydb.attend(3, self.ev)
        self.mydb.attend(4, self.ev)
        res1 = self.mydb.get_attendings(self.ev, 4)
        self.assertTrue(json.loads(res1))

    def test_get_attendings_after_unattend(self):
        self.mydb.attend(2, self.ev)
        self.mydb.unattend(2, self.ev)
        res1 = self.mydb.get_attendings(self.ev, 4)
        self.assertEqual(res1, '[]')

    def _test_get_attendings_not_my_self(self):
        self.mydb.attend(2, self.ev)
        res1 = self.mydb.get_attendings(self.ev, 2)
        self.assertEqual(res1, '[]')

    def test_attend(self):
        res = self.mydb.attend(2, self.ev)
        self.assertEqual(0, res)

    def test_attend_wrong_user_id_return_1(self):
        res = self.mydb.attend(1, self.ev)
        self.assertTrue(1, res)

    def test_attend_wrong_event_id_return_2(self):
        res = self.mydb.attend(2, 12)
        self.assertTrue(2, res)

    def test_unattend(self):
        self.mydb.attend(2, self.ev)
        res = self.mydb.unattend(2, self.ev)
        self.assertEqual(0, res)

    def test_get_all_user_events(self):
        self.mydb.attend(2, self.ev)
        event_id = self.mydb.set_event_details("2296", "Some Event", datetime.now(),
                                               "Tel Aviv-Yafo",  "Kiryat Atidim", "long-story-short", "rika pedro-shoham", "http://www.meetup.com", 64, "free", "All", "meetup")

        self.mydb.attend(2, event_id.id())
        res = self.mydb.get_all_user_events(2)
        print res
        self.assertTrue(json.loads(res))

    def tearDown(self):
        self.testbed.deactivate()