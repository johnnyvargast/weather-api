import pytz
from django.utils.timezone import datetime as django_datetime

from rest_framework import serializers
from timezonefinder import TimezoneFinder

from apps.weather.utils import get_wind_speed, get_date_string_from_timestamp, get_wind_direction


class WeatherSerializer(serializers.Serializer):
    location_name = serializers.SerializerMethodField()
    temperature = serializers.SerializerMethodField()
    wind = serializers.SerializerMethodField()
    cloudiness = serializers.SerializerMethodField()
    pressure = serializers.SerializerMethodField()
    humidity = serializers.SerializerMethodField()
    sunrise = serializers.SerializerMethodField()
    sunset = serializers.SerializerMethodField()
    geo_coordinates = serializers.SerializerMethodField()
    requested_time = serializers.SerializerMethodField()

    def __init__(self, *args, **kwargs):
        if args:
            coord = args[0].get("coord")
            self.timezone = TimezoneFinder().timezone_at(lng=coord["lon"], lat=coord["lat"])
        super().__init__(*args, **kwargs)

    def get_location_name(self, obj):
        return "{}, {}".format(obj["name"], obj["sys"]["country"])

    def get_temperature(self, obj) -> dict:
        celsius = "{} °C".format(round(obj["main"]["temp"], 1))
        fahrenheit = "{} °F".format(round((obj["main"]["temp"] * (9 / 5)) + 32, 1))
        return {
            "celsius": celsius,
            "fahrenheit": fahrenheit,
        }

    def get_wind(self, obj):
        wind_speed_text = get_wind_speed(speed=obj["wind"]["speed"])
        wind_speed = obj["wind"]["speed"]
        wind_direction = get_wind_direction(value=obj["wind"]["deg"])
        return "{}, {} m/s, {}".format(wind_speed_text, wind_speed, wind_direction)

    def get_cloudiness(self, obj):
        return obj["weather"][0]["description"].capitalize()

    def get_pressure(self, obj):
        return "{} hpa".format(obj["main"]["pressure"])

    def get_humidity(self, obj):
        return "{}%".format(obj["main"]["humidity"])

    def get_sunrise(self, obj):
        ts = int(obj["sys"]["sunrise"])
        return get_date_string_from_timestamp(value=ts, tz=self.timezone)

    def get_sunset(self, obj):
        ts = int(obj["sys"]["sunset"])
        return get_date_string_from_timestamp(value=ts, tz=self.timezone)

    def get_geo_coordinates(self, obj):
        lon = obj["coord"]["lon"]
        lat = obj["coord"]["lat"]
        return "[{}, {}]".format(lat, lon)

    def get_requested_time(self, obj):
        get_date_string_from_timestamp(value=obj["dt"])
        return django_datetime.now(pytz.timezone(self.timezone)).strftime('%Y-%m-%d %H:%M:%S')

    class Meta:
        fields = [
            "location_name",
            "temperature",
            "wind",
            "cloudiness",
            "pressure",
            "humidity",
            "sunrise",
            "sunset",
            "geo_coordinates",
            "requested_time",
        ]
