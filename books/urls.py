from django.urls import path, include
from . import views
from rest_framework.routers import DefaultRouter

router = DefaultRouter()

router.register(r'category', views.CategoryViewSet, basename= 'category')
router.register(r'city', views.CityViewSet, basename= 'city')
router.register(r'books', views.BookViewSet, basename= 'books')
router.register(r'trade', views.TradeViewSet, basename= 'trade')

urlpatterns = [
    path('', include(router.urls)),
]
