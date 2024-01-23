import requests
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


def get_draft_order(request):
    user = identity_user(request)

    if user is None:
        return None

    order = Order.objects.filter(owner_id=user.pk).filter(status=1).first()

    if order is None:
        return None

    return order


@api_view(["GET"])
def search_tariffs(request):
    query = request.GET.get("query", "")

    tariffs = Tariff.objects.filter(status=1).filter(name__icontains=query)

    serializer = TariffSerializer(tariffs, many=True)

    draft_order = get_draft_order(request)

    resp = {
        "tariffs": serializer.data,
        "draft_order_id": draft_order.pk if draft_order else None
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
def add_tariff_to_order(request, tariff_id):
    if not Tariff.objects.filter(pk=tariff_id).exists():
        return Response(status=status.HTTP_404_NOT_FOUND)

    tariff = Tariff.objects.get(pk=tariff_id)

    draft_order = get_draft_order(request)

    if draft_order is None:
        draft_order = Order.objects.create()
        draft_order.owner = identity_user(request)
        draft_order.save()

    if TariffOrder.objects.filter(order=draft_order, tariff=tariff).exists():
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)

    cons = TariffOrder.objects.create()
    cons.order = draft_order
    cons.tariff = tariff
    cons.save()

    serializer = OrderSerializer(draft_order)

    return Response(serializer.data)


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
def search_orders(request):
    user = identity_user(request)

    status_id = int(request.GET.get("status", -1))
    date_start = request.GET.get("date_start")
    date_end = request.GET.get("date_end")

    orders = Order.objects.exclude(status__in=[1, 5])

    if not user.is_moderator:
        orders = orders.filter(owner_id=user.pk)

    if status_id != -1:
        orders = orders.filter(status=status_id)

    if date_start and parse_datetime(date_start):
        orders = orders.filter(date_formation__gte=parse_datetime(date_start))

    if date_end and parse_datetime(date_end):
        orders = orders.filter(date_formation__lte=parse_datetime(date_end))

    serializer = OrdersSerializer(orders, many=True)

    return Response(serializer.data)


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def get_order_by_id(request, order_id):
    if not Order.objects.filter(pk=order_id).exists():
        return Response(status=status.HTTP_404_NOT_FOUND)

    order = Order.objects.get(pk=order_id)
    serializer = OrderSerializer(order)

    return Response(serializer.data)


@api_view(["PUT"])
@permission_classes([IsAuthenticated])
def update_order(request, order_id):
    if not Order.objects.filter(pk=order_id).exists():
        return Response(status=status.HTTP_404_NOT_FOUND)

    order = Order.objects.get(pk=order_id)
    serializer = OrderSerializer(order, data=request.data, partial=True)

    if serializer.is_valid():
        serializer.save()

    return Response(serializer.data)


@api_view(["PUT"])
@permission_classes([IsRemoteService])
def update_order_clinical_trial(request, order_id):
    if not Order.objects.filter(pk=order_id).exists():
        return Response(status=status.HTTP_404_NOT_FOUND)

    order = Order.objects.get(pk=order_id)
    serializer = OrderSerializer(order, data=request.data, partial=True)

    if serializer.is_valid():
        serializer.save()

    return Response(serializer.data)


@api_view(["PUT"])
@permission_classes([IsAuthenticated])
def update_status_user(request, order_id):
    if not Order.objects.filter(pk=order_id).exists():
        return Response(status=status.HTTP_404_NOT_FOUND)

    order = Order.objects.get(pk=order_id)

    order.owner = identity_user(request)
    order.status = 2
    order.date_formation = timezone.now()
    order.save()

    serializer = OrderSerializer(order)

    return Response(serializer.data)


@api_view(["PUT"])
@permission_classes([IsModerator])
def update_status_admin(request, order_id):
    if not Order.objects.filter(pk=order_id).exists():
        return Response(status=status.HTTP_404_NOT_FOUND)

    request_status = int(request.data["status"])

    if request_status not in [3, 4]:
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)

    order = Order.objects.get(pk=order_id)

    if order.status != 2:
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)

    order.moderator = identity_user(request)
    order.status = request_status
    order.date_complete = timezone.now()
    order.save()

    serializer = OrderSerializer(order)

    return Response(serializer.data)


@api_view(["DELETE"])
@permission_classes([IsAuthenticated])
def delete_order(request, order_id):
    if not Order.objects.filter(pk=order_id).exists():
        return Response(status=status.HTTP_404_NOT_FOUND)

    order = Order.objects.get(pk=order_id)

    if order.status != 1:
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)

    order.status = 5
    order.save()

    return Response(status=status.HTTP_200_OK)


@api_view(["DELETE"])
@permission_classes([IsAuthenticated])
def delete_tariff_from_order(request, order_id, tariff_id):
    if not TariffOrder.objects.filter(order_id=order_id, tariff_id=tariff_id).exists():
        return Response(status=status.HTTP_404_NOT_FOUND)

    item = TariffOrder.objects.get(order_id=order_id, tariff_id=tariff_id)
    item.delete()

    if not TariffOrder.objects.filter(order_id=order_id).exists():
        order = Order.objects.get(pk=order_id)
        order.delete()

    return Response(status=status.HTTP_200_OK)


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def get_tariff_in_order(request, order_id, tariff_id):
    if not TariffOrder.objects.filter(tariff_id=tariff_id, order_id=order_id).exists():
        return Response(status=status.HTTP_404_NOT_FOUND)

    item = TariffOrder.objects.get(tariff_id=tariff_id, order_id=order_id)
    return Response(item.months)


@api_view(["PUT"])
@permission_classes([IsAuthenticated])
def update_tariff_in_order(request, order_id, tariff_id):
    if not TariffOrder.objects.filter(tariff_id=tariff_id, order_id=order_id).exists():
        return Response(status=status.HTTP_404_NOT_FOUND)

    item = TariffOrder.objects.get(tariff_id=tariff_id, order_id=order_id)

    serializer = TariffOrderSerializer(item, data=request.data, many=False, partial=True)

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

    serializer = UserSerializer(
        user,
        context={
            "access_token": access_token
        }
    )

    response = Response(serializer.data, status=status.HTTP_200_OK)

    response.set_cookie('access_token', access_token, httponly=False, expires=settings.JWT["ACCESS_TOKEN_LIFETIME"])

    return response


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

    response = Response(message, status=status.HTTP_201_CREATED)

    response.set_cookie('access_token', access_token, httponly=False, expires=settings.JWT["ACCESS_TOKEN_LIFETIME"])

    return response


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def check(request):
    user = identity_user(request)

    user = CustomUser.objects.get(pk=user.pk)
    serializer = UserSerializer(user)

    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def logout(request):
    access_token = get_access_token(request)

    if access_token not in cache:
        cache.set(access_token, settings.JWT["ACCESS_TOKEN_LIFETIME"])

    message = {"message": "Вы успешно вышли из аккаунта"}
    response = Response(message, status=status.HTTP_200_OK)

    response.delete_cookie('access_token')

    return response
