from django.contrib.auth import authenticate
from django.http import HttpResponse
from django.utils.dateparse import parse_datetime
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response

from .jwt_helper import *
from .permissions import *
from .serializers import *
from .utils import identity_user


def get_draft_virtual(request):
    user = identity_user(request)

    if user is None:
        return None

    virtual = Virtual.objects.filter(owner_id=user.pk).filter(status=1).first()

    if virtual is None:
        return None

    return virtual


@api_view(["GET"])
def search_tariffs(request):
    query = request.GET.get("query", "")

    tariffs = Tariff.objects.filter(status=1).filter(name__icontains=query)

    serializer = TariffSerializer(tariffs, many=True)

    draft_virtual = get_draft_virtual(request)

    resp = {
        "tariffs": serializer.data,
        "draft_virtual_id": draft_virtual.pk if draft_virtual else None
    }

    return Response(resp)


@api_view(["GET"])
def get_tariff_by_id(request, tariff_id):
    if not Tariff.objects.filter(pk=tariff_id).exists():
        return Response(status=status.HTTP_404_NOT_FOUND)

    tariff = Tariff.objects.get(pk=tariff_id)
    serializer = TariffSerializer(tariff)

    return Response(serializer.data)


@api_view(["PUT"])
@permission_classes([IsModerator])
def update_tariff(request, tariff_id):
    if not Tariff.objects.filter(pk=tariff_id).exists():
        return Response(status=status.HTTP_404_NOT_FOUND)

    tariff = Tariff.objects.get(pk=tariff_id)
    serializer = TariffSerializer(tariff, data=request.data, partial=True)

    if serializer.is_valid():
        serializer.save()

    return Response(serializer.data)


@api_view(["POST"])
@permission_classes([IsModerator])
def create_tariff(request):
    tariff = Tariff.objects.create()

    serializer = TariffSerializer(tariff)

    return Response(serializer.data)


@api_view(["DELETE"])
@permission_classes([IsAuthenticated])
def delete_tariff(request, tariff_id):
    if not Tariff.objects.filter(pk=tariff_id).exists():
        return Response(status=status.HTTP_404_NOT_FOUND)

    tariff = Tariff.objects.get(pk=tariff_id)
    tariff.status = 5
    tariff.save()

    tariffs = Tariff.objects.filter(status=1)
    serializer = TariffSerializer(tariffs, many=True)

    return Response(serializer.data)


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def add_tariff_to_virtual(request, tariff_id):
    if not Tariff.objects.filter(pk=tariff_id).exists():
        return Response(status=status.HTTP_404_NOT_FOUND)

    tariff = Tariff.objects.get(pk=tariff_id)

    draft_virtual = get_draft_virtual(request)

    if draft_virtual is None:
        draft_virtual = Virtual.objects.create()
        draft_virtual.owner = identity_user(request)
        draft_virtual.save()

    if TariffVirtual.objects.filter(virtual=draft_virtual, tariff=tariff).exists():
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)

    cons = TariffVirtual.objects.create()
    cons.virtual = draft_virtual
    cons.tariff = tariff
    cons.save()

    return Response(status=status.HTTP_200_OK)


@api_view(["GET"])
def get_tariff_image(request, tariff_id):
    if not Tariff.objects.filter(pk=tariff_id).exists():
        return Response(status=status.HTTP_404_NOT_FOUND)

    tariff = Tariff.objects.get(pk=tariff_id)

    return HttpResponse(tariff.image, content_type="image/png")


@api_view(["PUT"])
@permission_classes([IsModerator])
def update_tariff_image(request, tariff_id):
    if not Tariff.objects.filter(pk=tariff_id).exists():
        return Response(status=status.HTTP_404_NOT_FOUND)

    tariff = Tariff.objects.get(pk=tariff_id)
    serializer = TariffSerializer(tariff, data=request.data, partial=True)

    if serializer.is_valid():
        serializer.save()

    return Response(serializer.data)


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def search_virtuals(request):
    user = identity_user(request)

    status_id = int(request.GET.get("status", -1))
    date_start = request.GET.get("date_start")
    date_end = request.GET.get("date_end")

    virtuals = Virtual.objects.exclude(status__in=[1, 5])

    if not user.is_moderator:
        virtuals = virtuals.filter(owner_id=user.pk)

    if status_id != -1:
        virtuals = virtuals.filter(status=status_id)

    if date_start and parse_datetime(date_start):
        virtuals = virtuals.filter(date_formation__gte=parse_datetime(date_start))

    if date_end and parse_datetime(date_end):
        virtuals = virtuals.filter(date_formation__lte=parse_datetime(date_end))

    serializer = VirtualsSerializer(virtuals, many=True)

    return Response(serializer.data)


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def get_virtual_by_id(request, virtual_id):
    if not Virtual.objects.filter(pk=virtual_id).exists():
        return Response(status=status.HTTP_404_NOT_FOUND)

    virtual = Virtual.objects.get(pk=virtual_id)
    serializer = VirtualSerializer(virtual)

    return Response(serializer.data)


@api_view(["PUT"])
@permission_classes([IsAuthenticated])
def update_virtual(request, virtual_id):
    if not Virtual.objects.filter(pk=virtual_id).exists():
        return Response(status=status.HTTP_404_NOT_FOUND)

    virtual = Virtual.objects.get(pk=virtual_id)
    serializer = VirtualSerializer(virtual, data=request.data, partial=True)

    if serializer.is_valid():
        serializer.save()

    return Response(serializer.data)


@api_view(["PUT"])
@permission_classes([IsRemoteService])
def update_virtual_clinical_trial(request, virtual_id):
    if not Virtual.objects.filter(pk=virtual_id).exists():
        return Response(status=status.HTTP_404_NOT_FOUND)

    virtual = Virtual.objects.get(pk=virtual_id)
    serializer = VirtualSerializer(virtual, data=request.data, partial=True)

    if serializer.is_valid():
        serializer.save()

    return Response(serializer.data)


@api_view(["PUT"])
@permission_classes([IsAuthenticated])
def update_status_user(request, virtual_id):
    if not Virtual.objects.filter(pk=virtual_id).exists():
        return Response(status=status.HTTP_404_NOT_FOUND)

    virtual = Virtual.objects.get(pk=virtual_id)

    virtual.owner = identity_user(request)
    virtual.status = 2
    virtual.date_formation = timezone.now()
    virtual.save()

    serializer = VirtualSerializer(virtual)

    return Response(serializer.data)


@api_view(["PUT"])
@permission_classes([IsModerator])
def update_status_admin(request, virtual_id):
    if not Virtual.objects.filter(pk=virtual_id).exists():
        return Response(status=status.HTTP_404_NOT_FOUND)

    request_status = int(request.data["status"])

    if request_status not in [3, 4]:
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)

    virtual = Virtual.objects.get(pk=virtual_id)

    if virtual.status != 2:
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)

    virtual.moderator = identity_user(request)
    virtual.status = request_status
    virtual.date_complete = timezone.now()
    virtual.save()

    serializer = VirtualSerializer(virtual)

    return Response(serializer.data)


@api_view(["DELETE"])
@permission_classes([IsAuthenticated])
def delete_virtual(request, virtual_id):
    if not Virtual.objects.filter(pk=virtual_id).exists():
        return Response(status=status.HTTP_404_NOT_FOUND)

    virtual = Virtual.objects.get(pk=virtual_id)

    if virtual.status != 1:
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)

    virtual.status = 5
    virtual.save()

    return Response(status=status.HTTP_200_OK)


@api_view(["DELETE"])
@permission_classes([IsAuthenticated])
def delete_tariff_from_virtual(request, virtual_id, tariff_id):
    if not TariffVirtual.objects.filter(virtual_id=virtual_id, tariff_id=tariff_id).exists():
        return Response(status=status.HTTP_404_NOT_FOUND)

    item = TariffVirtual.objects.get(virtual_id=virtual_id, tariff_id=tariff_id)
    item.delete()

    if not TariffVirtual.objects.filter(virtual_id=virtual_id).exists():
        virtual = Virtual.objects.get(pk=virtual_id)
        virtual.delete()

    return Response(status=status.HTTP_200_OK)


@api_view(["PUT"])
@permission_classes([IsAuthenticated])
def update_tariff_in_virtual(request, virtual_id, tariff_id):
    if not TariffVirtual.objects.filter(tariff_id=tariff_id, virtual_id=virtual_id).exists():
        return Response(status=status.HTTP_404_NOT_FOUND)

    item = TariffVirtual.objects.get(tariff_id=tariff_id, virtual_id=virtual_id)

    serializer = TariffVirtualSerializer(item, data=request.data, many=False, partial=True)

    if serializer.is_valid():
        serializer.save()

    return Response(serializer.data)


@swagger_auto_schema(method='post', request_body=UserLoginSerializer)
@api_view(["POST"])
def login(request):
    serializer = UserLoginSerializer(data=request.data)

    if not serializer.is_valid():
        return Response(serializer.errors, status=status.HTTP_401_UNAUTHORIZED)

    user = authenticate(**serializer.data)
    if user is None:
        message = {"message": "Введенные данные невалидны"}
        return Response(message, status=status.HTTP_401_UNAUTHORIZED)

    access_token = create_access_token(user.id)

    user_data = {
        "user_id": user.id,
        "name": user.name,
        "email": user.email,
        "is_moderator": user.is_moderator,
        "access_token": access_token
    }

    return Response(user_data, status=status.HTTP_200_OK)


@api_view(["POST"])
def register(request):
    serializer = UserRegisterSerializer(data=request.data)

    if not serializer.is_valid():
        return Response(status=status.HTTP_409_CONFLICT)

    user = serializer.save()

    access_token = create_access_token(user.id)

    message = {
        'message': 'Пользователь успешно зарегистрирован',
        'user_id': user.id,
        "access_token": access_token
    }

    return Response(message, status=status.HTTP_201_CREATED)


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def check(request):
    user = identity_user(request)

    user = CustomUser.objects.get(pk=user.pk)
    serializer = UserCheckSerializer(user)

    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def logout(request):
    access_token = get_access_token(request)

    if access_token not in cache:
        cache.set(access_token, settings.JWT["ACCESS_TOKEN_LIFETIME"])

    message = {
        "message": "Вы успешно вышли из аккаунта"
    }

    return Response(message, status=status.HTTP_200_OK)
