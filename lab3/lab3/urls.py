from django.contrib import admin
from api import views
from django.urls import include, path
from rest_framework import routers

router = routers.DefaultRouter()

urlpatterns = [
    path('', include(router.urls)),
    path(r'orders/', views.OrderList.as_view(), name='orders-list'),
    path(r'orders/<int:pk>/', views.OrderDetail.as_view(), name='orders-detail'),
    path(r'orders/<int:pk>/put/', views.put_detail, name='orders-put'),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('admin/', admin.site.urls),
]