# coding=utf-8
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
from sources_wrapper import SearchEventsUsingAPI
from models.event import Event
from models.attendings import Attendings
import logging
from datetime import datetime
from api_request import ApiRequest


class DailyTreatEventsHandler(webapp2.RequestHandler):
    obj = SearchEventsUsingAPI()
    api_obj = ApiRequest()

    def get(self):
        self.response.write('Welcome to attender server! Here is a cron job for pulling events from Meetup API')

        ev = Event()
        at = Attendings()
        logging.info("Adding new events to DataStore")
        results = self.obj.request_events(radius="25")
        logging.info("Events added: {}".format(results))
        logging.info("Deleting old events from DataStore")

        #Delete passed events
        qe = ev.return_all_events()
        results = qe.filter(Event.date < datetime.now())
        for res in results:
            logging.info(str(res.key.id()))
            old_attending = Attendings.query(Attendings.event_id == int(res.key.id())).get()
            logging.info("query {}".format(old_attending))
            if old_attending is not None:
                old_attending.key.delete()
            res.key.delete()


        #Update city names
        for q in qe:
            changed = self.api_obj.check_city(q.city)
            if changed:
                q.city = changed
                q.put()

app = webapp2.WSGIApplication([
    ('/cron', DailyTreatEventsHandler)
], debug=True)


