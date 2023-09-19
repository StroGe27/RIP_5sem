from datetime import date
from django.shortcuts import render
from django.http import HttpResponse

def GetOrders(request):
    return render(request, 'orders.html', {'data' : {
        'current_date': date.today(),
        'orders': [
            {'title': 'Книга с картинками', 'id': 1, 'src': '/images/1.jpg', 'definition': 'first'},
            {'title': 'Бутылка с водой', 'id': 2, 'src': 'images/2.jpg', 'definition': 'second'},
            {'title': 'Коврик для мышки', 'id': 3, 'src': 'images/3.jpg', 'definition': 'third'},
        ]
    }})

def GetOrder(request, id):
    return render(request, 'order.html', {'data' : {
        'current_date': date.today(),
        'id': id
    }})

def sendText(request):
    return HttpResponse(request)