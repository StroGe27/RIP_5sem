from rest_framework import serializers

from .models import *


class TariffSerializer(serializers.ModelSerializer):
    months = serializers.SerializerMethodField()

    def get_months(self, tariff):
        return self.context.get("months", "")

    class Meta:
        model = Tariff
        fields = "__all__"


class UserCheckSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ('id', 'name', 'email', 'is_moderator')


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ('name',)


class VirtualSerializer(serializers.ModelSerializer):
    tariffs = serializers.SerializerMethodField()
    owner = UserSerializer(read_only=True, many=False)
    moderator = UserSerializer(read_only=True, many=False)

    def get_tariffs(self, virtual):
        items = TariffVirtual.objects.filter(virtual_id=virtual.pk)

        tariffs = []
        for item in items:
            serializer = TariffSerializer(
                item.tariff,
                context={
                    "months": item.months
                }
            )
            tariffs.append(serializer.data)

        return tariffs

    class Meta:
        model = Virtual
        fields = "__all__"


class VirtualsSerializer(serializers.ModelSerializer):
    owner = UserSerializer(read_only=True, many=False)
    moderator = UserSerializer(read_only=True, many=False)

    class Meta:
        model = Virtual
        fields = "__all__"


class TariffVirtualSerializer(serializers.ModelSerializer):
    class Meta:
        model = TariffVirtual
        fields = "__all__"


class UserRegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ('id', 'email', 'password', 'name')
        write_only_fields = ('password',)
        read_only_fields = ('id',)

    def create(self, validated_data):
        user = CustomUser.objects.create(
            email=validated_data['email'],
            name=validated_data['name']
        )

        user.set_password(validated_data['password'])
        user.save()

        return user


class UserLoginSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)
    password = serializers.CharField(required=True)


