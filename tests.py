from src.utils import format_wether_message, get_weather_status
from pyowm.owm import OWM
from pyowm.utils.config import get_default_config
import os


def make_weather_attrs():
    weather_attrs = {}
    weather_attrs['temp'] = "32"
    weather_attrs['temp_feels'] = "35"
    weather_attrs['status'] = "sun"
    weather_attrs['sunrise'] = "5:00"
    weather_attrs['sunset'] = "20:00"
    return weather_attrs


def test_format_for_weather():
    weather_attrs = {}
    weather_attrs['temp'] = "32"
    weather_attrs['temp_feels'] = "35"
    weather_attrs['status'] = "sun"
    weather_attrs['sunrise'] = "5:00"
    weather_attrs['sunset'] = "20:00"
    assert type(format_wether_message(weather_attrs)) == str


def test_format_none_location():
    weather_attrs = {}
    weather_attrs['temp'] = "32"
    weather_attrs['temp_feels'] = "35"
    weather_attrs['status'] = "sun"
    weather_attrs['sunrise'] = "5:00"
    weather_attrs['sunset'] = "20:00"
    assert 'location' in format_wether_message(weather_attrs)


def test_format_non_none_location():
    weather_attrs = {}
    weather_attrs['temp'] = "32"
    weather_attrs['temp_feels'] = "35"
    weather_attrs['status'] = "sun"
    weather_attrs['sunrise'] = "5:00"
    weather_attrs['sunset'] = "20:00"
    assert 'Moscow' in format_wether_message(weather_attrs, 'Moscow')


class A:
    weather = {}
    def __init__(self, weath):
        self.weather = weath


def test_get_weather():
    """
    config_dict = get_default_config()
    config_dict['language'] = 'fr'  # your language here, eg. French
    owm = OWM(os.environ['OWM_API_KEY'], config_dict)
    mgr = owm.weather_manager()
    observation = mgr.weather_at_place('Paris, FR')
    """
    weather_attrs = {}
    """
    temp = {'temp': "32", 'temp_feels' : "35"}
    weather_attrs['temperature'] = temp
    weather_attrs['detailed_status'] = "sun"
    weather_attrs['sunrise'] = "5:00"
    weather_attrs['sunset'] = "20:00"
    """
    obs = A(weather_attrs)
    assert type(get_weather_status(obs)) == dict