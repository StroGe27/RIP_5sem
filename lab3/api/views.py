from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from rest_framework import status

from api.serializers import OrderSerializer
from api.models import Orders
from api.serializers import RequestSerializer
from api.models import Requests

from rest_framework.views import APIView
from rest_framework.decorators import api_view

class OrderList(APIView):
    model_class = Orders
    serializer_class = OrderSerializer
    
    def get(self, request, format=None):
        orders = self.model_class.objects.all()
        serializer = self.serializer_class(orders, many=True)
        return Response(serializer.data)
    
    def post(self, request, format=None): # хз пока не работает
        """
        Добавляет новый товар
        """
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class OrderDetail(APIView):
    model_class = Orders
    serializer_class = OrderSerializer

    def get(self, request, id, format=None):
        """
        Возвращает информацию об услуге
        """
        order = get_object_or_404(self.model_class, id=id)
        serializer = self.serializer_class(order)
        return Response(serializer.data)
    
    def put(self, request, id, format=None):
        """
        Обновляет информацию об услуге (для модератора)
        """
        order = get_object_or_404(self.model_class, id=id)
        serializer = self.serializer_class(order, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, id, format=None):
        """
        Удаляет информацию об услуге
        """
        order = get_object_or_404(self.model_class, id=id)
        order.status = "deleted"
        order.save()        
        return Response(status=status.HTTP_204_NO_CONTENT)
    
class RequestList(APIView):
    model_class = Requests
    serializer_class = RequestSerializer
    
    def get(self, request, format=None):
        request = self.model_class.objects.all()
        serializer = self.serializer_class(request, many=True)
        return Response(serializer.data)
    
    def post(self, request, format=None): # хз пока не работает
        """
        Добавляет новую заявку
        """
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class RequestDetail(APIView):
    model_class = Requests
    serializer_class = RequestSerializer

    def get(self, request, id, format=None):
        """
        Возвращает информацию о заявке
        """
        requests = get_object_or_404(self.model_class, id=id)
        serializer = self.serializer_class(requests)
        return Response(serializer.data)
    
    def put(self, request, id, format=None):
        """
        Обновляет информацию о заявке (для модератора)
        """
        requests = get_object_or_404(self.model_class, id=id)
        serializer = self.serializer_class(requests, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, id, format=None):
        """
        Удаляет информацию о заявке
        """
        requests = get_object_or_404(self.model_class, id=id)
        requests.status_id = 2  # Update the status to 2
        requests.save()   
        return Response(status=status.HTTP_204_NO_CONTENT)



@api_view(['Put'])
def put_detail(request, pk, format=None):
    """
    Обновляет информацию о товаре (для пользователя)
    """
    stock = get_object_or_404(Orders, pk=pk)
    serializer = OrderSerializer(stock, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)