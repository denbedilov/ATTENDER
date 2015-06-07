__author__ = 'itamar'

import sys
import logging
import webapp2
from DAL import DAL
from google.appengine.api import mail

class UserLoginHandler(webapp2.RequestHandler):
    def get(self):
        email = self.request.get("email").encode('ascii', 'ignore')
        hashed_password = self.request.get("password")
        first_name = self.request.get("firstname")
        last_name = self.request.get("lastname")
        if not mail.is_email_valid(email):
            self.post(-4)
            return

        if email is "" or hashed_password is "":
            self.post(-1)
            return
        # if first_name is "":
        #     self.post(-2)
        # if last_name is "":
        #     self.post(-3)

        mydb = DAL()
        user = mydb.user_login(email,hashed_password)
        if user is False or user is 2:
            if first_name is not  "" and last_name is not "":
                user = mydb.register(email, hashed_password, first_name, last_name)
                logging.info("in register  "+str(user))
            elif first_name is not "" and last_name is "":
                self.post(-3)
            elif first_name is "" and last_name is not "":
                self.post(-2)
            else:
                self.post(False)
        logging.info("after if   "+str(user))
        self.post(user)

    def post(self,response):
        if response is -4:
            self.response.set_status(403)
            self.response.write("Invalid mail")
        if response is -3:
            self.response.set_status(402)
            self.response.write("Missing Last Name")
        if response is -2:
            self.response.set_status(401)
            self.response.write("Missing First Name")
        if response is -1:
            self.response.set_status(400)
            self.response.write("Missing Parameters")
        if response is False:
            self.response.set_status(501)
            self.response.write("User Not Exist")
        if response is 1:
            self.response.set_status(500)
            self.response.write("Wrong Password")
        else:
            self.response.set_status(200)
            logging.info("in else")
            self.response.write(response)

user = webapp2.WSGIApplication([
    ('/userlogin', UserLoginHandler)
], debug=True)