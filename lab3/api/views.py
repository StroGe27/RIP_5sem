from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from rest_framework import status

from api.serializers import OrderSerializer
from api.serializers import RequestSerializer
from api.serializers import UserSerializer

from api.models import Orders
from api.models import Requests
from api.models import Users

from rest_framework.views import APIView
from rest_framework.decorators import api_view

from drf_yasg.utils import swagger_auto_schema
from api.serializers import OrdersSerializer
class OrdersList(APIView): 
    @swagger_auto_schema(request_body=OrdersSerializer)
    def post(self, request, format=None):
	    pass

class OrdersDetail(APIView):
    @swagger_auto_schema(request_body=OrdersSerializer)
    def put(self, request, pk, format=None):
	    pass

@swagger_auto_schema(method='put', request_body=OrderSerializer)

class OrderList(APIView):
    model_class = Orders
    serializer_class = OrderSerializer
    def get(self, request, format=None):
        orders = self.model_class.objects.all()
        serializer = self.serializer_class(orders, many=True)
        return Response(serializer.data)
    def post(self, request, format=None):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class OrderDetail(APIView):
    model_class = Orders
    serializer_class = OrderSerializer

    def get(self, request, id, format=None):
        order = get_object_or_404(self.model_class, id=id)
        serializer = self.serializer_class(order)
        return Response(serializer.data)
    
    def put(self, request, id, format=None):
        order = get_object_or_404(self.model_class, id=id)
        serializer = self.serializer_class(order, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, id, format=None):
        order = get_object_or_404(self.model_class, id=id)
        order.status = "deleted"
        order.save()        
        return Response(status=status.HTTP_204_NO_CONTENT)
    
@api_view(["GET"])   
def OrderSearch(request):
    search_query = request.GET.get('title', '')  # Пример GET запроса: /your-endpoint/?search=ваша_строка
    proc_type = request.GET.get('type', '')

    left_cost = request.GET.get('lcost', '') 
    right_cost = request.GET.get('rcost', '')

    orders = Orders.objects.filter(title__icontains=search_query)
    if proc_type == "Intel":
        orders = orders.filter(processor_type_id=1)
    elif proc_type == "AMD":
        orders = orders.ofilter(processor_type_id=2)

    print("hello", left_cost, right_cost)
    orders = orders.filter(cost__range=(left_cost, right_cost))

    serializer = OrderSerializer(orders, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(["GET"])   
def OrderRangedCost(request):
    left_range = request.GET.get('lcost', '') 
    right_range = request.GET.get('rcost', '')
    orders = Orders.objects.filter(cost__range=(left_range, right_range))
    # if left_range and right_range:
    #     orders = Orders.objects.filter(cost__range=(left_range, right_range))
    # else:
    #     orders = Orders.objects.filter(cost__range=(1, 100000))
    serializer = OrderSerializer(orders, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)

class RequestList(APIView):
    model_class = Requests
    serializer_class = RequestSerializer
    
    def get(self, request, format=None):
        request = self.model_class.objects.all().order_by('date_create')
        serializer = self.serializer_class(request, many=True)
        return Response(serializer.data)
    
    def post(self, request, format=None):
        serializer = self.serializer_class(data=request.data)
        print(request)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class RequestDetail(APIView):
    model_class = Requests
    serializer_class = RequestSerializer

    def get(self, request, id, format=None):
        requests = get_object_or_404(self.model_class.objects.all(), id=id)
        serializer = self.serializer_class(requests)
        return Response(serializer.data)
    
    def put(self, request, id, format=None):
        requests = get_object_or_404(self.model_class, id=id)
        serializer = self.serializer_class(requests, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, id, format=None):
        requests = get_object_or_404(self.model_class, id=id)
        requests.status_id = 2  # обновляем статус на deleted
        requests.save()   
        return Response(status=status.HTTP_204_NO_CONTENT)

