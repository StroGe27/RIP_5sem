from django.db import models, migrations
from django.contrib.auth.models import User

# Create your models here.
class Server(models.Model):
    processor = models.CharField(max_length=100)
    Ghz = models.FloatField()
    cores = models.IntegerField()
    ram = models.IntegerField()

class Order(models.Model):
    title = models.CharField(max_length=100)
    id = models.IntegerField(primary_key=True)
    src = models.CharField(max_length=100)
    definition = models.ManyToManyField(Server)

# info_arr = [
#     {'processor': 'Intel Xeon E-2236', "Ghz": 3.5, "cores": 6, "ram": 32},
#     {'processor': 'Intel Xeon E-2386G', "Ghz": 3.4, "cores": 6, "ram": 32},
#     {'processor': 'Intel Xeon E-2236', "Ghz": 3.4, "cores": 6, "ram": 32},
#     {'processor': 'Intel Xeon W-2255', "Ghz": 3.7, "cores": 10, "ram": 128},
#     {'processor': 'Intel Xeon W-2255', "Ghz": 3.7, "cores": 10, "ram": 256},
#     {'processor': 'Intel Xeon Gold 6354', "Ghz": 3, "cores": 18, "ram": 256},
# ]
# orders_arr = [
#     {'title': 'EL11-SSD-10GE', 'id': 1, 'src': '/images/1.jpg', 'definition': info_arr[0]},
#     {'title': 'EL42-NVMe', 'id': 2, 'src': 'images/2.jpg', 'definition': info_arr[1]},
#     {'title': 'EL13-SSD', 'id': 3, 'src': 'images/3.jpg', 'definition': info_arr[2]},
#     {'title': 'BL22-NVMe', 'id': 4, 'src': 'images/4.jpg', 'definition': info_arr[3]},
#     {'title': 'BL21R-NVMe', 'id': 5, 'src': 'images/5.jpg', 'definition': info_arr[4]},
#     {'title': 'PL25-NVMe', 'id': 6, 'src': 'images/6.jpg', 'definition': info_arr[5]},
# ]