"""Utility functions for weather forecast."""

from typing import Dict, Optional
from pyowm.weatherapi25 import observation
import gettext
translation = gettext.translation("weth", 'po', fallback=True)
_ = translation.gettext


def get_weather_status(observation: observation.Observation) -> Dict:
    """Get weather info from OWM observation object."""
    weather = observation.weather
    res = dict()

    res['temp'] = weather.temperature('celsius').get('temp', None)  # get temperature in Celsius
    res['temp_feels'] = weather.temperature('celsius').get('feels_like', None)
    res['status'] = weather.detailed_status   # get weather status
    res['sunrise'] = weather.sunrise_time(timeformat='date').strftime("%I:%M%p")
    res['sunset'] = weather.sunset_time(timeformat='date').strftime("%I:%M%p")

    return res


def format_wether_message(weather_attrs: Dict, location: Optional[str] = None) -> str:
    """Get weather message from info dictionary."""
    if location is None:
        location = 'location'
    message = _("The weather in") + " " + str(location) + " " + _("is") + " " + \
              weather_attrs['status'].decode('ascii') + \
              '\n' + _("The temperature is ") + " " + \
              "{:.1f}".format(weather_attrs['temp'].decode('ascii')) + _("degrees") + \
              '\n' + _("feels like") + " " + \
              "{:.1f}".format(weather_attrs['temp_feels'].decode('ascii')) + _("degrees") + \
              '\n' + _("Sun sets at") + " " + weather_attrs['sunset'].decode('ascii') + " " +\
              _("and rises at") + weather_attrs['sunrise'].decode('ascii')
    return message
