__author__ = 'itamar'

import sys
import logging
import webapp2
from DAL import DAL
from google.appengine.api import mail
import re


qtext = '[^\\x0d\\x22\\x5c\\x80-\\xff]'
dtext = '[^\\x0d\\x5b-\\x5d\\x80-\\xff]'
atom = '[^\\x00-\\x20\\x22\\x28\\x29\\x2c\\x2e\\x3a-\\x3c\\x3e\\x40\\x5b-\\x5d\\x7f-\\xff]+'
quoted_pair = '\\x5c[\\x00-\\x7f]'
domain_literal = "\\x5b(?:%s|%s)*\\x5d" % (dtext, quoted_pair)
quoted_string = "\\x22(?:%s|%s)*\\x22" % (qtext, quoted_pair)
domain_ref = atom
sub_domain = "(?:%s|%s)" % (domain_ref, domain_literal)
word = "(?:%s|%s)" % (atom, quoted_string)
domain = "%s(?:\\x2e%s)*" % (sub_domain, sub_domain)
local_part = "%s(?:\\x2e%s)*" % (word, word)
addr_spec = "%s\\x40%s" % (local_part, domain)
email_address = re.compile('\A%s\Z' % addr_spec)





class UserLoginHandler(webapp2.RequestHandler):
    def get(self):
        email = self.request.get("email")#.encode('ascii', 'ignore')
        hashed_password = self.request.get("password")
        first_name = self.request.get("firstname")
        last_name = self.request.get("lastname")

        mydb = DAL()

        if email is "" or hashed_password is "":
            self.post(-1)
        elif email is not "" and hashed_password is not "":
            isvalid = isValidEmailAddress(email)
            logging.info(isvalid)
            if not isvalid:
                self.post(-4)
            else:
                user = mydb.user_login(email,hashed_password)
                if user is False or user is 2:
                    if first_name is not "" and last_name is not "":
                        user = mydb.register(email, hashed_password, first_name, last_name)
                        logging.info("in register  " + str(user))
                    elif first_name is not "" and last_name is "":
                        user = -3
                    elif first_name is "" and last_name is not "":
                        user = -2
                    else:
                        user = False
                self.post(user)

    def post(self,response):
        if response is -4:
            self.response.set_status(403)
            self.response.write("Invalid mail")
        elif response is -3:
            self.response.set_status(402)
            self.response.write("Missing Last Name")
        elif response is -2:
            self.response.set_status(401)
            self.response.write("Missing First Name")
        elif response is -1:
            self.response.set_status(400)
            self.response.write("Missing Parameters")
        elif response is False:
            self.response.set_status(501)
            self.response.write("User Not Exist")
        elif response is 1:
            self.response.set_status(500)
            self.response.write("Wrong Password")
        else:
            self.response.set_status(200)
            self.response.write(response)

def isValidEmailAddress(email):
    if email_address.match(email):
        return True
    else:
        return False

user = webapp2.WSGIApplication([
    ('/userlogin', UserLoginHandler)
], debug=True)