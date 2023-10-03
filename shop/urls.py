from rest_framework.routers import DefaultRouter
from shop.views import ProductsViewSet, RetailsViewSet, AdminActionUpdateView
from django.urls import path


router = DefaultRouter()

router.register(r'products', ProductsViewSet, basename='products')
router.register(r'retails', RetailsViewSet, basename='retails')

urlpatterns = [
    path('retails/admin_action/<int:pk>/',
         AdminActionUpdateView.as_view(),
         name='admin_action'),

] + router.urls
