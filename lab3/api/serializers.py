from api.models import Orders
from api.models import Requests
from rest_framework import serializers

class RequestSerializer(serializers.ModelSerializer):
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
        fields = ["id", "title", "status", "processor", "ghz", "ram", "availableos", "cost", "img"]
