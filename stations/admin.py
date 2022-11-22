from django.contrib import admin

from . import models, services


@admin.register(models.Station)
class StationAdmin(admin.ModelAdmin):
    list_display = ('name', 'state', 'created_at', 'break_date')
    fields = ('name',)
    model = models.Station

    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)
        models.Coordinates.objects.create(station=obj)


@admin.register(models.Coordinates)
class CoordinatesAdmin(admin.ModelAdmin):
    list_display = ('station_name', 'x', 'y', 'z')
    exclude = ('station_name', 'x', 'y', 'z')
    model = models.Coordinates

    @admin.display(empty_value='unknown', description='Станция')
    def station_name(self, obj):
        return obj.station.name


@admin.register(models.Directive)
class DirectiveAdmin(admin.ModelAdmin):
    list_display = ('user', 'axis', 'distance', 'station')
    fields = ('axis', 'distance', 'station')
    model = models.Directive

    def save_model(self, request, obj, form, change):

        obj.user = request.user
        super().save_model(request, obj, form, change)

        station = obj.station
        coords = station.coordinates
        serializer = services.update_coordinates(
            coords, obj.axis, obj.distance
        )

        services.check_coords_and_break_station_if_needed(
            serializer.data[obj.axis], station
        )
