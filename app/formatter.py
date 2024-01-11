from app.location_service import Location
from app.weather_service import Weather


def format_weather(location: Location, weather: Weather) -> str:
    sunrise = weather.sunrise.strftime("%H:%M")
    sunset = weather.sunset.strftime("%H:%M")
    return (f"{location.country}, {location.city}\n"
            f"temperature: {weather.temperature:.1f}°C\n"
            f"feels like: {weather.feelslike}°C\n"
            f"{weather.description}\n"
            f"Sunrise: {sunrise}\n"
            f"Sunset: {sunset}\n")
