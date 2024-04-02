from django_filters import rest_framework as filters

from .models import Car, Cargo


class CargoWeightFilter(filters.FilterSet):
    """ Фильтр груза по весу """

    weight_gte = filters.NumberFilter(field_name='weight', lookup_expr='gte')
    weight_lte = filters.NumberFilter(field_name='weight', lookup_expr='lte')

    class Meta:
        model = Cargo
        fields = []


class CarsCapacityFilter(filters.FilterSet):
    """ Фильтр машин по грузоподъёмности """

    capacity_gte = filters.NumberFilter(field_name='capacity', lookup_expr='gte')
    capacity_lte = filters.NumberFilter(field_name='capacity', lookup_expr='lte')

    class Meta:
        model = Car
        fields = []


class CapacityCarsFilter:
    """
    По грузоподъемности машин.
    Применен в CargoListSerializer метод get_characteristics_cars
    """
    def __init__(self, data: list, cap_gte=None, cap_lte=None):
        self.cap_gte = None
        self.cap_lte = None
        if cap_gte is not None:
            self.cap_gte = int(cap_gte) if cap_gte.isdigit() else None
        if cap_lte is not None:
            self.cap_lte = int(cap_lte) if cap_lte.isdigit() else None
        self.data = data

    @staticmethod
    def more_than_or_equal(_gte, data):
        """ Больше или равно """
        if _gte is None:
            return data

        data_ = []
        for var in data:
            if var['capacity'] >= _gte:
                data_.append(var)
        data.clear()
        return data_

    @staticmethod
    def less_than_or_equal(_lte, data):
        """ Меньше или равно """
        if _lte is None:
            return data

        data_ = []
        for var in data:
            if var['capacity'] <= _lte:
                data_.append(var)
        data.clear()
        return data_

    def get_filter_capacity_cars(self):
        data = CapacityCarsFilter.more_than_or_equal(self.cap_gte, self.data)
        data_ = CapacityCarsFilter.less_than_or_equal(self.cap_lte, data)
        return data_


class DistanceCarsFilter:
    """
    По дистанции машины до груза.
    Применен в CargoListSerializer метод get_characteristics_cars
    """
    def __init__(self, data: list, dist_gte=None, dist_lte=None):
        self.dist_gte = None
        self.dist_lte = None
        if dist_gte is not None:
            self.dist_gte = int(dist_gte) if dist_gte.isdigit() else None
        if dist_lte is not None:
            self.dist_lte = int(dist_lte) if dist_lte.isdigit() else None
        self.data = data

    @staticmethod
    def more_than_or_equal(_gte, data):
        """ Больше или равно """
        if _gte is None:
            return data

        data_ = []
        for var in data:
            if var['distance_miles'] >= _gte:
                data_.append(var)
        data.clear()
        return data_

    @staticmethod
    def less_than_or_equal(_lte, data):
        """ Меньше или равно """
        if _lte is None:
            return data

        data_ = []
        for var in data:
            if var['distance_miles'] <= _lte:
                data_.append(var)
        data.clear()
        return data_

    def get_filter_distance_cars(self):
        data = DistanceCarsFilter.more_than_or_equal(self.dist_gte, self.data)
        data_ = DistanceCarsFilter.less_than_or_equal(self.dist_lte, data)
        return data_
