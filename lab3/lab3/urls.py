from api import views
from django.urls import include, path

from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi


from rest_framework import routers
from rest_framework import permissions

router = routers.DefaultRouter()

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
router.register('user', views.UserViewSet, basename='user')

urlpatterns = [
   path('', include(router.urls)),

   # Набор методов для услуг 
   path('api/orders/', views.getOrders),  # GET
   path('api/orders/post/', views.postOrders),  # POST only MANAGER

   path('api/orders/search/', views.searchOrders),  # GET

   path('api/orders/<int:id>/', views.getOrdersDetiled),  # GET
   path('api/orders/<int:id>/put/', views.putOrdersDetiled),  # PUT only MANAGER
   path('api/orders/<int:id>/delete/', views.deleteOrdersDetiled),  # DELETE only MANAGER
   
   # Набор методов для заявок
   path('api/requests/', views.getRequests), # GET only MANAGER
   path('api/requests/post/', views.postRequests), # POST only MANAGER

   path('api/requests/<int:id>/', views.getRequestsDetiled),  # GET
   path('api/requests/<int:id>/put/', views.putRequestsDetiled),  # PUT
   path('api/requests/<int:id>/delete/', views.deleteRequestsDetiled),  # DELETE

   # Swagger
   path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),

   # Авторизация
   path('login',  views.login_view, name='login'),
   path('logout', views.logout_view, name='logout'),
   path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),

   # Дореализовать методы
   # path('api/requests/<int:id>/update_status_user/', views.UpdateStatusUser.as_view()),  # PUT
   # path('api/requests/<int:id>/update_status_admin/', views.UpdateStatusAdmin.as_view()),  # PUT

   # path(r'users/', views.User.as_view()),
   # path(r'requests/<int:id>/', views.RequestDetail.as_view(), name="requests-detail"),
]