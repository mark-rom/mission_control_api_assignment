from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from . import serializers, services
from .models import Coordinates, Station
from .permissions import StaffOrReadOnly


class StationViewSet(ModelViewSet):

    queryset = Station.objects.all()
    serializer_class = serializers.StationSerializer
    permission_classes = [StaffOrReadOnly]

    def perform_create(self, serializer):
        instance = serializer.save()
        Coordinates.objects.create(station=instance)

    @action(
        methods=['get', 'post'], detail=True,
        serializer_class=serializers.DirectiveSerializer,
    )
    def state(self, request, pk):

        coordinates = get_object_or_404(Coordinates, station_id=pk)

        if request.method == 'GET':
            serializer = serializers.CoordinatesSerializer(coordinates)
            return Response(data=serializer.data, status=status.HTTP_200_OK)

        serializer = services.create_directive(self, request, pk)
        axis, distance = services.get_axis_and_distance(serializer)

        station = coordinates.station

        serializer = services.update_coordinates(coordinates, axis, distance)

        services.check_coords_and_break_station_if_needed(
            serializer.data[axis], station
        )

        return Response(data=serializer.data, status=status.HTTP_201_CREATED)
