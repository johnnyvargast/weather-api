from django.test import SimpleTestCase

from django.urls import reverse
from rest_framework import status


class WeatherTests(SimpleTestCase):
    weather_detail_url = reverse('weather:details')

    def fetcher(self, data: dict = {}):
        return self.client.get(self.weather_detail_url, data, format='json')

    def test_weather_detail_success_response(self):
        # if the endpoint responds well
        data = {'city': 'cartagena', 'country': 'co'}
        response = self.fetcher(data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_weather_fail_when_invalid_filter(self):
        # if you only accept allowed filters
        data = {'page_size': '9999'}
        response = self.fetcher(data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_weather_fail_when_city_does_not_exist(self):
        # validate when there is no city in the receiving country
        data = {'city': 'cartagena', 'country': 'it'}
        response = self.fetcher(data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_weather_fail_when_city_does_not_receive(self):
        # valid when the city is not received
        data = {'country': 'it'}
        response = self.fetcher(data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual({"cod": "404", "message": "city not found"}, response.data)

    def test_weather_fail_when_no_filters_are_received(self):
        # valid when no filter is received
        response = self.fetcher()
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual({"cod": "400", "message": "Nothing to geocode"}, response.data)
