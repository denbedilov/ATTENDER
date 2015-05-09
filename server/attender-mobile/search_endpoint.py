

import json
import logging
import webapp2
from models.Event import Event
# from protorpc import messages
# from protorpc import message_types
# from protorpc import remote
from SearchEventsInterface import EventSearch

class APIHandler(webapp2.RequestHandler):

    def get(self):
        res = EventSearch()
        city = self.request.get("city").encode('ascii','ignore')
        category = self.request.get("category").encode('ascii','ignore')
        time = self.request.get("time").encode('ascii','ignore')
        logging.info(type(city))
        logging.info("city:"+ city+"\ncategory: "+category+"\ntime: "+time)
        replyJson = res.get_events(city = None if city == "" else city,category =  None if category == "" else category,date_and_time = None if time == "" else time)
        logging.info("trying to prove itamar is wrong"+replyJson)
        self.post(replyJson)
        # else:
        #     self.post('[]')

    def post(self, replyJson = None):
        pass
         # time.sleep(1)
        # if replyJson =='[]':
        #     self.response.set_status(400)
        #     self.response.write('No result for this query')
        #     list = []
        #     replyJson = json.dumps(list.append("Empty Result"))
        #     return
        # else:
        #     if replyJson is not None:
        self.response.write(replyJson)
            # self.response.write(json.dumps(replyJson))




app = webapp2.WSGIApplication([
    ('/api', APIHandler)
], debug=True)