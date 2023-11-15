from django.contrib import admin
from api import views
from django.urls import include, path
from rest_framework import routers

router = routers.DefaultRouter()

urlpatterns = [
    path('', include(router.urls)),

    path(r'orders/', views.OrderList.as_view(), name='orders-list'), # вывод всех услуг
    path(r'orders/<int:id>/', views.OrderDetail.as_view(), name='orders-detail'), # Отобразить информацию об услуге

    path(r'requests/', views.RequestList.as_view(), name='requests-list'), # вывод всех услуг
    path(r'requests/<int:id>/', views.RequestDetail.as_view(), name="requests-detail"), # вывод заявок с фильтром

    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('admin/', admin.site.urls),
]