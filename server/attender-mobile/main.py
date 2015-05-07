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
from SearchEventsInterface import EventSearch
from models.Event import Event
import logging


class MainHandler(webapp2.RequestHandler):
    def get(self):
        self.response.write('Welcome to attender server!')
        ev = Event()
        obj = EventSearch()
        #logging.info("Adding new event to datastore")
        #obj.get_events(category="Career & Business")
        logging.info("trying to find event with category 'Fitness'")
        results = obj.get_events(city = "Herzeliya", category="Career & Business", date_and_time='1w')
        #results = ev.return_all_events()
        if results is not None:
            logging.info("result count: {}".format(results.count()))
            for res in results:
                logging.info("The result is: {}".format(res.id))
                logging.info("The result is: {}".format(res.category))


app = webapp2.WSGIApplication([
    ('/', MainHandler)
], debug=True)


