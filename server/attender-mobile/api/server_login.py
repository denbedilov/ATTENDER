__author__ = 'itamar'

import sys
import json
import logging
import webapp2
import facebook
from DAL import DAL
sys.path.insert(0, 'lib')  #we need this line in order to make libraries imported from lib folder work properly
import requests

FACEBOOK_APP_ID = "683953828381840"
FACEBOOK_APP_SECRET = "294d93ab1301dab751e5497bb318fb68"
FACEBOOK_URL = "https://graph.facebook.com/oauth/access_token?"
config = {}
config['webapp2_extras.sessions'] = dict(secret_key='')

class APILoginHandler(webapp2.RequestHandler):
    mydb = DAL()
    def get(self):
        received = False
        id = self.request.get("id").encode('ascii', 'ignore')
        token = self.request.get("token").encode('ascii', 'ignore')
        if id == "" or  token == "":
            received = False
            #build a Fb auth
        else:
            received = True
            request = {}
            # graph = facebook.GraphAPI(token)
            # profile = graph.get_object("me")
            # friends = graph.get_connections("me", "friends")
            #
            # friend_list = [friend['name'] for friend in friends['data']]
            self.mydb.set_user_details(int(id), "test","hey")
        self.post(received)

    def post(self, received):
        if received == False:
            self.response.set_status(400)
            self.response.write("ERROR: Missing parameters")
            return
        # elif received == 2:
        #     self.response.write("Session Aouth Failed")
        else:
            self.response.set_status(200)
            self.response.write("OK")
            return


def get_results(request_url, params):
    request = requests.get(request_url, params=params)
    data = request.json()
    return data, request.status_code
login = webapp2.WSGIApplication([
    ('/login', APILoginHandler)
], debug=True)