__author__ = 'olesya'
#!/usr/bin/env python
#
# Copyright 2007 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
import webapp2
from SearchEventsInterface import SearchUsingAPI
from models.Event import Event
import logging
from datetime import datetime

class DailyTreatEventsHandler(webapp2.RequestHandler):
    def get(self):
        self.response.write('Welcome to attender server! Here is a cron job for pulling events from Meetup API')
        obj = SearchUsingAPI()
        ev = Event()
        logging.info("Adding new events to DataStore")
        obj.request_events()
        logging.info("Deleting old events from DataStore")
        qe = ev.return_all_events()
        results = qe.filter(Event.date < datetime.now())
        for res in results:
            res.key.delete()


app = webapp2.WSGIApplication([
    ('/cron', DailyTreatEventsHandler)
], debug=True)


