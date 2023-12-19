from api import views
from django.urls import include, path

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