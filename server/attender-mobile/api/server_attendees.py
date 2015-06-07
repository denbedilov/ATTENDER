__author__ = 'itamar'

from facebook_logic import fb_logic
import logging
import webapp2
from DAL import DAL

class APIAttendeesHandler(webapp2.RequestHandler):
    mydb = DAL()

    def get(self):
        reply = -1
        received = False
        eventid = self.request.get("eventid").encode('ascii', 'ignore')
        token = self.request.get("token").encode('ascii','ignore')
        logging.info("eventid: "+eventid)
        if eventid == "" or token == "":
            self.post(-1)
        else:
            if self.mydb.check_token(int(token)) is not False:
                    self.post(self.mydb.get_attendings(int(eventid),int(token)))
            else:
                self.post(2)
        '''
        Db Returns:
            JSON containing data
            OR
            1 - No Such ID
            0 - No Attendees
        '''

    def post(self, received):
        if received == -1:
            self.response.set_status(400)
            self.response.write("ERROR: Missing parameters")
            return
        elif received == 1:
            self.response.set_status(401)
            self.response.write("ERROR: No Such ID")
            return
        elif received == 0:
            self.response.set_status(402)
            self.response.write("ERROR: No Attendees")
            return
        elif received == 2:
            self.response.set_status(403)
            self.response.write("ERROR: Invalid Token")
            return
        else:
            self.response.set_status(200)
            self.response.write(received)
            return




attendees = webapp2.WSGIApplication([
    ('/attendees', APIAttendeesHandler)
], debug=True)