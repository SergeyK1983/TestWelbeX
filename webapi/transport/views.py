import logging
from django.db import IntegrityError
from rest_framework import generics, status
from rest_framework.exceptions import APIException
from rest_framework.response import Response

from .models import Location, Car
from .serializer import LocationSerializer, CarsListSerializer, CarsEditSerializer

logger = logging.getLogger(__name__)


class LocationListAPIView(generics.ListAPIView):
    """ Контроллер списка локаций """

    serializer_class = LocationSerializer
    queryset = Location.objects.all().order_by("zip")


class CarListAPIView(generics.ListAPIView):
    """ Контроллер просмотра машин """

    serializer_class = CarsListSerializer
    queryset = Car.objects.all().order_by("cur_location__zip")


class CarCreateAPIView(generics.CreateAPIView):
    """ Создание машины. Локация задается случайным образом. """

    serializer_class = CarsEditSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)

        if not serializer.is_valid():
            data_err = {'error': serializer.errors, 'status': 'HTTP_400_BAD_REQUEST'}
            return Response(data_err, status=status.HTTP_400_BAD_REQUEST)

        serializer.is_valid(raise_exception=True)
        try:
            serializer.save()
        except Exception as e:
            logger.error(f"Ошибка при создании машины: {e.args}")
            return Response({"error": "Ошибка создания машины"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        return Response(serializer.data, status=status.HTTP_201_CREATED)
