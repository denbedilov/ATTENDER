__author__ = 'olesya'


import unittest
from DAL import DAL
from search_events_interface import SearchEventsUsingAPI
from models.user import User
from google.appengine.ext import ndb
from google.appengine.ext import testbed


class UserDetails(unittest.TestCase):
    def setUp(self):
        self.testbed = testbed.Testbed()
        self.testbed.activate()
        self.testbed.init_datastore_v3_stub(User)
        self.testbed.init_memcache_stub()
        ndb.get_context().clear_cache()
        self.mydb = DAL()
        self.obj = SearchEventsUsingAPI()

    def test_check_login_that_already_fb_logged_in(self):
        self.mydb.set_user_details(12, "Itamar", "Sharify", "sometest@gmail.com")
        token = self.mydb.register("sometest@gmail.com", "12134", "Itamar", "Sharify")
        qry = User.query(User.email == "sometest@gmail.com")
        print "token", token
        for q in qry:
            print q.first_name , q.last_name, q.email
        self.assertTrue(qry.count() == 1)

    def test_register_new_user(self):
        token = self.mydb.register("sometest@gmail.com", "12134", "Itamar", "Sharify")
        qry = User.query(User.email == "sometest@gmail.com")
        print "token", token
        for q in qry:
            print q.first_name , q.last_name, q.email
        self.assertTrue(qry.count() == 1)

    def test_error_is_1_on_wrong_password(self):
        self.mydb.register("sometest@gmail.com", "12134", "Itamar", "Sharify")
        res = self.mydb.user_login("sometest@gmail.com", "12134")
        self.assertEqual(res, 1)

    def test_error_is_false_on_not_existing_email(self):
        self.mydb.register("sometest@gmail.com", "12134", "Itamar", "Sharify")
        res = self.mydb.user_login("another@gmail.com", "1213")
        self.assertFalse(res)

    def test_error_is_2_on_none_password(self):
        self.mydb.set_user_details(12, "Itamar", "Sharify", "sometest@gmail.com")
        qry = User.query(User.email == "sometest@gmail.com")
        res = self.mydb.user_login("sometest@gmail.com", "1213")
        self.assertEqual(res, 2)

    def test_check_token_exist(self):
        self.mydb.set_user_details(12, "Itamar", "Sharify", "sometest@gmail.com")
        self.assertTrue(self.mydb.check_token(1))

    def test_check_token_not_exist(self):
        self.mydb.set_user_details(12, "Itamar", "Sharify", "sometest@gmail.com")
        self.assertFalse(self.mydb.check_token(2))