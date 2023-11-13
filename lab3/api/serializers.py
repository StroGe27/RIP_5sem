from api.models import Orders
from rest_framework import serializers


class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        # Модель, которую мы сериализуем
        model = Orders
        # Поля, которые мы сериализуем
        fields = ["pk", "title", "status", "processor", "ghz", "ram", "availableos", "cost"]
