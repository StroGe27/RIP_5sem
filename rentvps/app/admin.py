from django.contrib import admin
from .models import *

admin.site.register(Tariff)
admin.site.register(TariffVirtual)
admin.site.register(Virtual)
admin.site.register(CustomUser)

