from src.utils import format_wether_message, get_weather_status
from pyowm.owm import OWM
from pyowm.utils.config import get_default_config



def test_format_for_weather():
    weather_attrs = {}
    weather_attrs['temp'] = "32"
    weather_attrs['temp_feels'] = "35"
    weather_attrs['status'] = "sun"
    weather_attrs['sunrise'] = "5:00"
    weather_attrs['sunset'] = "20:00"
    assert type(format_wether_message(weather_attrs)) == str
def test_get_weather():
    config_dict = get_default_config()
    config_dict['language'] = 'fr'  # your language here, eg. French
    owm = OWM('your-api-key', config_dict)
    mgr = owm.weather_manager()
    observation = mgr.weather_at_place('Paris, FR')
    assert type(get_weather_status(observation)) == dict