__author__ = 'itamar'

import facebook
import json
import logging
import webapp2
from DAL import DAL

class APIAttendeesHandler(webapp2.RequestHandler):
    mydb = DAL()
    def get(self):
        reply = -1
        received = False
        id = self.request.get("eventid").encode('ascii', 'ignore')
        token = self.request.get("token").encode('ascii','ignore')
        logging.info("eventid: "+id)
        if id == "" or token == "":
            self.post(-1)
        else:
            if check_user(token) is not False:
                self.post(self.mydb.get_attendings(int(check_user(token))))
            else:
                self.post(2)
        '''
        Db Returns:
            JSON containing data
            OR
            1 - No Such ID
            0 - No Attendees
        '''

    def post(self, attendees):
        if attendees == -1:
            self.response.set_status(400)
            self.response.write("ERROR: Missing parameters")
            return
        elif attendees == 1:
            self.response.set_status(401)
            self.response.write("ERROR: No Such ID")
            return
        elif attendees == 0:
            self.response.set_status(402)
            self.response.write("ERROR: No Attendees")
            return
        elif attendees == 2:
            self.response.set_status(403)
            self.response.write("ERROR: Invalid Token")
            return
        else:
            self.response.set_status(200)
            reply_json = json.dumps(attendees)
            self.response.write(reply_json)
            return


def check_user(token):
     _id = 0
     try:
        graph = facebook.GraphAPI(token)
        user = graph.get_object("me")
        _id = user['id']

     except facebook.GraphAPIError as e:
        logging.info("invalid token")
        return False
     return _id

attendees = webapp2.WSGIApplication([
    ('/attendees', APIAttendeesHandler)
], debug=True)