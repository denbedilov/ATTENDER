__author__ = 'itamar'

import sys
import json
import logging
import webapp2
import facebook
import hashlib
import jinja2
import hmac
from DAL import DAL
sys.path.insert(0, 'lib')  #we need this line in order to make libraries imported from lib folder work properly
import requests

FACEBOOK_APP_ID = "683953828381840"

class APILoginHandler(webapp2.RequestHandler):

    def get(self):
        received = False
        id = self.request.get("id").encode('ascii', 'ignore')
        token = self.request.get("token").encode('ascii', 'ignore')
        if id == "" or  token == "":
            received = False
        else:
            received = validate_fb_login(id,token)
            logging.info(received)

        self.post(received)

    def post(self, received):
        if received == False:
            self.response.set_status(400)
            self.response.write("ERROR: Missing parameters")
            return
        elif received == 1:
             self.response.write("Session Aouth Failed")
        else:
            self.response.set_status(200)
            self.response.write("OK")
            return


def validate_fb_login(id,access_token):
    graph = facebook.GraphAPI(access_token)
    user = graph.get_object("me")
    _id = user['id']
    if id == _id:
        mydb = DAL()
        mydb.set_user_details(id,user['name'],user['last_name'])
        return True
    else:
        return 1

def get_results(request_url, params):
    request = requests.get(request_url, params=params, verify=True)
    data = request.json()
    return data, request.status_code


login = webapp2.WSGIApplication([
    ('/login', APILoginHandler)
], debug=True)