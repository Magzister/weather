### About
The idea is to create weather console app to show weather outside the window.

### App structure
Application should get a global ip of the computer, then using this ip get a coordinates and only then get a weather data in this area. Format the information for the console output.

#### Get IP module
IPService - abstract class.
Ifconfig - Fetch ip adress from ifconfig.me. Inherits IPService class.
##### Data types
IP - type alias for str.

#### Get coordinates module
LocationService - abstract class.
Ipapi - Fetch location information from ipapi.co. Inherits LocationService class.
##### Data types
Coordinates - NamedTuple with latitude and longitude values.
Location - dataclass with name of country and city, contains coordinates.

#### Get weather information
WeatherService - abstract class.
VisualCrossing - Fetch weather information form [this](https://www.visualcrossing.com/resources/documentation/weather-api/timeline-weather-api/) api. Inherits WeatherService class.
##### Data types
Weather - dataclass with information about weather description, temperature, sunrise and sunset.

#### Parse weather information
[formatter.py](https://github.com/Magzister/weather/blob/master/app/formatter.py#L5) file contains format_weather function that must be used for formatting weather and location information.