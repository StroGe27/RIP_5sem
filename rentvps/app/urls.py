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
    path('api/tariffs/<int:tariff_id>/add_to_virtual/', add_tariff_to_virtual),  # POST

    # Набор методов для заявок
    path('api/virtuals/search/', search_virtuals),  # GET
    path('api/virtuals/<int:virtual_id>/', get_virtual_by_id),  # GET
    path('api/virtuals/<int:virtual_id>/update/', update_virtual),  # PUT
    path('api/virtuals/<int:virtual_id>/update_clinical_trial/', update_virtual_clinical_trial),  # PUT
    path('api/virtuals/<int:virtual_id>/update_status_user/', update_status_user),  # PUT
    path('api/virtuals/<int:virtual_id>/update_status_admin/', update_status_admin),  # PUT
    path('api/virtuals/<int:virtual_id>/delete/', delete_virtual),  # DELETE

    # м-м
    path('api/virtuals/<int:virtual_id>/update_tariff/<int:tariff_id>/', update_tariff_in_virtual),  # PUT
    path('api/virtuals/<int:virtual_id>/delete_tariff/<int:tariff_id>/', delete_tariff_from_virtual),  # DELETE

    # Набор методов для аутентификации и авторизации
    path("api/register/", register),
    path("api/login/", login),
    path("api/check/", check),
    path("api/logout/", logout)
]
