__author__ = 'itamar'
from google.appengine.api import users
from google.appengine.ext.webapp.util import login_required
import logging
import webapp2
from DAL import DAL

class GoogleLoginHandler(webapp2.RequestHandler):
    @login_required
    def get(self):
        firstname = self.request.get("firstname")
        lastname = self.request.get("lastname")
        logging.info("entring user name:")

        logging.info(firstname)
        logging.info(lastname)
        user = users.get_current_user()
        if user is not None:
            mydb =DAL()
            logging.info(user.nickname())
            token = mydb.register(user.email(), None, firstname,lastname)
            self.response.write(token)
        else:
            self.post(False)

    def post(self,response):
        if response is not False:
            self.response.set_status("200")
            self.response.write(response)
        else:
            self.response.set_status("400")
            self.response.write("Aouth Failed")



googlelogin = webapp2.WSGIApplication([
    ('/googlelogin', GoogleLoginHandler)
], debug=True)