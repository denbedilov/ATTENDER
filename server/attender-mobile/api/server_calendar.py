__author__ = 'itamar'
from facebook_logic import fb_logic
import json
import logging
import webapp2
from DAL import DAL


class APICalendarHandler(webapp2.RequestHandler):

    def get(self):
        token = self.request.get("token").encode('ascii', 'ignore')
        if token == "":
            self.post(False)
        else:
            fb = fb_logic()
            if fb.check_token(token) is not False:
                id = fb.check_user(token)
                mydb = DAL()
                replyJson = mydb.get_all_user_events(id)
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
            reply_json = json.dumps(status)
            self.response.write(reply_json)

calendar = webapp2.WSGIApplication([
    ('/calendar', APICalendarHandler)
], debug=True)
