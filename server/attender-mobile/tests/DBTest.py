__author__ = 'olesya'

import unittest
from models.User import User
from DAL import DAL


class UserDetails(unittest.TestCase):
    def test_get_name(self):
        d = DAL()
        self.assertEqual(d.get_user_details("user_name"),"oles_ka")

    def test_set_name(self):
        d = DAL()
        us_list = d.set_user_details("itamar", "sn@dd.com", "123")
        self.assertEqual(us_list.pop().user_name ,"itamar")


def main():
    unittest.main()

if __name__ == "__main__":
    main()