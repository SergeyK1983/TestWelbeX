from django.urls import path

from .views import LocationListAPIView, CarCreateAPIView, CarListAPIView, CarUpdateAPIView, CargoCreateAPIView, \
    CargoUpdateAPIView, CargoDestroyAPIView, CargoAPIView, CargoListAPIView

urlpatterns = [
    path("v1/locations/", LocationListAPIView.as_view(), name="locations"),
    path("v1/cars/", CarListAPIView.as_view(), name="cars"),
    path("v1/create-car/", CarCreateAPIView.as_view(), name="create-car"),
    path("v1/update-car/<int:id>/", CarUpdateAPIView.as_view(), name="update-car"),
    path("v1/create-cargo/", CargoCreateAPIView.as_view(), name="create-cargo"),
    path("v1/update-cargo/<int:id>/", CargoUpdateAPIView.as_view(), name="update-cargo"),
    path("v1/destroy-cargo/<int:id>/", CargoDestroyAPIView.as_view(), name="destroy-cargo"),
    path("v1/cargo/<int:id>/", CargoAPIView.as_view(), name="cargo"),
    path("v1/list-cargo/", CargoListAPIView.as_view(), name="list-cargo"),
]

