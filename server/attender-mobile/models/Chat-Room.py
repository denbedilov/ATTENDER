__author__ = 'olesya'

from google.appengine.ext import ndb
from Chat import Chat
from User import User


class ChatRoom(ndb.Model):
    user_id = ndb.KeyProperty(kind=User.user_id)
    chat_id = ndb.KeyProperty(kind=Chat.chat_id)




