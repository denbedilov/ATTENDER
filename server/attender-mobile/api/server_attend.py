__author__ = 'itamar'
from facebook_logic import fb_logic
import logging
import webapp2
from DAL import DAL


class APIAttendHandler(webapp2.RequestHandler):
    def get(self):
        received = 0
        _token = self.request.get("token").encode('ascii', 'ignore')
        eventid = self.request.get("eventid").encode('ascii', 'ignore')
        attend_func = self.request.get("isAttend").encode('ascii', 'ignore')

        if eventid == "":
            received = -1
            self.post(received)
        elif id == "":
            received = -2
            self.post(received)
        else:
            fb = fb_logic()
            if fb.check_token(token=_token):  #check if the token is valid
                mydb= DAL()
                logging.info("user id : "+fb.get_id(_token))
                if attend_func == "true":
                    self.post(mydb.attend(int(fb.get_id(_token)),int(eventid)))
                elif attend_func == "false":
                    self.post(mydb.unattend(int(fb.get_id(_token)),int(eventid)))
            else:
                self.post(-3)
            return
            # self.post(received)
        '''returns:
                0 = OK
                1 = wrong ID
                2 = wrong Event ID
        '''

    def post(self, received):
        if received is -3:
            self.response.set_status(404)
            self.response.write("ERROR: Wrong Token")
            return
        if received is -2:
            self.response.set_status(400)
            self.response.write("ERROR: Missing User Token")
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