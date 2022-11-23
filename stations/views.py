from django.shortcuts import get_object_or_404
from drf_spectacular.utils import (extend_schema, extend_schema_view,
                                   inline_serializer)
from rest_framework import serializers, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from . import services
from .models import Coordinates, Station
from .permissions import StaffOrReadOnly
from .serializers import (CoordinatesSerializer, DirectiveSerializer,
                          StationSerializer)


# Расширить количество ответов на post, put, delete
# ошибками 400, 401, 403, 404 (при неообходимости)
@extend_schema_view(
    list=extend_schema(
        summary='Список космических станций',
        description='''Возвращает список всех космических станций.
        Сервис доступен всем пользователям.''',
        auth=[],
        tags=['Stations']
    ),
    retrieve=extend_schema(
        summary='Космическая станция',
        description='''Возвращает указанную космическую станцию.
        Сервис доступен всем пользователям.''',
        auth=[],
        tags=['Stations']
    ),
    create=extend_schema(
        summary='Создание космической станции',
        description='''Создает и возвращает космическую станцию.
        Сервис доступен только пользователям с правами администратора
        (is_staff, is_superuser).
        ''',
        tags=['Stations']
    ),
    update=extend_schema(
        summary='Изменение космической станции',
        description='''Изменяет космическую станцию.
        Сервис доступен только пользователям с правами администратора
        (is_staff, is_superuser).
        ''',
        tags=['Stations']
    ),
    partial_update=extend_schema(exclude=True),
    destroy=extend_schema(
        summary='Удаление космической станции',
        description=''''Удаляет космическую станцию.
        Сервис доступен только пользователям с правами администратора
        (is_staff, is_superuser).
        ''',
        tags=['Stations']
    )
)
class StationViewSet(ModelViewSet):
    """Вьюсет предоставляющий базовые CRUD методы работы со станциями.
    Расширен action методами для получения координат станции."""
    queryset = Station.objects.all()
    serializer_class = StationSerializer
    permission_classes = [StaffOrReadOnly]

    def perform_create(self, serializer):
        instance = serializer.save()
        Coordinates.objects.create(station=instance)

    @extend_schema(
        summary='Получение координат космической станции',
        auth=[], tags=['States']
    )
    @action(
        methods=['get'], detail=True,
        serializer_class=CoordinatesSerializer, url_path='state',
        url_name='state_retrieve'
    )
    def state_get(self, request, pk):
        """Возвращает текущие координаты космической станции."""
        coordinates = get_object_or_404(Coordinates, station_id=pk)

        serializer = self.get_serializer(coordinates)
        return Response(data=serializer.data, status=status.HTTP_200_OK)

    @extend_schema(
        summary='Смещение космической станции',
        responses={
            200: CoordinatesSerializer,
            # 400: inline_serializer(name='Error400', fields={'field_name': serializers.CharField(many=True)}),
            # 404: inline_serializer(name='Error404', fields={'detail': serializers.CharField()})
        },
        tags=['States'],
    )
    @action(
        methods=['post'], detail=True,
        serializer_class=DirectiveSerializer, url_path='state',
        url_name='state_post'
    )
    def state_post(self, request, pk):
        """Получает ось и значение, на которое сместится станция.
        Если станция выходит за пределы положительных координат, "ломает" ее.
        """
        coordinates = get_object_or_404(Coordinates, station_id=pk)

        serializer = services.create_directive(self, request, pk)
        axis, distance = services.get_axis_and_distance(serializer)

        station = coordinates.station

        serializer = services.update_coordinates(coordinates, axis, distance)

        services.check_coords_and_break_station_if_needed(
            serializer.data[axis], station
        )

        return Response(data=serializer.data, status=status.HTTP_201_CREATED)
