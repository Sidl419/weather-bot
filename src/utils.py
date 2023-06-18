"""Utility functions for weather forecast."""

from typing import Dict, Optional
from pyowm.weatherapi25 import observation
import gettext
translation = gettext.translation("weth", 'po', fallback=True)
_, ngettext = translation.gettext, translation.ngettext


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

    message = f"""
        The weather in {location} is <b>{weather_attrs['status']}</b>

        The temperature is <b>{weather_attrs['temp']:.1f}°C</b>, feels like <b>{weather_attrs['temp_feels']:.1f}°C</b>

        Sun sets at <b>{weather_attrs['sunset']}</b> and rises at <b>{weather_attrs['sunrise']}</b>
        """
    message = _("The weather in") + " " + str(location) + " " + _("is") + " " + \
              f"<b>{weather_attrs['status']}</b>" + \
              '\n' + _("The temperature is ") + " " + \
              f"<b>{weather_attrs['temp']:.1f}</b>" + \
              ngettext("degree", "degrees", abs(int(weather_attrs['temp'].decode('ascii')))) + \
              '\n' + _("feels like") + " " + \
              f"<b>{weather_attrs['temp_feels']:.1f}</b>" + \
              ngettext("degree", "degrees", abs(int(weather_attrs['temp_feels'].decode('ascii')))) + \
              '\n' + _("Sun sets at") + " " + f"<b>{weather_attrs['sunset']}</b>" + " " +\
              _("and rises at") + f"<b>{weather_attrs['sunrise']}</b>"
    return message
