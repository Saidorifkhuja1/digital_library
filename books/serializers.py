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




class TypeSerializer(serializers.ModelSerializer):
    books = BookSerializer(many=True, read_only=True, source='book_set')

    class Meta:
        model = Type
        fields = ['id', 'name', 'books']




class AuthorSerializer(serializers.ModelSerializer):
    books = BookSerializer(many=True, read_only=True)

    class Meta:
        model = Author
        fields = ['id', 'name', 'books']




class BookUseSerializer(serializers.ModelSerializer):
    author = AuthorSerializer()
    genre = TypeSerializer()
    class Meta:
        model = Book
        fields = ['id', 'title', 'author', 'genre', 'description', 'cover_image', 'views', 'downloads']



class BookBaseSerializer(serializers.ModelSerializer):
    author = AuthorSerializer()
    genre = TypeSerializer()

    class Meta:
        model = Book
        fields = '__all__'
        read_only_fields = ['uploaded_by', 'views', 'downloads']






class CartUseSerializer(serializers.ModelSerializer):
    book = BookUseSerializer()

    class Meta:
        model = Cart
        fields = '__all__'


class CartSerializer(serializers.ModelSerializer):

    class Meta:
        model = Cart
        fields = ['book', 'added_at']




class BookInCartCheckSerializer(serializers.Serializer):
    book_id = serializers.IntegerField()
