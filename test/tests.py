import os
import datetime
import sys

testdir = os.path.dirname(__file__)
srcdir = '../src'
sys.path.insert(0, os.path.abspath(os.path.join(testdir, srcdir)))
from utils import format_wether_message, get_weather_status


def make_weather_attrs():
    weather_attrs = {}
    weather_attrs['temp'] = "32"
    weather_attrs['temp_feels'] = "35"
    weather_attrs['status'] = "sun"
    weather_attrs['sunrise'] = "5:00"
    weather_attrs['sunset'] = "20:00"
    return weather_attrs


def test_format_for_weather():
    weather_attrs = make_weather_attrs()
    assert type(format_wether_message(weather_attrs)) == str


def test_format_none_location():
    weather_attrs = make_weather_attrs()
    assert 'location' in format_wether_message(weather_attrs)


def test_format_non_none_location():
    weather_attrs = make_weather_attrs()
    assert 'Moscow' in format_wether_message(weather_attrs, 'Moscow')


class A:
    weather = {}
    def __init__(self, weath):
        self.weather = weath

class W:
    def __init__(self, temp, detailed_status, sunrise, sunset):
        self.temp = temp
        self.detailed_status = detailed_status
        self.sunrise = sunrise
        self.sunset = sunset

    def temperature(self, s):
        return self.temp

    def sunrise_time(self, timeformat):
        return datetime.datetime.strptime(self.sunrise, "%I:%M%p")

    def sunset_time(self, timeformat):
        return datetime.datetime.strptime(self.sunset, "%I:%M%p")


def test_get_weather():
    temp = {'temp': "32", 'temp_feels' : "35"}
    weather_attrs = W(temp, "sun", "10:36AM", "10:36PM")
    obs = A(weather_attrs)
    assert type(get_weather_status(obs)) == dict


def test_dict_labels():
    temp = {'temp': "32", 'temp_feels': "35"}
    weather_attrs = W(temp, "sun", "10:36AM", "10:36PM")
    obs = A(weather_attrs)
    res = get_weather_status(obs)
    assert 'temp' in res
    assert 'temp_feels' in res
    assert 'status' in res
    assert 'sunrise' in res
    assert 'sunset' in res
