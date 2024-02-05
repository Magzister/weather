import os

APP_NAME = "weather"
APP_DESCRIPTION = "displays weather forecast by location"

# ip service
IFCONFIG_URL = "https://ifconfig.me/ip/"

# location service
IPAPI_URL = "https://ipapi.co/{ip}/{response_format}/"
IPAPI_FORMAT = "json"

# reverse geocoding service
GEOAPIFY_API_KEY = os.environ.get("GEOAPIFY_API_KEY", "")
GEOAPIFY_URL = ("https://api.geoapify.com/"
                "v1/geocode/reverse?"
                "lat={latitude}&lon={longitude}&"
                "apiKey=" + GEOAPIFY_API_KEY)

# weather service
VISUALCROSSING_API_KEY = os.environ.get("VISUALCROSSING_API_KEY", "")
VISUALCROSSING_URL = ("https://weather.visualcrossing.com/"
                      "VisualCrossingWebServices/rest/services/timeline/"
                      "{latitude},{longitude}/{date}?"
                      "key=" + VISUALCROSSING_API_KEY + "&"
                      "include=current")
DATE_FORMAT = "%Y-%m-%d"

#sst
SEA_TEMPERATURE_URL = "https://www.seatemperature.org/countries.htm"

# db connection
DB_PATH = "sqlite+pysqlite:///database.db"
