from datetime import datetime
from typing import Tuple

from rest_framework.request import Request
from rest_framework.serializers import ModelSerializer
from rest_framework.viewsets import ModelViewSet

from .models import Coordinates, Station
from .serializers import CoordinatesSerializer, DirectiveSerializer


def get_axis_and_distance(serializer: ModelSerializer) -> Tuple[str, int]:
    axis = serializer.data['axis']
    distance = serializer.data['distance']
    return axis, distance


def create_directive(view: ModelViewSet, request: Request, station_id: int):

    serializer = DirectiveSerializer(
        data=request.data,
        context={
            'request': view.request,
            'format': view.format_kwarg,
            'view': view
        }
    )
    serializer.is_valid(raise_exception=True)
    serializer.save(user=request.user, station_id=station_id)

    return serializer


def update_coordinates(instance: Coordinates, axis: str, distance: int):

    attr = instance.__getattribute__(axis)
    serializer = CoordinatesSerializer(
        instance=instance, data={axis: attr+distance}
    )
    serializer.is_valid(raise_exception=True)
    serializer.save()

    return serializer


def break_the_station(station: Station):

    station.break_date = datetime.now()
    station.state = 'b'
    station.save()


def check_coords_and_break_station_if_needed(
    coord_distance: int, station: Station
):

    if coord_distance < 1 and not station.break_date:
        break_the_station(station)
