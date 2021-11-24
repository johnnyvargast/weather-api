import logging

from django.conf import settings
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from drf_spectacular.utils import extend_schema
from rest_framework import status
from rest_framework.exceptions import ValidationError
from rest_framework.views import APIView
from rest_framework.response import Response
import requests as req

from apps.weather.serializers import WeatherSerializer
from apps.weather.utils import weather_detail_parameters

logger = logging.getLogger(__name__)


class WeatherDetail(APIView):
    """ Endpoint to obtain the climatic data of a city """

    # url by default, from where the data will be obtained
    url = "http://api.openweathermap.org/data/2.5/weather"

    # filters allowed by the endpoint
    filters = [
        'city',
        'country',
    ]

    @method_decorator(cache_page(60 * 2))
    @extend_schema(responses={status.HTTP_200_OK: WeatherSerializer()}, parameters=weather_detail_parameters())
    def get(self, request, *args, **kwargs):
        # Validate that they only receive set filters
        if list(set(request.GET.keys()) - set(self.filters)):
            msg = "There are invalid filters. The allowed filters are: {}".format(", ".join(self.filters))
            raise ValidationError({"cod": "404", "message": msg})

        # default filters
        filters = {"appid": settings.WEATHER_API_KEY, "units": "metric"}

        # receive city and country filters to merge them into one
        city_country = [str(request.GET[item]).lower() for item in ["city", "country"] if request.GET.get(item, None)]
        if city_country:
            city_country = ",".join(city_country) if city_country else None
            filters["q"] = city_country

        try:
            # make the request to obtain the data
            response = req.get(self.url, params=filters)
            response_data = response.json()

            # if the request was not successful
            if response.status_code != status.HTTP_200_OK:
                return Response(response_data, status=status.HTTP_400_BAD_REQUEST)

            return Response(WeatherSerializer(response_data).data)
        except Exception as ex:
            logger.error('There was an error trying to get the weather data: {}'.format(ex))
            msg = "There was an error trying to get the data, please contact a developer."
            raise ValidationError({"cod": "404", "message": msg})
