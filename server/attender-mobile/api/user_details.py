__author__ = 'olesya'

import webapp2
from DAL import DAL


class UserDetailsHandler(webapp2.RequestHandler):
    def get(self):
        mydb = DAL()
        token = self.request.get("token")
        if token is "":
            self.post(-1)
        else:
            try:
                json_response = mydb.get_user_by_token(int(token))
                self.post(json_response)
            except ValueError:
                self.post(2)

    def post(self, response):
        if response == -1:
            self.response.set_status(400)
            self.response.write("ERROR: Missing token")
        elif response == 1:
            self.response.set_status(401)
            self.response.write("ERROR: No such user")
        elif response == 2:
            self.response.set_status(402)
            self.response.write("ERROR: Invalid token. Should be integer!")
        else:
            self.response.set_status(200)
            self.response.write(response)


user = webapp2.WSGIApplication([
    ('/userdetails', UserDetailsHandler)
], debug=True)