from src.utils import format_wether_message

def test_format_for_wether():
    weather_attrs = {}
    weather_attrs['temp'] = "32"
    weather_attrs['temp_feels'] = "35"
    weather_attrs['status'] = "sun"
    weather_attrs['sunrise'] = "5:00"
    weather_attrs['sunset'] = "20:00"
    assert type(format_wether_message(weather_attrs)) == str