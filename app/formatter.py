from app.types import Location
from app.types import Weather
from app.types import Celsius


def format_weather(location: Location,
                   weather: Weather,
                   sst: Celsius | None) -> str:
    '''Return string with formatted weather and location info.'''
    sunrise = weather.sunrise.strftime("%H:%M")
    sunset = weather.sunset.strftime("%H:%M")
    result = (f"{location.country}, {location.city}\n"
                f"temperature: {weather.temperature:.1f}°C\n"
                f"feels like: {weather.feelslike:.1f}°C\n"
                f"{weather.description}\n"
                f"Sunrise: {sunrise}\n"
                f"Sunset: {sunset}\n")
    if sst: result += f"Sea temperature: {sst:.1f}°C\n"
    return result
