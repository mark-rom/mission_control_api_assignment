import pytest

from stations.models import Directive, Station

pytestmark = pytest.mark.django_db


class TestStateEndpoints:

    endpoint = '/api/v1/stations/'

    @pytest.mark.parametrize('field', [('x'), ('y'), ('z')])
    def test_retrive_coordinates(self, client, station_1, field):

        url = f'{self.endpoint}{station_1.id}/state/'
        response = client.get(url)

        assert response.status_code == 200, (
            f'Проверьте, что при GET запросе на {url}, возвращается статус 200'
        )

        test_data = response.json()
        assert test_data[field] == 100, (
            f'Проверьте, что значение поля "{field}" по умолчанию равно 100'
        )

    def test_change_coordinates(self, user_client, station_2):
        url = f'{self.endpoint}{station_2.id}/state/'
        directives = Directive.objects.count()
        data = {
            'axis': 'x',
            'distance': 5
        }

        response = user_client.post(url, data=data)

        assert response.status_code == 201, (
            f'Проверьте, что при POST запросе на {url}, возвращается статус 201'
        )
        assert Directive.objects.count() == directives + 1, (
            f'Проверьте, что POST запрос на {url} создает Указание в бд'
        )
        assert response.json() == {'x': 105, 'y': 100, 'z': 100}, (
            f'Проверьте, что {url} возвращает измененные координаты станции'
        )

    def test_change_coordinate_to_zero(self, user_client, station_1):
        url = f'{self.endpoint}{station_1.id}/state/'
        directives = Directive.objects.count()
        data = {
            'axis': 'y',
            'distance': -100
        }

        response = user_client.post(url, data=data)
        station_1 = Station.objects.get(pk=station_1.id)

        assert response.status_code == 201, (
            f'Проверьте, что при POST запросе на {url} с правильными данными, возвращается статус 201'
        )
        assert Directive.objects.count() == directives + 1, (
            f'Проверьте, что POST запрос на {url} создает Указание в бд'
        )
        assert response.json() == {'x': 100, 'y': 0, 'z': 100}, (
            f'Проверьте, что {url} возвращает измененные координаты станции'
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
            'distance': 105
        }
        assert station_1.get_state_display() == 'broken', (
            'Проверьте, что после возвращения станции на положительные координаты'
            'параметр "state" не изменился (статус "broken")'
        )

        response = user_client.post(url, data=data)

        break_date = station_1.break_date
        data = {
            'axis': 'x',
            'distance': -100
        }

        response = user_client.post(url, data=data)

        assert station_1.break_date == break_date, (
            'Проверьте, что после снижения второй координаты ниже 1'
            'дата поломки не изменилась'
        )

    def test_change_coordinate_below_zero(self, user_client, station_1):
        url = f'{self.endpoint}{station_1.id}/state/'
        directives = Directive.objects.count()
        data = {
            'axis': 'y',
            'distance': -130
        }

        response = user_client.post(url, data=data)
        station_1 = Station.objects.get(pk=station_1.id)

        assert response.status_code == 201, (
            f'Проверьте, что при POST запросе на {url} с правильными данными, возвращается статус 201'
        )
        assert Directive.objects.count() == directives + 1, (
            f'Проверьте, что POST запрос на {url} создает Указание в бд'
        )
        assert response.json() == {'x': 100, 'y': -30, 'z': 100}, (
            f'Проверьте, что {url} возвращает измененные координаты станции'
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
            'distance': 135
        }
        assert station_1.get_state_display() == 'broken', (
            'Проверьте, что после возвращения станции на положительные координаты'
            'параметр "state" не изменился (статус "broken")'
        )

        response = user_client.post(url, data=data)

        break_date = station_1.break_date
        data = {
            'axis': 'x',
            'distance': -100
        }

        response = user_client.post(url, data=data)

        assert station_1.break_date == break_date, (
            'Проверьте, что после снижения второй координаты ниже 1'
            'дата поломки не изменилась'
        )