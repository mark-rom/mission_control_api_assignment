from rest_framework import permissions


class StaffOrReadOnly(permissions.IsAuthenticatedOrReadOnly):
    """Разрешает доступ к списку и объекту только для чтения.
    Небезопасные запросы доступны только пользователям
    с ролью staff и суперюзерам.
    """
    def has_permission(self, request, view):
        user = request.user
        return (
            user.is_staff or super().has_permission(request, view)
        )
