from django.contrib import admin
from .models import Location, Car, Cargo


class LocationAdmin(admin.ModelAdmin):
    list_display = ["id", "zip", "lat", "long", "state", "city"]


class CarAdmin(admin.ModelAdmin):
    list_display = ["id", "number", "cur_location", "capacity"]


class CargoAdmin(admin.ModelAdmin):
    list_display = ["id", "loc_pick_up", "loc_delivery", "weight", "description"]


admin.site.register(Location, LocationAdmin)
admin.site.register(Car, CarAdmin)
admin.site.register(Cargo, CargoAdmin)
