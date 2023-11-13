from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from rest_framework import status
from api.serializers import OrderSerializer
from api.models import Orders
from rest_framework.views import APIView
from rest_framework.decorators import api_view

class OrderList(APIView):
    model_class = Orders
    serializer_class = OrderSerializer
    
    def get(self, request, format=None):
        """
        Возвращает список товаров
        """
        orders = self.model_class.objects.all()
        serializer = self.serializer_class(orders, many=True)
        return Response(serializer.data)
    
    def post(self, request, format=None):
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

    def get(self, request, pk, format=None):
        """
        Возвращает информацию о товаре
        """
        order = get_object_or_404(self.model_class, pk=pk)
        serializer = self.serializer_class(order)
        return Response(serializer.data)
    
    def put(self, request, pk, format=None):
        """
        Обновляет информацию о товаре (для модератора)
        """
        stock = get_object_or_404(self.model_class, pk=pk)
        serializer = self.serializer_class(stock, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        """
        Удаляет информацию товаре
        """
        stock = get_object_or_404(self.model_class, pk=pk)
        stock.delete() # поменять на изменение статуса
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