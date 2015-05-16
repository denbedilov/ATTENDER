__author__ = 'itamar'


import json
import logging
import webapp2
from DAL import DAL

class APIAttendeesHandler(webapp2.RequestHandler):
    mydb = DAL()
    def get(self):
        reply = -1
        received = False
        #TODO create a user db object
        id = self.request.get("eventid").encode('ascii', 'ignore')
        logging.info("eventid: "+id)
        if id == "":
            self.post(-1)
        else:
            self.post(self.mydb.get_attendings(int(id)))

        '''
        Db Returns:
            JSON containing data
            OR
            1 - No Such ID
            0 - No Attendees
        '''

    def post(self, attendees):
        if attendees == -1:
            self.response.set_status(400)
            self.response.write("ERROR: Missing parameters")
            return
        elif attendees == 1:
            self.response.set_status(401)
            self.response.write("ERROR: No Such ID")
            return
        elif attendees == 0:
            self.response.set_status(402)
            self.response.write("ERROR: No Attendees")
            return
        else:
            self.response.set_status(200)
            reply_json = json.dumps(attendees)
            self.response.write(reply_json)
            return



attendees = webapp2.WSGIApplication([
    ('/attendees', APIAttendeesHandler)
], debug=True)