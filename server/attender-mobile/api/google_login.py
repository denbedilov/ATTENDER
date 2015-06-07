__author__ = 'itamar'
from google.appengine.api import users
from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import login_required
import logging
import webapp2
from DAL import DAL

class GoogleLoginHandler(webapp2.RequestHandler):
    @login_required
    def get(self):
        user = users.get_current_user()
        if user is not None:
            self.post(True)
        else:
            self.post(False)
        self.response.out.write('Hello, ' + user.nickname())

    def post(self,response):
        if response is not None:
            self.response.set_status("200")
            self.response.write(response)
        else:
            self.response.set_status("400")
            self.response.write("Aouth Failed")

googlelogin = webapp2.WSGIApplication([
    ('/googlelogin', GoogleLoginHandler)
], debug=True)