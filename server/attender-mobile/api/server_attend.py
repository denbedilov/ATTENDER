__author__ = 'itamar'


import json
import logging
import webapp2
#TODO add the right imports
class APIAttendHandler(webapp2.RequestHandler):

    def get(self):
        received = 0
        #TODO create a user db object
        id = self.request.get("id").encode('ascii', 'ignore')
        eventid = self.request.get("eventid").encode('ascii', 'ignore')
        logging.info("is:"+ id+"\nid: "+id+"\neventid: "+eventid)
        if eventid is "":
            received = -1
        if id is "":
            received = -2

        #TODO send to the Db
        '''returns:
                0 = OK
                1 = wrong ID
                2 = wrong Event ID
        '''
        self.post(received)

    def post(self, received):
        if received is -2:
            self.response.set_status(400)
            self.response.write("ERROR: Missing User ID")
            return
        elif received is -1:
            self.response.set_status(400)
            self.response.write("ERROR: Missing Event ID")
            return
        elif received is 1:
            self.response.set_status(400)
            self.response.write("ERROR: Event ID not found")
            return
        elif received is 2:
            self.response.set_status(400)
            self.response.write("ERROR: No Such User")
            return
        else:
            self.response.set_status(200)
            self.response.write("OK")
            return



login = webapp2.WSGIApplication([
    ('/attend', APIAttendHandler)
], debug=True)