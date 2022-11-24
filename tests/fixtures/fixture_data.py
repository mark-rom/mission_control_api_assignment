import pytest


@pytest.fixture
def station_1():
    from stations.models import Coordinates, Station
    station = Station.objects.create(name='Станция 1')
    Coordinates.objects.create(station=station)
    return station


@pytest.fixture
def station_2():
    from stations.models import Coordinates, Station
    station = Station.objects.create(name='Станция 2')
    Coordinates.objects.create(station=station)
    return station


@pytest.fixture
def station_3():
    from stations.models import Coordinates, Station
    station = Station.objects.create(name='Станция 3')
    Coordinates.objects.create(station=station)
    return station
