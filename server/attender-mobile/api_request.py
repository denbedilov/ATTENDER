# coding=utf-8
__author__ = 'olesya'

from google.appengine.api import urlfetch
import defenitions
from lib import requests
import logging
from DAL import DAL
from models.Event import Event
from datetime import datetime, timedelta


class ApiRequest():

    def get_sources(self):
        return defenitions.sources

    def get_settings(self, source):
        return {
        'meetup': defenitions.meetup_settings,
        'eventbrite': defenitions.eventbrite_settings
        }[source]

    def get_category(self, category, source):
        result = {
            'meetup': defenitions.meetup_categories.get(category),
            'eventbrite': defenitions.eventbrite_categories.get(category),
        }[source]
        if result is None:
            logging.info("There is no such category {}".format(category))
            return 401
        else:
            return result

    def get_category_by_id(self, c_id, source):
        result = {
            'meetup': [key for key, value in defenitions.meetup_categories.items() if value == int(c_id)],
            'eventbrite': [key for key, value in defenitions.eventbrite_categories.items() if value == int(c_id)],
        }[source]
        if result is None:
            logging.info("There is no such category {}".format(c_id))
            return 401
        else:
            return result

    def possible_cities(self, source):
        return {
           'meetup': defenitions.meetup_cities,
           'eventbrite': defenitions.eventbrite_cities
        }[source]

    def http_request_using_urlfetch(self, http_url, params):
        url = self.prepare_get_url(http_url, params)
        result = urlfetch.fetch(url=url,
                                deadline=30,
                                headers={"Authorization": "Bearer " + params['token']})
        return result.content, result.status_code

    def prepare_get_url(self, url, params):
        new_url = url
        for key, value in params.iteritems():
            new_url = new_url + key + '=' + str(value)
            if key != params.keys()[-1]:
                new_url += "&"
        return new_url

    def http_request_using_requests_lib(self, http_url, params):
        request = requests.get(http_url, params=params)
        logging.info("after requests http {}".format(request))
        data = request.json()
        return data, request.status_code

    def check_city(self, city):
        if city in ["Jerusalem", "jerusalem", u'ירושלים', 'Jerusalem, Old City']:
            return "Jerusalem"
        elif city in ["Tel Aviv-Yafo", "Tel-Aviv", "Tel Aviv", u'תל אביב', u'תל-אביב', u'תל-אביב יפו', u'תל אביב-יפו']:
            return "Tel Aviv-Yafo"
        elif city in ['Herzeliyya', 'Herzeliya', 'Herzliya', 'Herzelia', 'Hertzliya Pituach', 'Herzeliyah Pituach', 'Herzeliyya Pituach', 'Herzliya Pituach', u'הרצליה', u'הרצליה פיתוח']:
            return "Herzeliyya"
        elif city in ["Haifa", u'חיפה']:
            return "Haifa"
        elif city in ["Ra'anana", "Raanana", "raanana", u'רעננה']:
            return "Ra'anana"
        elif city in ["Rekhovot", "rehovot", u'רחובות']:
            return "Rekhovot"
        elif city in ["Kefar Sava", u'כפר סבא', u'כפר-סבא']:
            return "Kefar Sava"
        elif city in ["Ramat Gan", "RAMAT GAN", u'רמת גן', u'רמת-גן']:
            return "Ramat Gan"
        elif city in ["Netanya", u'נתניה']:
            return "Netanya"
        elif city in ["Modi'in", u'מודיעין', u'מודעין']:
            return "Modi'in"
        elif city is None:
            return "Unknown"


    def save_in_db(self, event, source, category=None):
        mydb = DAL()
        sec = event['date'] / 1000
        e = Event()
        date = datetime.fromtimestamp(sec)
        if category is not None:
            e.update_category(event['id'], category)

        mydb.set_event_details(event['id'], event['name'], date, event['city'], event['address'],
                               event['description'], event['host'], event['event_url'], event['attendees'], event['price'],
                               category, source)


    #Surround with try and catch for each requested field in case the information is not available
    def check_valid(self, event, res, key, params, params2=None, params3=None):
        try:
            if params2 is None and params3 is None:
                event[key] = res[params]
            elif params3 is None:
                event[key] = res[params][params2]
            else:
                event[key] = res[params][params2][params3]
                return event
        except:
            event[key] = "Unknown"