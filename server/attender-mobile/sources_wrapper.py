__author__ = 'olesya'

from api_request import ApiRequest
from meetup_api import MeetupApi
from eventbrite_api import EventbriteApi

class SearchEventsUsingAPI():
    def request_events(self, city=None, category=None, date_and_time=None, city_num=10, radius="1"):
        apirequst_object = ApiRequest()
        all_events = ""
        events = ""
        for source in apirequst_object.get_sources():
            if source == 'meetup':
                events = self.meetup_response(city, category, date_and_time, city_num, radius)
            elif source == 'eventbrite':
                events = self.eventbrite_response(city, category, date_and_time)

            all_events += events
        return all_events

    def meetup_response(self, city=None, category=None, date_and_time=None, city_num=10, radius="1"):
        meetup_object = MeetupApi()
        return meetup_object.request_events(city, category, date_and_time, city_num, radius)

    def eventbrite_response(self, city=None, category=None, date_and_time=None):
        eventbrite_object = EventbriteApi()
        return eventbrite_object.request_events(city, category, date_and_time)


