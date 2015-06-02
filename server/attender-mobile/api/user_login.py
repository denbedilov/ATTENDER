__author__ = 'itamar'

import sys
import logging
import webapp2
from DAL import DAL

class UserLoginHandler(webapp2.RequestHandler):
    def get(self):
        email = self.request.get("email")
        hashed_password = self.request.get("password")
        user_id = self.request.get("username")

        if email is "" or hashed_password is "" or user_id is "":
            self.post(-1)
            return

        '''
        check_if_user_exist()
            returns:
                False - if user is not exist
                1 - if user name exist with different email
                2 - if email exist with different user name
                3 - wrong password
                userid - if user exist
        user_sign_in()
            creating new user.
            returns:
                userid - user created correctly
        '''
        mydb = DAL()
        user = mydb.check_if_user_exist(email,hashed_password,user_id)
        if user is False:
            token = mydb.user_sign_in(email,hashed_password,user_id)
            self.post(token)
        else:
            self.post(user)

    def post(self,response):
        if response is -1:
            self.response.set_status(400)
            self.response.write("Missing Parameters")
        if response is 1:
            self.response.set_status(500)
            self.response.write("User Already exist")
        if response is 2:
            self.response.set_status(501)
            self.response.write("Email Already Exist")
        if response is 3:
            self.response.set_status(502)
            self.response.write("wrong password")
        else:
            self.response.set_status(200)
            self.response.write(response)

user = webapp2.WSGIApplication([
    ('/userlogin', UserLoginHandler)
], debug=True)