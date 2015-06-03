__author__ = 'itamar'

import sys
from facebook_logic import fb_logic
import logging
import webapp2
from DAL import DAL

sys.path.insert(0, 'lib')  #we need this line in order to make libraries imported from lib folder work properly
import requests

FACEBOOK_APP_ID = "683953828381840"

class APILoginHandler(webapp2.RequestHandler):

    def get(self):
        received = False
        _id = self.request.get("id").encode('ascii', 'ignore')
        token = self.request.get("token").encode('ascii', 'ignore')
        if _id == "" or token == "":
            received = False
        else:
            fb = fb_logic()
            if fb.test_id(_id) is False:
                received = 2
            else:
                fb = fb_logic()
                if fb.validate_fb_login(_id, access_token=token) is not False:
                    mydb = DAL()
                    user = fb.validate_fb_login(_id, access_token=token)
                    logging.info(user)
                    mydb.set_user_details(user_id=int(_id), name=user['first_name'].encode('ascii', 'ignore'),
                                          last_name=user['last_name'].encode('ascii', 'ignore'),
                                          email = user["email"].encode('ascii', 'ignore'))

                    received = True
                    logging.info("received is True")
                else:
                    received = -1

        logging.info(received)
        self.post(received)

    def post(self, received):
        if received is False:
            self.response.set_status(400)
            self.response.write("ERROR: Missing parameters")
            return
        elif received == -1:
            self.response.set_status(401)
            self.response.write("Session Aouth Failed")
        elif received == 2:
            self.response.set_status(402)
            self.response.write("Invalid ID")
        elif received is True:
            self.response.set_status(200)
            self.response.write("OK")
            return




def get_results(request_url, params):
    request = requests.get(request_url, params=params, verify=True)
    data = request.json()
    return data, request.status_code


login = webapp2.WSGIApplication([
    ('/login', APILoginHandler)
], debug=True)