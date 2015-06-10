__author__ = 'itamar'
from facebook_logic import fb_logic
import webapp2
from DAL import DAL


class APICalendarHandler(webapp2.RequestHandler):

    def get(self):
        token = self.request.get("token").encode('ascii', 'ignore')
        if token == "":
            self.post(False)
        else:
            # fb = fb_logic()
            mydb = DAL()
            try:
                inttoken = int(token)
                if mydb.check_token(inttoken) is not False:
                    replyJson = mydb.get_all_user_events(inttoken)
                    self.post(replyJson)
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
