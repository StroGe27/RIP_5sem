from django.urls import path
from .views import *

urlpatterns = [
    # Набор методов для услуг
    path('api/tariffs/search/', search_tariffs),  # GET
    path('api/tariffs/<int:tariff_id>/', get_tariff_by_id),  # GET
    path('api/tariffs/<int:tariff_id>/image/', get_tariff_image),  # GET
    path('api/tariffs/<int:tariff_id>/update/', update_tariff),  # PUT
    path('api/tariffs/<int:tariff_id>/update_image/', update_tariff_image),  # PUT
    path('api/tariffs/<int:tariff_id>/delete/', delete_tariff),  # DELETE
    path('api/tariffs/create/', create_tariff),  # POST
    path('api/tariffs/<int:tariff_id>/add_to_order/', add_tariff_to_order),  # POST

    # Набор методов для заявок
    path('api/orders/search/', search_orders),  # GET
    path('api/orders/<int:order_id>/', get_order_by_id),  # GET
    path('api/orders/<int:order_id>/update/', update_order),  # PUT
    path('api/orders/<int:order_id>/update_clinical_trial/', update_order_clinical_trial),  # PUT
    path('api/orders/<int:order_id>/update_status_user/', update_status_user),  # PUT
    path('api/orders/<int:order_id>/update_status_admin/', update_status_admin),  # PUT
    path('api/orders/<int:order_id>/delete/', delete_order),  # DELETE

    # м-м
    path('api/orders/<int:order_id>/tariffs/<int:tariff_id>/', get_tariff_in_order),  # GET
    path('api/orders/<int:order_id>/update_tariff/<int:tariff_id>/', update_tariff_in_order),  # PUT
    path('api/orders/<int:order_id>/delete_tariff/<int:tariff_id>/', delete_tariff_from_order),  # DELETE

    # Набор методов для аутентификации и авторизации
    path("api/register/", register),
    path("api/login/", login),
    path("api/check/", check),
    path("api/logout/", logout)
]
