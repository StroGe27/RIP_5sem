# Generated by Django 4.2.5 on 2024-01-31 19:51

import datetime
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='CustomUser',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('email', models.EmailField(max_length=254, unique=True)),
                ('name', models.CharField(max_length=30)),
                ('is_moderator', models.BooleanField(default=False)),
                ('is_staff', models.BooleanField(default=False)),
                ('is_active', models.BooleanField(default=True)),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.permission', verbose_name='user permissions')),
            ],
            options={
                'verbose_name': 'Пользователь',
                'verbose_name_plural': 'Пользователи',
            },
        ),
        migrations.CreateModel(
            name='Tariff',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, verbose_name='Название')),
                ('description', models.TextField(blank=True, verbose_name='Описание')),
                ('ram', models.IntegerField(null=True, verbose_name='Оперативная память')),
                ('ssd', models.IntegerField(null=True, verbose_name='Размер SSD хранилища')),
                ('price', models.IntegerField(null=True, verbose_name='Цена в месяц')),
                ('status', models.IntegerField(choices=[(1, 'Действует'), (2, 'Удалена')], default=1, verbose_name='Статус')),
                ('image', models.ImageField(default='tariffs/default.jpg', upload_to='tariffs', verbose_name='Картинка')),
            ],
            options={
                'verbose_name': 'Тариф',
                'verbose_name_plural': 'Тарифы',
            },
        ),
        migrations.CreateModel(
            name='Virtual',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.IntegerField(choices=[(1, 'Введён'), (2, 'В работе'), (3, 'Завершен'), (4, 'Отклонен'), (5, 'Удален')], default=1, verbose_name='Статус')),
                ('date_created', models.DateTimeField(default=datetime.datetime(2024, 1, 31, 19, 51, 43, 254563, tzinfo=datetime.timezone.utc), verbose_name='Дата создания')),
                ('date_formation', models.DateTimeField(blank=True, null=True, verbose_name='Дата формирования')),
                ('date_complete', models.DateTimeField(blank=True, null=True, verbose_name='Дата завершения')),
                ('moderator', models.ForeignKey(null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='moderator', to=settings.AUTH_USER_MODEL, verbose_name='Модератор')),
                ('owner', models.ForeignKey(null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='owner', to=settings.AUTH_USER_MODEL, verbose_name='Создатель')),
            ],
            options={
                'verbose_name': 'Виртуальная машина',
                'verbose_name_plural': 'Виртуальные машины',
                'ordering': ('-date_formation',),
            },
        ),
        migrations.CreateModel(
            name='TariffVirtual',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('months', models.IntegerField(blank=True, null=True, verbose_name='Кол-во месяцев аренды')),
                ('tariff', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='app.tariff')),
                ('virtual', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='app.virtual')),
            ],
            options={
                'verbose_name': 'М-М',
                'verbose_name_plural': 'М-М',
            },
        ),
    ]
