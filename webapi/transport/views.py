import logging

from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics, status
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response

from .filters import CargoWeightFilter, CarsCapacityFilter
from .models import Location, Car, Cargo
from .serializer import LocationSerializer, CarsListSerializer, CarsCreateSerializer, CarsUpdateSerializer, \
    CargoCreateSerializer, CargoUpdateSerializer, CargoListSerializer, CargoSerializer

logger = logging.getLogger(__name__)


class LocationListAPIView(generics.ListAPIView):
    """ Контроллер списка локаций """

    serializer_class = LocationSerializer
    queryset = Location.objects.all().order_by("zip")


class CarListAPIView(generics.ListAPIView):
    """ Контроллер просмотра машин """

    serializer_class = CarsListSerializer
    queryset = Car.objects.all().order_by("cur_location__zip")
    filter_backends = [DjangoFilterBackend]
    filterset_class = CarsCapacityFilter


class CarCreateAPIView(generics.CreateAPIView):
    """ Создание машины. Локация задается случайным образом. """

    serializer_class = CarsCreateSerializer

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


class CarUpdateAPIView(generics.UpdateAPIView):
    """ Редактирование машины по ID (локация (определяется по введенному zip-коду)) """

    serializer_class = CarsUpdateSerializer

    def get_queryset(self):
        queryset = Car.objects.filter(id=self.kwargs['id'])
        return queryset

    def get_object(self):
        obj = get_object_or_404(Car, id=self.kwargs['id'])
        return obj

    def put(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = CarsUpdateSerializer(instance=instance, data=request.data, context={'request': request})

        if not serializer.is_valid():
            data_err = {'error': serializer.errors, 'status': 'HTTP_400_BAD_REQUEST'}
            return Response(data_err, status=status.HTTP_400_BAD_REQUEST)

        serializer.is_valid(raise_exception=True)
        try:
            serializer.save()
        except Exception as e:
            logger.error(f"Ошибка редактирования машины: {e.args}")
            return Response({"error": "Ошибка редактирования машины"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        return Response(serializer.data, status=status.HTTP_200_OK)


class CargoCreateAPIView(generics.CreateAPIView):
    """ Создание нового груза (характеристики локаций pick-up, delivery определяются по введенному zip-коду) """

    serializer_class = CargoCreateSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data, context={'request': request})

        if not serializer.is_valid():
            data_err = {'error': serializer.errors, 'status': 'HTTP_400_BAD_REQUEST'}
            return Response(data_err, status=status.HTTP_400_BAD_REQUEST)

        serializer.is_valid(raise_exception=True)
        try:
            serializer.save()
        except Exception as e:
            logger.error(f"Ошибка при создании груза: {e.args}")
            return Response({"error": "Ошибка создания груза"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        return Response(serializer.data, status=status.HTTP_201_CREATED)


class CargoUpdateAPIView(generics.UpdateAPIView):
    """ Редактирование груза по ID (вес, описание) """

    serializer_class = CargoUpdateSerializer

    def get_queryset(self):
        queryset = Cargo.objects.filter(id=self.kwargs['id'])
        return queryset

    def get_object(self):
        obj = get_object_or_404(Cargo, id=self.kwargs['id'])
        return obj

    def put(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = CargoUpdateSerializer(instance=instance, data=request.data, context={'request': request})

        if not serializer.is_valid():
            data_err = {'error': serializer.errors, 'status': 'HTTP_400_BAD_REQUEST'}
            return Response(data_err, status=status.HTTP_400_BAD_REQUEST)

        serializer.is_valid(raise_exception=True)
        try:
            serializer.save()
        except Exception as e:
            logger.error(f"Ошибка редактирования груза: {e.args}")
            return Response({"error": "Ошибка редактирования груза"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        return Response(serializer.data, status=status.HTTP_200_OK)


class CargoDestroyAPIView(generics.DestroyAPIView):
    """ Удаление груза по ID. """

    serializer_class = CargoUpdateSerializer

    def get_object(self):
        obj = get_object_or_404(Cargo, id=self.kwargs['id'])
        return obj

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        logger.info(f"Запись о грузе удалена: {instance}")
        return Response(data={'status': 'Запись о грузе удалена.'}, status=status.HTTP_204_NO_CONTENT)


class CargoAPIView(generics.ListAPIView):
    """
    Получение информации о конкретном грузе по ID (локации pick-up, delivery, вес, описание,
    список номеров ВСЕХ машин с расстоянием до выбранного груза);
    """
    serializer_class = CargoSerializer

    def get_queryset(self):
        queryset = Cargo.objects.filter(id=self.kwargs['id'])
        return queryset


class CargoListAPIView(generics.ListAPIView):
    """
    Получение списка грузов (локации pick-up, delivery, количество ближайших машин до груза (=< 450 миль));
    """
    serializer_class = CargoListSerializer
    queryset = Cargo.objects.all()
    filter_backends = [DjangoFilterBackend]
    filterset_class = CargoWeightFilter


