from rest_framework import generics

from .models import Location
from .serializer import LocationSerializer


class LocationListAPIView(generics.ListAPIView):
    """ Контроллер списка локаций """

    serializer_class = LocationSerializer
    queryset = Location.objects.all().order_by("zip")


