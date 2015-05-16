__author__ = 'itamar'


import json
import logging
import webapp2
from DAL import DAL

class APIAttendHandler(webapp2.RequestHandler):
    def get(self):
        received = 0
        #TODO create a user db object
        id = self.request.get("id").encode('ascii', 'ignore')
        eventid = self.request.get("eventid").encode('ascii', 'ignore')
        logging.info("is:"+ id+"\nid: "+id+"\neventid: "+eventid)
        if eventid == "":
            received = -1
            self.post(received)
        elif id == "":
            received = -2
            self.post(received)
        else:
            mydb = DAL()
            received = mydb.set_attendings(int(id), int(eventid))
            self.post(received)
        '''returns:
                0 = OK
                1 = wrong ID
                2 = wrong Event ID
        '''

    def post(self, received):
        if received is -2:
            self.response.set_status(400)
            self.response.write("ERROR: Missing User ID")
            return
        elif received is -1:
            self.response.set_status(401)
            self.response.write("ERROR: Missing Event ID")
            return
        elif received is 2:
            self.response.set_status(402)
            self.response.write("ERROR: Event ID not found")
            return
        elif received is 1:
            self.response.set_status(403)
            self.response.write("ERROR: No Such User")
            return
        else:
            self.response.set_status(200)
            self.response.write("OK")
            return



attend = webapp2.WSGIApplication([
    ('/attend', APIAttendHandler)
], debug=True)