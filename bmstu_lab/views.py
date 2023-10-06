from django.shortcuts import render
from bmstu_lab.models import Requests
from bmstu_lab.models import Users
from bmstu_lab.models import Moderators
from bmstu_lab.models import Orders

def GetOrders(request):
    orders_arr = Orders.objects.all()
    input_text = request.GET.get("find")
    print(input_text)
    temp_arr = []
    if input_text is None:
        return render(request, 'orders.html', {'data' : {
                'orders': orders_arr,
                'query': "",
            }})
    for i in orders_arr:
        if input_text is not None:
            if input_text in i.title:
                temp_arr.append(i)
        else:
            return render(request, 'orders.html', {'data' : {
                'orders': orders_arr,
                'query': input_text,
            }})
    return render(request, 'orders.html', {'data' : {
        'orders': temp_arr,
        'query': input_text,
    }})

def GetOrder(request, id):
    orders_arr = Orders.objects.all()
    print(orders_arr    )
    order = next((find for find in orders_arr if find.id== id), None)
    if order:
        print(order.title)
    else:
        print("Not found!")
    
    return render(request, 'order.html', {'data' : {
        'orders': order,
    }})