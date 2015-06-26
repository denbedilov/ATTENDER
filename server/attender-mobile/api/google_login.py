__author__ = 'itamar'
from google.appengine.api import users
from google.appengine.ext.webapp.util import login_required
import logging
from google.appengine.api import oauth

import webapp2
from engine.DAL import DAL

class GoogleLoginHandler(webapp2.RequestHandler):
    def get(self):
        firstname = self.request.get("firstname")
        lastname = self.request.get("lastname")
        email = self.request.get("email")
        token = False
        if firstname == "" or lastname == "" or email == "":
            token = -1
        else:
            mydb =DAL()
            logging.info("entring user name:")
            logging.info(firstname)
            logging.info(lastname)
            logging.info(email)

            token = mydb.google_login(email, firstname,lastname)
        self.post(token)

    def post(self,response):
        if response is -1:
            self.response.set_status("400")
            self.response.write("ERROR: Missing Parameters")
        elif response is 1:
            self.response.set_status(500)
            self.response.write("ERROR: Wrong Password")
        elif response is 2:
            self.response.set_status(502)
            self.response.write("ERROR: User already exist!")
        else:
            self.response.set_status("200")
            self.response.write(response)



googlelogin = webapp2.WSGIApplication([
    ('/googlelogin', GoogleLoginHandler)
], debug=True)