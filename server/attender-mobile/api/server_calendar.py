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
            if mydb.check_token(token) is not False:
                # user_id = fb.check_user(token)
                replyJson = mydb.get_all_user_events(int(token))
                self.post(replyJson)
            else:
                self.post(0)

    def post(self,status):
        if status is False:
            self.response.status(400)
            self.response.write("ERROR: Missing ID")
        elif status is 0:
            self.response.status(401)
            self.response.write("ERROR: Wrong ID")
        else:
            self.response.write(status)

calendar = webapp2.WSGIApplication([
    ('/calendar', APICalendarHandler)
], debug=True)
