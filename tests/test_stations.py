import pytest

from stations.models import Station


pytestmark = pytest.mark.django_db


class TestStationsEndpoints:

    endpoint = '/api/v1/stations/'

    def test_list(self, client, station_1, station_2):

        response = client.get(
            self.endpoint
        )

        assert response.status_code == 200, (
            f'Проверьте, что при GET запросе на {self.endpoint} возвращается статус 200'
        )
        assert len(response.json()) == 2, (
            f'Проверьте, что при GET запросе на {self.endpoint} возвращается список станций'
        )

    @pytest.mark.parametrize('field, expected', [
        ('name', 'Eagle'),
        ('state', 'running'),
        ('break_date', None)
    ])
    def test_create(self, user_client, field, expected):
        data = {'name': 'Eagle'}

        response = user_client.post(
            self.endpoint,
            data=data
        )

        assert response.status_code == 201, (
            f'Проверьте, что при POST запросе на {self.endpoint} возвращается статус 201'
        )
        assert response.json()[field] == expected, (
            f'Проверьте, что ответ {self.endpoint} на POST запрос соответствует ожидаемому'
        )

    def test_retrieve(self, client, station_1):
        data = {
            'id': station_1.id,
            'name': station_1.name,
            'state': station_1.get_state_display(),
            'created_at': station_1.created_at.strftime('%Y-%m-%dT%H:%M:%S.%fZ'),
            'break_date': station_1.break_date
        }

        url = f'{self.endpoint}{station_1.id}/'

        response = client.get(url)

        assert response.status_code == 200, (
            f'Проверьте, что при GET запросе на {url}, возвращается статус 200'
        )
        assert response.json() == data, (
            f'Проверьте, что при GET запросе на {url} возвращается указанная станция'
        )

    def test_update(self, user_client, station_1):
        data = {'name': 'Eagle'}
        url = f'{self.endpoint}{station_1.id}/'

        response = user_client.put(url, data=data)

        assert response.status_code == 200, (
            f'Проверьте, что при PUT запросе на {url}, возвращается статус 200'
        )
        assert response.json()['name'] == 'Eagle', (
            f'Проверьте, что ответ {url} на PUT запрос соответствует ожидаемому'
        )
        assert response.json()['created_at'] == station_1.created_at.strftime('%Y-%m-%dT%H:%M:%S.%fZ'), (
            f'Проверьте, что ответ {url} на PUT запрос соответствует ожидаемому'
        )

    def test_delete(self, user_client, station_1):
        station_id = station_1.id
        station_count = Station.objects.count()
        url = f'{self.endpoint}{station_id}/'

        response = user_client.delete(url)

        assert response.status_code == 204, (
            f'Проверьте, что при DELETE запросе на {url}, возвращается статус 204'
        )
        assert Station.objects.count() == station_count - 1, (
            f'Проверьте, что при DELETE запросе на {url} объект удаляется'
        )
