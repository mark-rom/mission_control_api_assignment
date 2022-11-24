### Уделенное время:
Времени потрачено: 28 часов 11 минут.
Тестовое задание выполнялось 20-24 ноября.

### Покрытие тестами
Согласно отчету coverage тестами покрыто 99% приложения
Тесты запускались командой `coverage run --source=stations -m pytest`

### Swagger
Swagger генерируется автоматически и доступен по адресу `/api/schema/swagger-ui/#/`. Также доступен redoc

### Об API
Поскольку это сервис по управлению космическими станциями, то делать небезопасные запросы может только юзер с правами if_staff или is_superuser. Для тестирования юзер может быть создан командой `python3 manage.py createsuperuser`. В дальнейшем можно подключить, например Djoser, для работы с пользователями.

Модель указания расширена по сравнению с данной. Добавлены дата указания и станция, получающая указание.

При запуске без Docker выполнить следующую команду:

`python3 manage.py migrate`
`python3 manage.py createsuperuser`

При запуске с Docker выполнить следующие команды:

`docker exec -it infra_web_1 python3 manage.py migrate`

`docker exec -it infra_web_1 python3 manage.py createsuperuser`