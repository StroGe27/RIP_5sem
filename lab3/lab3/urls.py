from api import views
from django.urls import path, include

from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi


schema_view = get_schema_view(
   openapi.Info(
      title="Snippets API",
      default_version='v1',
      description="Test description",
      terms_of_service="https://www.google.com/policies/terms/",
      contact=openapi.Contact(email="contact@snippets.local"),
      license=openapi.License(name="BSD License"),
   ),
   public=True,
   permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    # Набор методов для услуг 
    path('api/orders/', views.OrderList.as_view()),  # GET
    path('api/orders/search/', views.OrderSearch),  # GET
    path('api/orders/rangedcost/', views.OrderRangedCost),  # GET
    path('api/orders/<int:id>/', views.OrderDetail.as_view()), # GET | PUT | DELETE


    # Набор методов для заявок
    path('api/requests/', views.RequestList.as_view()), # GET
    path('api/requests/<int:id>/', views.RequestDetail.as_view()), # GET | PUT | DELETE
    # path('api/requests/<int:id>/update_status_user/', views.UpdateStatusUser.as_view()),  # PUT
    # path('api/requests/<int:id>/update_status_admin/', views.UpdateStatusAdmin.as_view()),  # PUT




    # path(r'users/', views.User.as_view()),
    # path(r'requests/<int:id>/', views.RequestDetail.as_view(), name="requests-detail"),

    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
]