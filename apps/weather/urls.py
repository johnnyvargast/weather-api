from django.urls import path

from . import views

app_name = 'weather'

urlpatterns = [
    path('weather/', views.WeatherDetail.as_view(), name='details'),
]
