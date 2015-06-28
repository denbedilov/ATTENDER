__author__ = 'olesya'

import unittest
import json
from engine.search_events_interface import EventSearch
from google.appengine.ext import ndb
from google.appengine.ext import testbed

try:
    from google.appengine.api import urlfetch
    _httplib = 'urlfetch'
except ImportError:
    pass


class EventsTester(unittest.TestCase):
    def setUp(self):
        self.object =EventSearch()

        self.testbed = testbed.Testbed()
        self.testbed.activate()
        self.testbed.init_datastore_v3_stub()
        self.testbed.init_memcache_stub()

        ndb.get_context().clear_cache()

        self.testbed.init_urlfetch_stub()

    def test_get_events(self):
        events = self.object.get_events(category="Transport")
        print events

        self.assertTrue(json.loads(events))
        events_list = json.loads(events)
        for ev in events_list:
            print ev["city"]
            print '\n'