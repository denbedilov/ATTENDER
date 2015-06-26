__author__ = 'olesya'

sources = ["meetup", "eventbrite"]

meetup_settings ={'URL_PATTERN': "https://api.meetup.com/find/open_events?",
                  'URL_PATTERN_CITIES': "http://api.meetup.com/2/cities",
                  'API_KEY': "185c2b3e44c4b4644365a3022d5a2f"}

meetup_categories = {"Career": 2,  # Career & Business"
                     "Community": 4,  #Community & Environment
                     "Entertainment": 11,  #Games
                     "Fitness": 9,
                     "Health": 14,  #Health & Wellbeing"
                     "New Age": 22,  #New Age & Spirituality
                     "Politics": 13,  #Movement & Politics
                     "Socializing": 31,
                     "Tech": 34,
                     "Transport": 3}  # Cars & Motorcycles

meetup_cities = ['Tel Aviv-Yafo', 'Jerusalem', 'Herzeliyya', 'Haifa', "Ra'anana", 'Rekhovot', 'Kefar Sava',
                 'Ramat Gan', 'Netanya', "Modi'in"]



eventbrite_settings = {"URL_PATTERN": "https://www.eventbriteapi.com/v3/events/search/?",
                       "API_KEY": "W46EUEAIC77N3ZDAJN",
                       "token": "Q7QZWAQ7LFTNH62IWHCG" }

eventbrite_categories = {"Career": 101,
                         "Community": 113,
                         "Entertainment": 104,  # Film, Media & Entertainment
                         "Fitness": 108,
                         "Health": 107,
                         "New Age": 114,  #Spirituality
                         "Politics": 112,  #Government & Politics
                         "Socializing": 109,
                         "Tech": 102,
                         "Transport": 118}  # Auto, Boat & Air

eventbrite_cities = {'Tel Aviv-Yafo': 'Tel+Aviv-Yafo', 'Jerusalem': 'Jerusalem', 'Herzeliyya': 'Herzliya', 'Haifa': 'Haifa' ,
          "Ra'anana": "Ra'anana", 'Rekhovot': 'Rehovot', 'Kefar Sava': 'Kfar+Saba', 'Ramat Gan': 'Ramat+Gan',
          'Netanya': 'Netanya', "Modi'in": "Modiin+Ilit"}