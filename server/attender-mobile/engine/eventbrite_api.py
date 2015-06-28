__author__ = 'olesya'

import api_request
import logging
import json
import datetime
import time

class EventbriteApi(api_request.ApiRequest):
    def __init__(self):
        self.source = "eventbrite"
        self.settings = self.get_settings(self.source)

    def request_events(self, city=None, category=None, date_and_time=None):
        events_list = []
        request = {'token': self.settings['token'], "venue.country": "IL", "expand": "venue"}

        if category is not None:
            catg = self.get_category(category.strip(), self.source)  #find in dictionary
            if catg != 401:
                request.update({"categories": catg})
            else:
                return 401
        if date_and_time is not None:
            d_t = {
                "1d": "tomorrow",
                "1w": "this_week",
                "1m": "this_month"
            }[date_and_time]
            request.update({"start_date.keyword": d_t})
        if city is not None:
            try:
                city = self.possible_cities(self.source)[city]
                logging.info("city exist")
                request.update({"venue.city": city})
            except:
                logging.info("The city is not exist")

        logging.info("Starting connection to eventbrite.api")
        response, status_code = self.http_request_using_urlfetch(self.settings['URL_PATTERN'], request)
        logging.info("eventbrite actual response {}".format(response))
        response = json.loads(response)

        if status_code == 200:
            for res in response['events']:
                event = {}
                self.check_valid(event, res, 'name', 'name', 'text')
                self.check_valid(event, res, 'description', 'description', 'text')
                self.check_valid(event, res, 'id', 'id')
                self.check_valid(event, res, 'date', 'start', 'local') #Get start date and time
                date_object = datetime.datetime.strptime(event['date'], '%Y-%m-%dT%H:%M:%S') # Convert to datetime object
                milisec = time.mktime(date_object.timetuple())*1000 #Convert to milliseconds
                event['date'] = int(milisec) #Save the new date and time in milliseconds
                try:
                    c_id = res['category']['id']
                    category = self.get_category_by_id(c_id, self.source).pop()
                except:
                    pass

                self.check_valid(event, res, 'city', 'venue', 'address', 'city')
                c = self.check_city(event['city'])
                if c is not None:
                    event['city'] = c

                self.check_valid(event, res, 'address', 'venue', 'address', 'address_1')
                self.check_valid(event, res, 'event_url', 'url')
                self.check_valid(event, res, 'host', 'organizer', 'name')
                event['attendees'] = 0
                try:
                    if all(r['free'] for r in res['ticket_classes']):
                        event['price'] = "free"
                    else:
                        event['price'] = event['event_url']
                except KeyError:
                    event['price'] = event['event_url']
                events_list.append(event)
                self.save_in_db(event, self.source, category)

        event_json = json.dumps(events_list)
        return event_json
