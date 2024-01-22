import random

from django.core import management
from django.core.management.base import BaseCommand
from ...models import *
from .utils import random_date, random_timedelta


def add_tariffs():
    Tariff.objects.create(
        name="Экономный тариф",
        description="Хостинг максимально оптимизирован под требования разных современных CMS систем, например таких как WordPress, Joomla, Drupal, PHPbb, Bitrix, Opencart и другие.",
        ram=4,
        ssd=5,
        price=500,
        image="tariffs/1.jpg"
    )
    Tariff.objects.create(
        name="Выгодный тариф",
        description="Хостинг максимально оптимизирован под требования разных современных CMS систем, например таких как WordPress, Joomla, Drupal, PHPbb, Bitrix, Opencart и другие.",
        ram=8,
        ssd=10,
        price=1000,
        image="tariffs/2.jpg"
    )
    Tariff.objects.create(
        name="Оптимальный тариф",
        description="Хостинг максимально оптимизирован под требования разных современных CMS систем, например таких как WordPress, Joomla, Drupal, PHPbb, Bitrix, Opencart и другие.",
        ram=12,
        ssd=15,
        price=1500,
        image="tariffs/3.jpg"
    )
    Tariff.objects.create(
        name="Мощный тариф",
        description="Хостинг максимально оптимизирован под требования разных современных CMS систем, например таких как WordPress, Joomla, Drupal, PHPbb, Bitrix, Opencart и другие.",
        ram=16,
        ssd=25,
        price=2500,
        image="tariffs/4.jpg"
    )

    print("Услуги добавлены")


def add_orders():
    users = CustomUser.objects.filter(is_superuser=False)
    moderators = CustomUser.objects.filter(is_superuser=True)

    if len(users) == 0 or len(moderators) == 0:
        print("Заявки не могут быть добавлены. Сначала добавьте пользователей с помощью команды add_users")
        return

    tariffs = Tariff.objects.all()

    for _ in range(30):
        order = Order.objects.create()
        order.status = random.randint(2, 5)
        order.owner = random.choice(users)

        if order.status in [3, 4]:
            order.date_complete = random_date()
            order.date_formation = order.date_complete - random_timedelta()
            order.date_created = order.date_formation - random_timedelta()
            order.moderator = random.choice(moderators)
            order.clinical_trial = random.randint(0, 1)
        else:
            order.date_formation = random_date()
            order.date_created = order.date_formation - random_timedelta()

        for i in range(random.randint(1, 3)):
            try:
                item = TariffOrder.objects.create()
                item.order = order
                item.tariff = random.choice(tariffs)
                item.months = random.randint(1, 12)
                item.save()
            except Exception as e:
                print(e)

        order.save()

    print("Заявки добавлены")


class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        management.call_command("clean_db")
        management.call_command("add_users")

        add_tariffs()
        add_orders()









