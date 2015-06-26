__author__ = 'itamar'

import webapp2
from engine.DAL import DAL


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
            mydb = DAL()
            try:
                int_token = int(_token)
                if mydb.check_token(int_token) is True:  #check if the token is valid
                    if attend_func == "true":
                        self.post(mydb.attend(int_token, int(eventid)))
                    elif attend_func == "false":
                        self.post(mydb.unattend(int_token, int(eventid)))
                else:
                    self.post(-3)
                    return
            except ValueError:
                self.post(3)

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
        elif received is 3:
            self.response.set_status(404)
            self.response.write("ERROR: Invalid id. Should be integer!")
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