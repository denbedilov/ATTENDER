__author__ = 'itamar'

import webapp2
from engine.DAL import DAL


class APICalendarHandler(webapp2.RequestHandler):

    def get(self):
        token = self.request.get("token").encode('ascii', 'ignore')
        if token == "":
            self.post(False)
        else:
            mydb = DAL()
            try:
                int_token = int(token)
                if mydb.check_token(int_token) is not False:
                    reply_json = mydb.get_all_user_events(int_token)
                    self.post(reply_json)
                else:
                    self.post(0)
            except ValueError:
                self.post(2)

    def post(self, status):
        if status is False:
            self.response.set_status(400)
            self.response.write("ERROR: Missing ID")
        elif status is 0:
            self.response.set_status(401)
            self.response.write("ERROR: Wrong ID")
        elif status is 2:
            self.response.set_status(402)
            self.response.write("ERROR: Invalid token. Should be integer!")
        else:
            self.response.write(status)

calendar = webapp2.WSGIApplication([
    ('/calendar', APICalendarHandler)
], debug=True)
