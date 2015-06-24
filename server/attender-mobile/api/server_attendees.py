__author__ = 'itamar'

import webapp2
from engine.DAL import DAL

class APIAttendeesHandler(webapp2.RequestHandler):
    mydb = DAL()

    def get(self):
        reply = -1
        received = False
        eventid = self.request.get("eventid").encode('ascii', 'ignore')
        token = self.request.get("token").encode('ascii','ignore')
        fb_token = self.request.get("fbtoken").encode('ascii','ignore')
        if eventid == "" or token == "":
            self.post(-1)
        else:
            if fb_token == "":
                fb_token = None

            try:
                int_token = int(token)
                if self.mydb.check_token(int_token) is not False:
                    self.post(self.mydb.get_attendings(int(eventid), int_token, fb_token))

                else:
                    self.post(2)

            except ValueError:
                self.post(3)



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
            self.response.write("ERROR: No Such event ID")
            return
        elif received == 0:
            self.response.set_status(402)
            self.response.write("ERROR: No Attendees")
            return
        elif received == 2:
            self.response.set_status(403)
            self.response.write("ERROR: Invalid Token")
            return
        elif received == 3:
            self.response.set_status(404)
            self.response.write("ERROR: Invalid token. Should be integer!")
            return
        else:
            self.response.set_status(200)
            self.response.write(received)
            return




attendees = webapp2.WSGIApplication([
    ('/attendees', APIAttendeesHandler)
], debug=True)