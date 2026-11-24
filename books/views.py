from django.db.models import Q
from rest_framework import generics, status
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from .serializers import *
from .models import *

from .permissions import IsBookOwnerOrReadOnly
from django_filters.rest_framework import DjangoFilterBackend

class CategoryViewSet(ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAdminUser]
    
class CityViewSet(ModelViewSet):
    queryset = City.objects.all()
    serializer_class = CitySerializer
    permission_classes = [IsAdminUser]



class BookViewSet(ModelViewSet):
    queryset = Books.objects.all().order_by('-id')
    serializer_class = BooksSerializer
    permission_classes = [IsBookOwnerOrReadOnly]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['category', 'city', 'book_conditions']

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


class TradeListCreateView(generics.ListCreateAPIView):
    serializer_class = TradeSerializer

    def get_queryset(self):
        user_id = self.request.user.id
        return Trade.objects.filter(
            Q(getter_id=user_id) | Q(book__user_id=user_id)
        ).order_by('-id')

    def perform_create(self, serializer):
        serializer.save(getter=self.request.user)


class TradeDetailView(generics.RetrieveAPIView):
    serializer_class = TradeSerializer

    def get_queryset(self):
        user_id = self.request.user.id
        return Trade.objects.filter(
            Q(getter_id=user_id) | Q(book__user_id=user_id)
        )


class TradeDecisionView(generics.GenericAPIView):
    serializer_class = TradeDecisionSerializer

    def get_queryset(self):
        return Trade.objects.filter(book__user_id=self.request.user.id)

    def post(self, request, pk):
        trade = self.get_object()

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        new_status = serializer.validated_data['status']

        updated = Trade.objects.filter(pk=trade.pk, status='PENDING').update(
            status=new_status
        )

        if not updated:
            return Response(
                {'detail': 'На эту заявку уже ответили.'},
                status=status.HTTP_409_CONFLICT,
            )

        return Response({'status': new_status})

