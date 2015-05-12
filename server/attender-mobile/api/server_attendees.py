__author__ = 'itamar'


import json
import logging
import webapp2
#TODO add the right import
class APIAttendeesHandler(webapp2.RequestHandler):

    def get(self):
        received = False
        #TODO create a user db object
        id = self.request.get("eventid").encode('ascii', 'ignore')
        logging.info("eventid: "+id)
        if id is not "":
            received = True
        #TODO send to the Db
        '''
        Db Returns:
            JSON containing data
            OR
            0 - No Such ID
            1 - No Attendees
        '''
        self.post(received)

    def post(self, received):
        if received is False:
            self.response.set_status(400)
            self.response.write("ERROR: Missing parameters")
            return
        elif received is 0:
            self.response.set_status(401)
            self.response.write("ERROR: No Such ID")
            return
        elif received is 1:
            self.response.set_status(402)
            self.response.write("ERROR: No Attendees")
            return
        else:
            self.response.set_status(200)
            self.response.write("OK")
            return



login = webapp2.WSGIApplication([
    ('/attendees', APIAttendeesHandler)
], debug=True)