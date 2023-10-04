from django.shortcuts import render
from bmstu_lab.models import Book
from bmstu_lab.models import Requests
from bmstu_lab.models import Users
from bmstu_lab.models import Moderators
from bmstu_lab.models import Orders
info_arr = [
    {'processor': 'Intel Xeon E-2236', "Ghz": 3.5, "cores": 6, "ram": 32},
    {'processor': 'Intel Xeon E-2386G', "Ghz": 3.4, "cores": 6, "ram": 32},
    {'processor': 'Intel Xeon E-2236', "Ghz": 3.4, "cores": 6, "ram": 32},
    {'processor': 'Intel Xeon W-2255', "Ghz": 3.7, "cores": 10, "ram": 128},
    {'processor': 'Intel Xeon W-2255', "Ghz": 3.7, "cores": 10, "ram": 256},
    {'processor': 'Intel Xeon Gold 6354', "Ghz": 3, "cores": 18, "ram": 256},
    {'processor': 'Intel Xeon Gold 6354', "Ghz": 3, "cores": 18, "ram": 254},
]
orders_arr = [
    {'title': 'EL11-SSD-10GE', 'id': 1, 'src': '/images/1.jpg', 'definition': info_arr[0]},
    {'title': 'EL42-NVMe', 'id': 2, 'src': 'images/2.jpg', 'definition': info_arr[1]},
    {'title': 'EL13-SSD', 'id': 3, 'src': 'images/3.jpg', 'definition': info_arr[2]},
    {'title': 'BL22-NVMe', 'id': 4, 'src': 'images/4.jpg', 'definition': info_arr[3]},
    {'title': 'BL21R-NVMe', 'id': 5, 'src': 'images/5.jpg', 'definition': info_arr[4]},
    {'title': 'PL25-NVMe', 'id': 6, 'src': 'images/6.jpg', 'definition': info_arr[5]},
    {'title': 'PL25-NVMe', 'id': 7, 'src': 'images/6.jpg', 'definition': info_arr[6]},
]

def GetOrderss(request):
    print(Orders.objects.all())
    return render(request, 'orders.html', {'data' : {
                # 'orders': orders_arr,
                'orders': Orders.objects.all(),
                # 'query': "",
            }})


def GetOrders(request):
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
            if input_text in i['title']:
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
    order = next((find for find in orders_arr if find["id"] == id), None)
    if order:
        print(order["title"])
    else:
        print("Not found!")
    return render(request, 'order.html', {'data' : {
        'orders': order,
    }})