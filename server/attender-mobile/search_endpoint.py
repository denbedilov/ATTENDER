"""Hello World API implemented using Google Cloud Endpoints.

Defined here are the ProtoRPC messages needed to define Schemas for methods
as well as those methods defined in an API.
"""

import json
import webapp2
from protorpc import messages
from protorpc import message_types
from protorpc import remote
# from EventSearch import SearchHandler





class APIHandler(webapp2.RequestHandler):
	def get(self,city, time, ):
		self.post()

	def post(self):
		replyJson = {}

		user = User.checkUser()
		if not user:
			self.response.set_status(401)
			self.response.write('Need active user to proceed')
			return

		guess = self.request.get('word')
		if not guess:
			self.response.set_status(400)
			self.response.write('Can not process an empty guess')
			return

		word = Word.todaysWord()
		score = WordScore.getScore(user, word)
		score.incAttempts()

		if guess == word.word:
			replyJson['solved'] = True
			replyJson['attempts'] = score.attempts
			score.setSolved()
		else:
			replyJson['solved'] = False
			replyJson['attempts'] = score.attempts

		if score.attempts >= config.ATTEMPTS_FOR_CLUE or replyJson['solved']:
			replyJson['wordLen'] = word.len


		self.response.write(json.dumps(replyJson))

app = webapp2.WSGIApplication([
	('/api/guess', GuessHandler)
], debug=True)
"""
package = 'APISearch'


class Greeting(messages.Message):
  """Greeting that stores a message."""
  message = messages.StringField(1)


class GreetingCollection(messages.Message):
  """Collection of Greetings."""
  items = messages.MessageField(Greeting, 1, repeated=True)


STORED_GREETINGS = GreetingCollection(items=[
    Greeting(message='hello world!'),
    Greeting(message='goodbye world!'),
])


@endpoints.api(name='search', version='v1')
class MeetupSearch(remote.Service, webapp2.RequestHandler):
    """Helloworld API v1."""
    def get(self):
        self.response.write("Test One Two")
    # res = SearchHandler()
    @endpoints.method(message_types.VoidMessage, GreetingCollection,
                      path='hellogreeting', http_method='GET',
                      name='greetings.listGreeting')
    def greetings_list(self, unused_request):
        p =self.res.get_events()
        time.sleep(1)
        self.response.write(p)
        return self.res.get_events()
        # return STORED_GREETINGS
    ID_RESOURCE = endpoints.ResourceContainer(
        message_types.VoidMessage,
        id=messages.IntegerField(1, variant=messages.Variant.INT32))

    @endpoints.method(ID_RESOURCE, Greeting,
                      path='hellogreeting/{id}', http_method='GET',
                      name='greetings.getGreeting')
    def greeting_get(self, city = None,time = None,category = None):
        return self.res.get_events(city,time,category)

#
# api = webapp2.WSGIApplication([
#     ('/api', SearchHandler)
# ], debug=True)
APPLICATION = endpoints.api_server([MeetupSearch])


"""