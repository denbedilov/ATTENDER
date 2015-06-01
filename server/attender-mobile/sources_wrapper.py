__author__ = 'olesya'

from api_request import ApiRequest
from meetup_api import MeetupApi
from eventbrite_api import EventbriteApi


class SearchEventsUsingAPI():
    def request_events(self, city=None, category=None, date_and_time=None, city_num=10, radius="1"):
        apirequst_object = ApiRequest()
        all_events = ""
        for source in apirequst_object.get_sources():
            events = {
                'meetup': self.meetup_response(city, category, date_and_time, city_num, radius),
                'eventbrite': self.eventbrite_response(city, category, date_and_time, city_num, radius)
            }[source]
            all_events += events

        return all_events

    def meetup_response(self, city=None, category=None, date_and_time=None, city_num=10, radius="1"):
        meetup_object = MeetupApi()
        return meetup_object.request_events(city, category, date_and_time, city_num, radius)

    def eventbrite_response(self, city=None, category=None, date_and_time=None, city_num=10, radius="1"):
        eventbrite_object = EventbriteApi()
        return eventbrite_object.request_events(city, category, date_and_time)


