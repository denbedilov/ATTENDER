__author__ = 'itamar'
from api import facebook
import logging
from DAL import DAL

class fb_logic:

    def validate_fb_login(id,access_token):
        try:
            graph = facebook.GraphAPI(access_token)
            user = graph.get_object("me")
            _id = user['id']
            if id == _id:
                mydb = DAL()
                mydb.set_user_details(id,user['first_name'],user['last_name'])
                return True

        except facebook.GraphAPIError as e:
            logging.info("invalid token")

        return 1

    def check_token(token , eventid):
         try:
            graph = facebook.GraphAPI(token)
            user = graph.get_object("me")
            _id = user['id']
            mydb = DAL()
            mydb.set_attendings(u_key=_id,e_key=eventid)

         except facebook.GraphAPIError as e:
            logging.info("invalid token")
            return False

         return True

    def test_id(id):
        try:
            _id_ = int(id)
        except ValueError:
            return False
        return True

    def check_user(self, token):
        _id = 0
        try:
            graph = facebook.GraphAPI(token)
            user = graph.get_object("me")
            _id = user['id']

        except facebook.GraphAPIError as e:
            logging.info("invalid token")
            return False
        return _id