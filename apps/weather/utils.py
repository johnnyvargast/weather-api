import json
from datetime import datetime

import pytz


def get_wind_speed(speed: float):
    """
    Get text describing the wind speed.

    :param speed: (float) Speed
    :return: (str) Label
    """
    file = open("local_storage/wind-speed-new-data.json")
    data = json.load(file)
    data = data["en"]

    for item in data:
        speed_interval = data[item]["speed_interval"]
        start = speed_interval[0]
        end = speed_interval[1]
        if speed >= start and speed <= end:
            return item
    return ''


def get_wind_direction(value: int):
    """
    Get wind direction in text

    :param value: (int) Value
    :return: (str) Direction of the wind
    """
    file = open("local_storage/wind-direction.json")
    data = json.load(file)
    data = data["en"]

    for item in sorted(data, key=lambda i: i['wind'], reverse=True):
        if value >= item["wind"]:
            return item["label"]
    return ""


def get_date_string_from_timestamp(value: int, date_format: str = '%H:%M:%S', tz: str = None):
    """
    Convert from timestamp to date to string and with a date format.

    :param value: (int) Value to convert
    :param date_format: (str) Format to the date
    :param tz: (str) Timezone
    :return: (datetime)
    """
    date = datetime.utcfromtimestamp(value)
    date = date.replace(tzinfo=pytz.UTC)
    if tz:
        date = date.astimezone(tz=pytz.timezone(tz))

    date = date.strftime(date_format)
    return date
