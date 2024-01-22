from django.contrib import admin
from .models import *

admin.site.register(Tariff)
admin.site.register(TariffOrder)
admin.site.register(Order)
admin.site.register(CustomUser)

