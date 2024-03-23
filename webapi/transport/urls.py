from django.urls import path

from .views import LocationListAPIView


urlpatterns = [
    path("v1/locations/", LocationListAPIView.as_view(), name="locations"),
]

