# Generated by Django 4.1.3 on 2022-11-22 12:51

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Station',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, unique=True, verbose_name='Название станции')),
                ('state', models.CharField(choices=[('brk', 'broken'), ('run', 'running')], default='run', editable=False, max_length=3, verbose_name='Текущее состояние')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Дата запуска')),
                ('break_date', models.DateTimeField(blank=True, editable=False, null=True, verbose_name='Дата поломки')),
            ],
            options={
                'verbose_name': 'Станция',
                'verbose_name_plural': 'Станции',
            },
        ),
        migrations.CreateModel(
            name='Directive',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('axis', models.CharField(choices=[('x', 'x'), ('y', 'y'), ('z', 'z')], max_length=1, verbose_name='Ось')),
                ('distance', models.SmallIntegerField(verbose_name='Расстояние')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Дата запуска')),
                ('station', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='directives', to='stations.station')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='directives', to=settings.AUTH_USER_MODEL, verbose_name='Автор указания')),
            ],
            options={
                'verbose_name': 'Указание',
                'verbose_name_plural': 'Указания',
            },
        ),
        migrations.CreateModel(
            name='Coordinates',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('x', models.SmallIntegerField(default=100, verbose_name='Координата по x')),
                ('y', models.SmallIntegerField(default=100, verbose_name='Координата по y')),
                ('z', models.SmallIntegerField(default=100, verbose_name='Координата по z')),
                ('station', models.OneToOneField(on_delete=django.db.models.deletion.DO_NOTHING, to='stations.station', verbose_name='Станция')),
            ],
            options={
                'verbose_name': 'Координаты',
                'verbose_name_plural': 'Координаты',
            },
        ),
    ]