__author__ = 'olesya'

from google.appengine.ext import ndb


class Attendings(ndb.Model):
    user_id = ndb.IntegerProperty()
    event_id = ndb.IntegerProperty()

    def check_attend_exist(self,u_id, e_id):
        q = Attendings.query(Attendings.user_id == u_id, Attendings.event_id == e_id).get()
        if q:
            return q
        else:
            return False