from .models import *
from drf_extra_fields.fields import Base64ImageField
from rest_framework import serializers


class BookSerializer(serializers.ModelSerializer):
    photo = Base64ImageField(allow_null=True, required=False)
    class Meta:
        model = Book
        fields = '__all__'
        read_only_fields = ['title', 'author']

    def create(self, validated_data):
        request = self.context.get('request')
        user = request.user
        book = Book.objects.create(**validated_data)
        book.uploaded_by.add(user)
        return book


class BookBaseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = '__all__'
        read_only_fields = ['uploaded_by', 'read_by']


class CartSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cart
        fields = ['user', 'book', 'added_at']

class AuthorSerializer(serializers.ModelSerializer):
    books = BookSerializer(many=True, read_only=True)

    class Meta:
        model = Author
        fields = ['id', 'name', 'books']



class TypeSerializer(serializers.ModelSerializer):
    books = BookSerializer(many=True, read_only=True)

    class Meta:
        model = Type
        fields = ['id', 'name', 'books']





