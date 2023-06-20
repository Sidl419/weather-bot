"""Utility functions for weather forecast."""

from typing import Dict, Optional
from pyowm.weatherapi25 import observation
import gettext
import requests
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


def get_fact(degree):
    """Get fact about number."""
    response = requests.get(f"http://numbersapi.com/{degree}/trivia")
    return response


def format_wether_message(weather_attrs: Dict, location: Optional[str] = None) -> str:
    """Get weather message from info dictionary."""
    if location is None:
        location = 'location'

    message = _("The weather in") + " " + str(location) + " " + _("is") + " " + \
        weather_attrs['status'] + \
        '\n' + _("The temperature is ") + \
        str(int((weather_attrs['temp']))) + " " + \
        ngettext("degree", "degrees", abs(int(weather_attrs['temp']))) + \
        '\n' + _("feels like") + " " + \
        str(int(weather_attrs['temp_feels'])) + " " + \
        ngettext("degree", "degrees", abs(int(weather_attrs['temp_feels']))) + \
        '\n' + _("Sun sets at") + " " + weather_attrs['sunset'] + " " +\
        _("and rises at") + " " + weather_attrs['sunrise']
    message += '\n'
    message += '\n'
    message += _('Fact about number') + " " + str(int((weather_attrs['temp']))) + '\n'
    message += '\n'
    message += get_fact(int((weather_attrs['temp']))).text
    return message

def build_menu(buttons,n_cols,header_buttons=None,footer_buttons=None):
    """Get menu with buttons for message interface."""
    menu = [buttons[i:i + n_cols] for i in range(0, len(buttons), n_cols)]
    
    if header_buttons:
        menu.insert(0, header_buttons)
    if footer_buttons:
        menu.append(footer_buttons)
        
    return menu


def get_weather_msg_wrapper(location: str, weather_mgr) -> int:
    """Get current weather in string-format information for the specified location."""
    try:
        observation = weather_mgr.weather_at_place(location)
        weather_attrs = get_weather_status(observation)
        message = format_wether_message(weather_attrs, location)

    except pyowm.commons.exceptions.NotFoundError:
        message = f"Sorry, I couldn't find any weather information for <b>{location}</b>"

    return message

def get_weather_emodzi(msg_lw: str) -> str:
    """Get emodzi for the weather."""
    if msg_lw.find('clouds') != -1:
        return "\U0001f325"
    elif msg_lw.find('sun') != -1:
        return "\U0001f304"
    elif msg_lw.find('rain') != -1:
        return "\U0001f327"
    elif msg_lw.find('snow') != -1:
        return "\U0001f328"
    else:
        return "\U0001f914"