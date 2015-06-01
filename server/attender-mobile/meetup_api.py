__author__ = 'olesya'
import api_request
import logging
import json

class MeetupApi(api_request.ApiRequest):

    def __init__(self):
        self.source = "meetup"
        self.settings = self.get_settings(self.source)

    def request_events(self, city=None, category=None, date_and_time=None, city_num=10, radius="1"):
        events_list = []
        per_page = 200
        offset = 0
        cities = []
        request = {}

        if category is not None:
            catg = self.get_category(category.strip(), self.source)  #find in dictionary
            if catg != 401:
                request.update({"category": catg})
            else:
                return 401

        if date_and_time is not None:
            date_and_time = ',' + date_and_time
            request.update({"time": date_and_time})

        if city is not None:
            if city in self.possible_cities(self.source):
                logging.info("city exist")
                cities.append(city)
            else:
                logging.info("The city is not exist")
        else:
            cities = self.request_city(city_num)

        logging.info("Starting connection to meetup.api")
        for city in cities:  #for each city requst info from meetup
            request.update({"sign": "true", "country": "il", "key": self.settings['API_KEY'],
                            "page": per_page, "offset": offset, "fields": "event_hosts", "city": city,
                            "text_format": "plain", "radius": radius})

            response, status_code = self.http_request_using_requests_lib("http://api.meetup.com/2/open_events", request)
            offset += 1
            logging.info("Actual meetup respond {}".format(response))
            if status_code == 200:
                for res in response['results']:
                    event = {}

                    self.check_valid(event, res, 'id', 'id')
                    self.check_valid(event, res, 'name', 'name')
                    self.check_valid(event, res, 'date', 'time')
                    self.check_valid(event, res, 'city', 'venue', 'city')
                    c = self.check_city(event['city'])
                    if c is not None:
                        event['city'] = c
                    self.check_valid(event, res, 'address', 'venue', 'address_1')
                    self.check_valid(event, res, 'description', 'description')
                    self.check_valid(event, res, 'event_url', 'event_url')

                    try:
                        for host in res['event_hosts']:  #Owner
                            event['host'] = host['member_name']
                    except:
                        event['host'] = 'Unknown'
                    try:
                        event['attendees'] = res['yes_rsvp_count']  #Attendees
                    except:
                        event['attendees'] = 'Unknown'
                    try:
                        event['price'] = res['fee']['amount'] + res['fee']['currency']
                    except:
                        event['price'] = "free"

                    events_list.append(event)
                    self.save_in_db(event, self.source, category)

        event_json = json.dumps(events_list)
        return event_json

    def request_city(self, city_num):
        cities = []
        request = {"sign": "true", "country": "il", "key": self.settings['API_KEY'],
                   "page": city_num, "offset": 0}
        response, status_code = self.http_request_using_requests_lib(self.settings['URL_PATTERN_CITIES'], request)
        if status_code == 200:
            for res in response["results"]:
                cities.append(res["city"])
            return cities
        else:
            logging.info("ERROR occurred in cities request, status code: {}".format(status_code))

