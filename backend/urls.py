from django.urls import path, include

urlpatterns = [
    path('', include('apps.weather.urls', namespace='weather')),
]
