from rest_framework import serializers
from .models import *

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'

class CitySerializer(serializers.ModelSerializer):
    class Meta:
        model = City
        fields = '__all__' 

class BooksSerializer(serializers.ModelSerializer):
    class Meta:
        model = Books
        fields = '__all__'
        read_only_fields = ('user',)
        
class TradeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Trade
        fields = ('id', 'book', 'getter', 'status', 'created_at')
        read_only_fields = ('getter', 'status', 'created_at')

    def validate_book(self, book):
        if book.user_id == self.context['request'].user.id:
            raise serializers.ValidationError('Нельзя отправить заявку на свою книгу.')
        return book

class TradeDecisionSerializer(serializers.Serializer):
    status = serializers.ChoiceField(choices=['ACCEPTED', 'CANCEL'])