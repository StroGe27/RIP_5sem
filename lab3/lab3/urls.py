from django.contrib import admin
from api import views
from django.urls import include, path
from rest_framework import routers

router = routers.DefaultRouter()

urlpatterns = [
    path('', include(router.urls)),
    # услуги
    path(r'orders/', views.OrderList.as_view(), name='orders-list'), 
    path(r'orders/<int:id>/', views.OrderDetail.as_view(), name='orders-detail'),
    # заявки
    path(r'requests/', views.RequestList.as_view(), name='requests-list'),
    path(r'requests/<int:id>/', views.RequestDetail.as_view(), name="requests-detail"),

    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('admin/', admin.site.urls),
]