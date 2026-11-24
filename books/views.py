from django.shortcuts import render
from rest_framework import generics
from rest_framework.viewsets import ModelViewSet
from .serializers import *
from .models import *

from .permissions import IsBookOwnerOrReadOnly

class CategoryViewSet(ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    
class CityViewSet(ModelViewSet):
    queryset = City.objects.all()
    serializer_class = CitySerializer


class BookViewSet(ModelViewSet):
    queryset = Books.objects.all().order_by('-id')
    serializer_class = BooksSerializer
    permission_classes = [IsBookOwnerOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def destroy(self, request, *args, **kwargs):
        book = self.get_object()

        if Trade.objects.filter(book=book, status='PENDING').exists():
            return Response({'detail': 'На книгу есть заявка, которая ждёт ответа.'},
                status=status.HTTP_409_CONFLICT,
            )

        self.perform_destroy(book)
        return Response(status=status.HTTP_204_NO_CONTENT)

class TradeViewSet(ModelViewSet):
    queryset = Trade.objects.all()
    serializer_class = TradeSerializer
    

