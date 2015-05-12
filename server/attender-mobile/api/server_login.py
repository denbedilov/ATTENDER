__author__ = 'itamar'


import json
import logging
import webapp2
#TODO add the right import
class APILoginHandler(webapp2.RequestHandler):

    def get(self):
        received = False
        #TODO create a user db object
        id = self.request.get("id").encode('ascii', 'ignore')
        firstname = self.request.get("firstname").encode('ascii', 'ignore')
        firstname= firstname.strip()
        lastname = self.request.get("lastname").encode('ascii', 'ignore')
        logging.info("is:"+ id+"\nfirstname: "+firstname+"\nlastname: "+lastname)
        if [id,firstname,lastname] is not "":
            received = True
        #TODO send to the Db
        self.post(received)

    def post(self, received):
        if received is False:
            self.response.set_status(400)
            self.response.write("ERROR: Missing parameters")
            return
        else:
            self.response.set_status(200)
            self.response.write("OK")
            return



login = webapp2.WSGIApplication([
    ('/login', APILoginHandler)
], debug=True)