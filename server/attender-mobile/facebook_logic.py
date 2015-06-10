__author__ = 'itamar'
from api import facebook
import logging

class fb_logic():
    @staticmethod
    def validate_fb_login(_id, access_token):
        try:
            graph = facebook.GraphAPI(access_token)
            user = graph.get_object("me")
            _id_ = user['id']
            if _id == _id_:
                return user
        except facebook.GraphAPIError as e:
            logging.info("invalid token")

        return False

    @staticmethod
    def check_token(token):
        try:
            graph = facebook.GraphAPI(token)
        except facebook.GraphAPIError as e:
            logging.info("invalid token")
            return False

        return True

    def get_id(self,token):
        graph = facebook.GraphAPI(token)
        user = graph.get_object("me")
        return user['id']

    @staticmethod
    def test_id(_id):
        flag = False
        try:
            _id_ = int(_id)
            flag = True
        except ValueError:
            flag = False

        return flag

    @staticmethod
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

    @staticmethod
    def get_fb_friends(access_token):
        try:
            graph = facebook.GraphAPI(access_token)
            friends = graph.get_connections("me", "friends")
            logging.info(friends)
            friend_list = [friend['id'] for friend in friends['data']]
            logging.info(friend_list)
            return friend_list

        except facebook.GraphAPIError as e:
            logging.info("invalid token")
            return None
