from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


class Station(models.Model):

    STATE_CHOICES = [
        ('brk', 'broken'),
        ('run', 'running')
    ]

    name = models.CharField(
        verbose_name='Название станции', max_length=100,
        unique=True
    )
    state = models.CharField(
        verbose_name='Текущее состояние', max_length=3, default='run',
        choices=STATE_CHOICES, editable=False
    )
    created_at = models.DateTimeField(
        verbose_name='Дата запуска', auto_now_add=True, editable=False
    )
    break_date = models.DateTimeField(
        verbose_name='Дата поломки', editable=False, blank=True, null=True
    )

    class Meta:
        verbose_name = 'Станция'
        verbose_name_plural = 'Станции'

    def __str__(self) -> str:
        return f'Станция {self.name}, статус {self.get_state_display()}'


class Directive(models.Model):
    AXIS_CHOICES = [
        ('x', 'x'),
        ('y', 'y'),
        ('z', 'z')
    ]

    user = models.ForeignKey(
        User, on_delete=models.DO_NOTHING, related_name='directives',
        verbose_name='Автор указания'
    )
    axis = models.CharField(
        verbose_name='Ось', max_length=1, choices=AXIS_CHOICES
    )
    distance = models.SmallIntegerField(
        verbose_name='Расстояние',
    )
    station = models.ForeignKey(
        Station, on_delete=models.DO_NOTHING, related_name='directives'
    )
    created_at = models.DateTimeField(
        verbose_name='Дата запуска', auto_now_add=True, editable=False
    )

    class Meta:
        verbose_name = 'Указание'
        verbose_name_plural = 'Указания'

    def __str__(self) -> str:
        return f'Указание для {self.station}: {self.axis} на {self.distance}'


class Coordinates(models.Model):
    station = models.OneToOneField(
        Station, on_delete=models.DO_NOTHING, verbose_name='Станция',
    )
    x = models.SmallIntegerField(
        verbose_name='Координата по x', default=100
    )
    y = models.SmallIntegerField(
        verbose_name='Координата по y', default=100
    )
    z = models.SmallIntegerField(
        verbose_name='Координата по z', default=100
    )

    class Meta:
        verbose_name = 'Координаты'
        verbose_name_plural = 'Координаты'

    def __str__(self) -> str:
        return f'Координаты станции {self.station}'
