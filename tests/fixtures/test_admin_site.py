import pytest

from stations.models import Directive, Station


class TestAdminSiteEndpoints:

    endpoint = '/admin/stations/directive/add/'

    def test_admin_site_change_coordinates(self, admin_client, station_2):
        directives = Directive.objects.count()
        data = {
            'axis': 'x',
            'distance': 5,
            'station': station_2.id,
            "_save": "Save"
        }

        response = admin_client.post(self.endpoint, data=data)
        station_1 = Station.objects.get(pk=station_2.id)

        assert response.status_code == 302, (
            f'Проверьте, что при POST запросе на {self.endpoint} срабатывает перенаправление'
        )
        assert station_1.coordinates.x == 105, (
            f'Проверьте, что {self.endpoint} возвращает измененные координаты станции'
        )
        assert station_1.break_date is None, (
            'Проверьте, что параметр "break_date" станции  возвращает null/None'
        )
        assert Directive.objects.count() == directives + 1, (
            f'Проверьте, что POST запрос на {self.endpoint} создает Указание в бд'
        )

    def test_admin_site_change_coordinate_to_zero(self, admin_client, station_1):
        directives = Directive.objects.count()
        data = {
            'axis': 'y',
            'distance': -100,
            'station': station_1.id,
            "_save": "Save"
        }

        response = admin_client.post(self.endpoint, data=data)
        station_1 = Station.objects.get(pk=station_1.id)

        assert response.status_code == 302, (
            f'Проверьте, что при POST запросе на {self.endpoint} срабатывает перенаправление'
        )
        assert Directive.objects.count() == directives + 1, (
            f'Проверьте, что POST запрос на {self.endpoint} создает Указание в бд'
        )
        assert station_1.coordinates.y == 0, (
            f'Проверьте, что {self.endpoint} возвращает измененные координаты станции'
        )
        assert station_1.break_date is not None, (
            'Проверьте, что после снижения одной из координат ниже 1'
            'параметр "break_date" станции не возвращает null/None'
        )
        assert station_1.get_state_display() == 'broken', (
            'Проверьте, что после снижения одной из координат ниже 1'
            'параметр "state" станции  возвращает "broken"'
        )

        data = {
            'axis': 'y',
            'distance': 100,
            'station': station_1.id,
            "_save": "Save"
        }

        response = admin_client.post(self.endpoint, data=data)

        assert station_1.get_state_display() == 'broken', (
            'Проверьте, что после возвращения станции на положительные координаты'
            'параметр "state" не изменился (статус "broken")'
        )

        break_date = station_1.break_date
        data = {
            'axis': 'x',
            'distance': -100,
            'station': station_1.id,
            "_save": "Save"
        }

        response = admin_client.post(self.endpoint, data=data)

        assert station_1.break_date == break_date, (
            'Проверьте, что после снижения второй координаты ниже 1'
            'дата поломки не изменилась'
        )

    def test_admin_site_change_coordinate_below_zero(self, admin_client, station_1):
        directives = Directive.objects.count()
        data = {
            'axis': 'y',
            'distance': -130,
            'station': station_1.id,
            "_save": "Save"
        }

        response = admin_client.post(self.endpoint, data=data)
        station_1 = Station.objects.get(pk=station_1.id)

        assert response.status_code == 302, (
            f'Проверьте, что при POST запросе на {self.endpoint} срабатывает перенаправление'
        )
        assert Directive.objects.count() == directives + 1, (
            f'Проверьте, что POST запрос на {self.endpoint} создает Указание в бд'
        )
        assert station_1.coordinates.y == -30, (
            f'Проверьте, что {self.endpoint} возвращает измененные координаты станции'
        )
        assert station_1.break_date is not None, (
            'Проверьте, что после снижения одной из координат ниже 1'
            'параметр "break_date" станции не возвращает null/None'
        )
        assert station_1.get_state_display() == 'broken', (
            'Проверьте, что после снижения одной из координат ниже 1'
            'параметр "state" станции  возвращает "broken"'
        )

        data = {
            'axis': 'y',
            'distance': 140,
            'station': station_1.id,
            "_save": "Save"
        }

        response = admin_client.post(self.endpoint, data=data)

        assert station_1.get_state_display() == 'broken', (
            'Проверьте, что после возвращения станции на положительные координаты'
            'параметр "state" не изменился (статус "broken")'
        )

        break_date = station_1.break_date
        data = {
            'axis': 'x',
            'distance': -100,
            'station': station_1.id,
            "_save": "Save"
        }

        response = admin_client.post(self.endpoint, data=data)

        assert station_1.break_date == break_date, (
            'Проверьте, что после снижения второй координаты ниже 1'
            'дата поломки не изменилась'
        )
