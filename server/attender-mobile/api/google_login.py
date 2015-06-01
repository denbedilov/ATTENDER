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
        self.response.out.write('Hello, ' + user.nickname())


googlelogin = webapp2.WSGIApplication([
    ('/googlelogin', GoogleLoginHandler)
], debug=True)