import locale
import requests
import json
import datetime
from phrases import Phrases


class Knowledge(object):
    def __init__(self, weather_api_token=None):
        self.weather_api_token = weather_api_token

    def find_weather(self):
        loc_obj = self.get_location()

        lat = loc_obj['lat']
        lon = loc_obj['lon']

        weather_req_url = "http://api.openweathermap.org/data/2.5/find?lat={0}&lon={1}&units=metric&appid={2}".format(
            lat, lon, self.weather_api_token)
        r = requests.get(weather_req_url)
        weather_json = json.loads(r.text)

        temperature = int(weather_json['list'][0]['main']['temp'])

        return {'temperature': temperature}

    def get_location(self):
        # get location
        location_req_url = "http://freegeoip.net/json/%s" % self.get_ip()
        r = requests.get(location_req_url)
        location_obj = json.loads(r.text)

        lat = location_obj['latitude']
        lon = location_obj['longitude']

        return {'lat': lat, 'lon': lon}

    def get_ip(self):
        ip_url = "http://jsonip.com/"
        req = requests.get(ip_url)
        ip_json = json.loads(req.text)
        return ip_json['ip']

    # datetime functions
    def get_time(self):
        return datetime.datetime.now().strftime('%I:%M')

    def get_weekday(self):
        locale.setlocale(locale.LC_ALL, 'el_GR.UTF-8')
        return datetime.datetime.today().strftime('%A')

    def get_date(self):
        locale.setlocale(locale.LC_ALL, 'el_GR.UTF-8')
        return datetime.datetime.today().strftime('%A, %x')

    @staticmethod
    def learn_default_responses(file, phrases):
        Phrases.add_phrases(file, phrases)
