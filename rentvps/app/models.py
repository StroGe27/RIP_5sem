from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.db import models
from django.utils import timezone
from django.contrib.auth.models import PermissionsMixin


class Tariff(models.Model):
    STATUS_CHOICES = (
        (1, 'Действует'),
        (2, 'Удалена'),
    )

    name = models.CharField(verbose_name="Название", blank=True)
    description = models.TextField(verbose_name="Описание", blank=True)
    ram = models.IntegerField(verbose_name="Оперативная память", null=True)
    ssd = models.IntegerField(verbose_name="Размер SSD хранилища", null=True)
    price = models.IntegerField(verbose_name="Цена в месяц", null=True)

    status = models.IntegerField( verbose_name="Статус", choices=STATUS_CHOICES, default=1)
    image = models.ImageField(verbose_name="Картинка", default="tariffs/default.jpg", upload_to="tariffs")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Тариф"
        verbose_name_plural = "Тарифы"


class CustomUserManager(BaseUserManager):
    def create_user(self, name, email, password="1234", **extra_fields):
        extra_fields.setdefault('name', name)
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, name, email, password="1234", **extra_fields):
        extra_fields.setdefault('is_moderator', True)
        extra_fields.setdefault('is_active', True)
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(name, email, password, **extra_fields)


class CustomUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)
    name = models.CharField(max_length=30)
    is_moderator = models.BooleanField(default=False)

    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name']

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"


class Virtual(models.Model):
    STATUS_CHOICES = (
        (1, 'Введён'),
        (2, 'В работе'),
        (3, 'Завершен'),
        (4, 'Отклонен'),
        (5, 'Удален'),
    )

    status = models.IntegerField(verbose_name="Статус", choices=STATUS_CHOICES, default=1)
    date_created = models.DateTimeField(verbose_name="Дата создания", default=timezone.now())
    date_formation = models.DateTimeField(verbose_name="Дата формирования", blank=True, null=True)
    date_complete = models.DateTimeField(verbose_name="Дата завершения", blank=True, null=True)

    owner = models.ForeignKey(CustomUser, on_delete=models.DO_NOTHING, verbose_name="Создатель", related_name='owner', null=True)
    moderator = models.ForeignKey(CustomUser, on_delete=models.DO_NOTHING, verbose_name="Модератор", related_name='moderator', null=True)

    def __str__(self):
        return "Виртуальная машина №" + str(self.pk)

    class Meta:
        verbose_name = "Виртуальная машина"
        verbose_name_plural = "Виртуальные машины"
        ordering = ('-date_formation', )


# м-м
class TariffVirtual(models.Model):
    tariff = models.ForeignKey(Tariff, models.CASCADE, blank=True, null=True)
    virtual = models.ForeignKey(Virtual, models.CASCADE, blank=True, null=True)
    months = models.IntegerField(verbose_name="Кол-во месяцев аренды", blank=True, null=True)

    def __str__(self):
        return "М-М №" + str(self.pk)

    class Meta:
        verbose_name = "М-М"
        verbose_name_plural = "М-М"
