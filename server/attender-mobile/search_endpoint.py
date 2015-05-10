

import json
import logging
import webapp2
from SearchEventsInterface import EventSearch

class APIHandler(webapp2.RequestHandler):

    def get(self):
        res = EventSearch()
        city = self.request.get("city").encode('ascii', 'ignore')
        category = self.request.get("category").encode('ascii', 'ignore')
<<<<<<< HEAD
        category = category.rstrip()
=======
        category = category.strip()
>>>>>>> a523c8ba9998f7fff36ea3c76fd60413854e0786
        time = self.request.get("time").encode('ascii', 'ignore')
        logging.info("city:"+ city+"\ncategory: "+category+"\ntime: "+time)
        reply_json = res.get_events(city=None if city == "" else city, category=None if category == "" else category, date_and_time=None if time == "" else time)
        logging.info("printing the result in json format" + reply_json)
        self.post(reply_json)


    def post(self, replyJson = None):
        if replyJson == '[]':
            self.response.set_status(400)
            self.response.write('[]')
            list = []
            reply_json = json.dumps(list.append("Empty Result"))
            return
        else:
            self.response.write(replyJson)
            return



app = webapp2.WSGIApplication([
    ('/api', APIHandler)
], debug=True)