from django.urls import path, include
from . import views
from rest_framework.routers import DefaultRouter

router = DefaultRouter()

router.register(r'category', views.CategoryViewSet, basename= 'category')
router.register(r'city', views.CityViewSet, basename= 'city')
router.register(r'books', views.BookViewSet, basename= 'books')

urlpatterns = [
    path('trade/', views.TradeListCreateView.as_view(), name='trade-list'),
    path('trade/<int:pk>/', views.TradeDetailView.as_view(), name='trade-detail'),
    path('trade/<int:pk>/decision/', views.TradeDecisionView.as_view(), name='trade-decision',),
    path('', include(router.urls)),

]
