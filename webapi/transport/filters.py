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
    """ Фильтр машин по грузоподъёмности. Применен в CarListAPIVie. """

    capacity_gte = filters.NumberFilter(field_name='capacity', lookup_expr='gte')
    capacity_lte = filters.NumberFilter(field_name='capacity', lookup_expr='lte')

    class Meta:
        model = Car
        fields = []


class BaseCarsMethodFilter:
    @staticmethod
    def more_than_or_equal(_gte, data, field: str):
        """ Больше или равно """
        if _gte is None:
            return data

        data_ = []
        for var in data:
            if var[field] >= _gte:
                data_.append(var)
        data.clear()
        return data_

    @staticmethod
    def less_than_or_equal(_lte, data, field: str):
        """ Меньше или равно """
        if _lte is None:
            return data

        data_ = []
        for var in data:
            if var[field] <= _lte:
                data_.append(var)
        data.clear()
        return data_


class CapacityCarsFilter:
    """
    По грузоподъемности машин.
    Применен в CargoListSerializer метод get_characteristics_cars
    """
    def __init__(self, data: list, request: (dict, None), field: str):
        self.request = request or {}
        self.field = field if isinstance(field, str) else str(field)
        self.cap_gte = request['cap_gte'] if 'cap_gte' in request else None
        self.cap_lte = request['cap_lte'] if 'cap_lte' in request else None
        if self.cap_gte is not None:
            self.cap_gte = int(self.cap_gte) if self.cap_gte.isdigit() else None
        if self.cap_lte is not None:
            self.cap_lte = int(self.cap_lte) if self.cap_lte.isdigit() else None
        self.data = data

    def get_filter_capacity_cars(self):
        data = BaseCarsMethodFilter.more_than_or_equal(self.cap_gte, self.data, self.field)
        data_ = BaseCarsMethodFilter.less_than_or_equal(self.cap_lte, data, self.field)
        return data_


class DistanceCarsFilter:
    """
    По дистанции машины до груза.
    Применен в CargoListSerializer метод get_characteristics_cars
    """
    def __init__(self, data: list, request: (dict, None), field: str):
        self.request = request or {}
        self.field = field if isinstance(field, str) else str(field)
        self.dist_gte = request['dist_gte'] if 'dist_gte' in request else None
        self.dist_lte = request['dist_lte'] if 'dist_lte' in request else None
        if self.dist_gte is not None:
            self.dist_gte = int(self.dist_gte) if self.dist_gte.isdigit() else None
        if self.dist_lte is not None:
            self.dist_lte = int(self.dist_lte) if self.dist_lte.isdigit() else None
        self.data = data

    def get_filter_distance_cars(self):
        data = BaseCarsMethodFilter.more_than_or_equal(self.dist_gte, self.data, self.field)
        data_ = BaseCarsMethodFilter.less_than_or_equal(self.dist_lte, data, self.field)
        return data_

