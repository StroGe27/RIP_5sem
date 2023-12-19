from api.models import Orders
from api.models import Requests
from api.models import Users
from rest_framework import serializers

class RequestSerializer(serializers.ModelSerializer):
    # id = serializers.IntegerField(read_only=False)  #чтобы можно было добавлять с произвольным id
    class Meta:
        # Модель, которую мы сериализуем
        model = Requests
        # Поля, которые мы сериализуем
        fields = ["date_create", "date_formation", "date_complete", "moderator", "user", "status"]

class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        # Модель, которую мы сериализуем
        model = Orders
        # Поля, которые мы сериализуем
        fields = ["id", "title", "status", "processor", "ghz", "ram", "ip", "processor_type_id", "availableos", "cost", "img"]

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        # Модель, которую мы сериализуем
        model = Users
        # Поля, которые мы сериализуем
        fields = ["id", "name", "mail", "password", "role"]

