# Добавляем импорты для работы с Django и Django REST Framework
from rest_framework.response import Response
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from rest_framework import status, viewsets

# Добавляем импорт для работы с API

from rest_framework.views import APIView
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from api.serializers import *
from api.models import Orders, Requests, CustomUser
from api.permissions import *

# Добавляем импорты для аутентификации

from django.contrib.auth import authenticate, login, logout
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from django.conf import settings
import redis
import uuid
from django.contrib.sessions.models import Session

# Добавляем импорты для работы с Swagger

from drf_yasg.utils import swagger_auto_schema

# Добавляем импорт для работы с Minio

from minio import Minio
from minio.error import S3Error
from datetime import datetime

session_storage = redis.StrictRedis(host=settings.REDIS_HOST, port=settings.REDIS_PORT)

@api_view(['GET'])
def getOrders(request):
    orders = Orders.objects.filter(status='valid')
    serializer = OrderSerializer(orders, many=True)
    return Response(serializer.data)

@api_view(['POST'])
@permission_classes([IsManager])
def postOrders(request):
    serializer = OrderSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def getOrdersDetiled(request, id, format=None):
    order = Orders.objects.get(id=id)
    serializer = OrderSerializer(order)
    return Response(serializer.data)
@api_view(['PUT'])
def putOrdersDetiled(request, id, format=None):
    order = get_object_or_404(Orders, id=id)
    serializer = OrderSerializer(order, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(["DELETE"])
def deleteOrdersDetiled(request, id, format=None):
    order = get_object_or_404(Orders, id=id)
    order.status = "deleted"
    order.save()        
    return Response(status=status.HTTP_204_NO_CONTENT)

@api_view(['GET'])   
def searchOrders(request):
    search_query = request.GET.get('title', '')
    proc_type = request.GET.get('type', '')
    left_cost = request.GET.get('lcost', '') 
    right_cost = request.GET.get('rcost', '')
    
    orders = Orders.objects.filter(status='valid')
    
    if search_query:
        orders = orders.filter(title__icontains=search_query)
        
    if proc_type == "Intel":
        orders = orders.filter(processor_type_id=1)
    elif proc_type == "AMD":
        orders = orders.filter(processor_type_id=2)
    
    # if left_cost and right_cost:
    #     orders = orders.filter(cost__range=(int(left_cost), int(right_cost)))
    
    serializer = OrderSerializer(orders, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(['GET'])   
def getRequests(request, format=None):
    requests = Requests.objects.all().order_by('date_create')
    serializer = RequestSerializer(requests, many=True)
    return Response(serializer.data)


@api_view(['POST'])
def postRequests(request, format=None):
    serializer = OrderSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def getRequestsDetiled(request, id, format=None):
    requests = get_object_or_404(Orders, id=id)
    serializer = OrderSerializer(requests)
    return Response(serializer.data)

@api_view(['PUT'])
def putRequestsDetiled(request, id, format=None):
    requests = get_object_or_404(Orders, id=id)
    serializer = OrderSerializer(requests, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(["DELETE"])
def deleteRequestsDetiled(request, id, format=None):
    requests = get_object_or_404(Orders, id=id)
    requests.status_id = 2
    requests.save()   
    return Response(status=status.HTTP_204_NO_CONTENT)

# Authorization methods
class UserViewSet(viewsets.ModelViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer
    model_class = CustomUser
    authentication_classes = []
    permission_classes = [AllowAny]

    def create(self, request):
        print('req is', request.data)
        if self.model_class.objects.filter(email=request.data['email']).exists():
            return Response({'status': 'Exist'}, status=400)
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            self.model_class.objects.create_user(email=serializer.data['email'],
                                     password=serializer.data['password'],
                                     full_name=serializer.data['full_name'],
                                     is_superuser=serializer.data['is_superuser'],
                                     is_staff=serializer.data['is_staff'])
            random_key = str(uuid.uuid4())
            session_storage.set(random_key, serializer.data['email'])
            user_data = {
                "email": request.data['email'],
                "full_name": request.data['full_name'],
                #"phone_number": request.data['phone_number'],
                "is_superuser": False
            }

            print('user data is ', user_data)
            response = Response(user_data, status=status.HTTP_201_CREATED)
            # response = HttpResponse("{'status': 'ok'}")
            response.set_cookie("session_id", random_key)
            return response
            # return Response({'status': 'Success'}, status=200)
        return Response({'status': 'Error', 'error': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

@swagger_auto_schema(method='post', request_body=UserSerializer)
@api_view(['Post'])
@permission_classes([AllowAny])
def login_view(request):
    username = request.data.get('email')
    password = request.data.get('password')
    user = authenticate(request, email=username, password=password)
    if user is not None:
        print(user)
        random_key = str(uuid.uuid4())
        session_storage.set(random_key, username)
        user_data = {
            "id_user": user.id,
            "email": user.email,
            "full_name": user.full_name,
            #"phone_number": user.phone_number,
            "password": user.password,
            #"is_superuser": user.is_superuser,
        }
        response = Response(user_data, status=status.HTTP_201_CREATED)
        response.set_cookie("session_id", random_key, samesite="Lax", max_age=30 * 24 * 60 * 60)
        return response
    else:
        return HttpResponse("login failed", status=400)

@api_view(['POST'])
@permission_classes([IsAuth])
def logout_view(request):
    ssid = request.COOKIES["session_id"]
    if session_storage.exists(ssid):
        session_storage.delete(ssid)
        response_data = {'status': 'Success'}
    else:
        response_data = {'status': 'Error', 'message': 'Session does not exist'}
    return Response(response_data)

@api_view(['GET'])
# @permission_classes([IsAuth])
def user_info(request):
    try:
        ssid = request.COOKIES["session_id"]
        if session_storage.exists(ssid):
            email = session_storage.get(ssid).decode('utf-8')
            user = CustomUser.objects.get(email=email)
            user_data = {
                "user_id": user.id,
                "email": user.email,
                "full_name": user.full_name,
                "is_superuser": user.is_superuser
            }
            return Response(user_data, status=status.HTTP_200_OK)
        else:
            return Response({'status': 'Error', 'message': 'Session does not exist'})
    except:
        return Response({'status': 'Error', 'message': 'Cookies are not transmitted'})