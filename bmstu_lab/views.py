from datetime import date
from django.shortcuts import render
from django.http import HttpResponse
info_arr = [
    {'processor': 'Intel Xeon E-2236', "Ghz": 3.5, "cores": 6, "ram": 32},
    {'processor': 'Intel Xeon E-2386G', "Ghz": 3.4, "cores": 6, "ram": 32},
    {'processor': 'Intel Xeon E-2236', "Ghz": 3.4, "cores": 6, "ram": 32},
    {'processor': 'Intel Xeon W-2255', "Ghz": 3.7, "cores": 10, "ram": 128},
    {'processor': 'Intel Xeon W-2255', "Ghz": 3.7, "cores": 10, "ram": 256},
    {'processor': 'Intel Xeon Gold 6354', "Ghz": 3, "cores": 18, "ram": 256},
]
orders_arr = [
    {'title': 'EL11-SSD-10GE', 'id': 1, 'src': '/images/1.jpg', 'definition': info_arr[0]},
    {'title': 'EL42-NVMe', 'id': 2, 'src': 'images/2.jpg', 'definition': info_arr[1]},
    {'title': 'EL13-SSD', 'id': 3, 'src': 'images/3.jpg', 'definition': info_arr[2]},
    {'title': 'BL22-NVMe', 'id': 4, 'src': 'images/1.jpg', 'definition': info_arr[3]},
    {'title': 'BL21R-NVMe', 'id': 5, 'src': 'images/2.jpg', 'definition': info_arr[4]},
    {'title': 'PL25-NVMe', 'id': 6, 'src': 'images/3.jpg', 'definition': info_arr[5]},
]

def GetOrders(request):
    input_text = request.GET.get("sub")
    print(input_text)
    temp_arr = []
    for i in orders_arr:
        if input_text is not None:
            if input_text in i['title']:
                temp_arr.append(i)
        else:
            return render(request, 'orders.html', {'data' : {
                'orders': orders_arr,
            }})
    return render(request, 'orders.html', {'data' : {
        'orders': temp_arr,
    }})

def GetOrder(request, id):
    order = next((sub for sub in orders_arr if sub["id"] == id), None)
    if order:
        print(order["title"])
    else:
        print("Not found!")
    return render(request, 'order.html', {'data' : {
        'orders': order,
    }})

# def sendText(request):
#     input_text = request.GET.get("text")
#     temp_arr = []
#     for i in orders_arr:
#         if input_text in i['title']:
#             temp_arr.append(i)
#     if len(temp_arr) == 0:
#         return render(request, 'orders.html', {'data' : {
#             'current_date': date.today(),
#             'orders': [{'title': 'Тут ничего нет', 'id': 1, 'src': '/images/1.jpg', 'definition': 'first'}],
#         }})
#     return render(request, 'orders.html', {'data' : {
#         'current_date': date.today(),   
#         'orders': temp_arr,
#     }})        
