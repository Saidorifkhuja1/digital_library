from .models import *

from rest_framework import serializers


class BookSerializer(serializers.ModelSerializer):
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






# class ReviewSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Review
#         fields = ['id', 'book', 'user', 'rating', 'comment', 'timestamp']
#         read_only_fields = ['id', 'user', 'timestamp']









