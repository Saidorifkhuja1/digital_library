from django.http import FileResponse, Http404
from .serializers import *
from accounts.utils import unhash_token
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework import generics, permissions, status
from rest_framework.exceptions import NotFound
from rest_framework.response import Response
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from rest_framework.pagination import PageNumberPagination




class APIListPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100


class BookListAPIView(generics.ListAPIView):
    queryset = Book.objects.all()
    serializer_class = BookUseSerializer
    pagination_class = APIListPagination



class BookDetailAPIView(generics.RetrieveAPIView):
    serializer_class = BookBaseSerializer
    queryset = Book.objects.all()
    permission_classes = [IsAuthenticated]

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.views += 1
        instance.save()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)








class CreateBookAPIView(generics.CreateAPIView):
    serializer_class = BookSerializer
    permission_classes = [IsAdminUser]

    def perform_create(self, serializer):
        serializer.save()




class UpdateBookAPIView(generics.UpdateAPIView):
    serializer_class = BookSerializer
    permission_classes = [IsAdminUser]

    def get_queryset(self):
        return Book.objects.all()

    def perform_update(self, serializer):
        serializer.save()





class DeleteBookAPIView(generics.DestroyAPIView):
    queryset = Book.objects.all()
    serializer_class = BookBaseSerializer
    permission_classes = [IsAdminUser]

    def perform_destroy(self, instance):
        instance.delete()




class BookGenreList(generics.ListAPIView):
    serializer_class = TypeSerializer
    queryset = Type.objects.all()
    pagination_class = APIListPagination






class BookAuthorList(generics.ListAPIView):
    serializer_class = AuthorSerializer
    queryset = Author.objects.all()
    pagination_class = APIListPagination





class BookGenreSearch(generics.ListAPIView):
    serializer_class = BookUseSerializer
    queryset = Book.objects.all()
    pagination_class = APIListPagination

    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter(
                name='name',
                in_=openapi.IN_QUERY,
                type=openapi.TYPE_STRING,
                required=True,  # Set required to True
                description='Name of the genre'
            ),
        ]
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    def get_queryset(self):
        name = self.request.query_params.get("name", None)
        if name:
            query = self.queryset.filter(genre__name=name)
        else:
            query = self.queryset.none()
        return query







class BookAuthorSearch(generics.ListAPIView):
    serializer_class = BookUseSerializer
    queryset = Book.objects.all()
    pagination_class = APIListPagination

    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter(
                name='name',
                in_=openapi.IN_QUERY,
                type=openapi.TYPE_STRING,
                required=True,
                description='Name of the author'
            ),
        ]
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    def get_queryset(self):
        name = self.request.query_params.get("name", None)
        if name:
            query = self.queryset.filter(author__name=name)
        else:
            query = self.queryset.none()
        return query









class SearchByNameAPIView(generics.ListAPIView):
    queryset = Book.objects.all()
    serializer_class = BookBaseSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter]
    search_fields = ['title']




@method_decorator(csrf_exempt, name='dispatch')
class BookDownloadView(generics.GenericAPIView):
    queryset = Book.objects.all()
    serializer_class = BookBaseSerializer
    lookup_field = 'pk'
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, *args, **kwargs):
        decoded_token = unhash_token(request.headers)
        user_id = decoded_token.get('user_id')
        book = self.get_object()
        book.downloads += 1
        book.save()

        if book.pdf:
            try:
                response = FileResponse(book.pdf.open('rb'), content_type='application/pdf')
                response['Content-Disposition'] = f'attachment; filename="{book.pdf.name}"'
                return response
            except FileNotFoundError:
                raise Http404("File not found")
        else:
            raise Http404("PDF file not available for this book")





class RecommendedBooksView(generics.ListAPIView):
    serializer_class = BookBaseSerializer

    def get_queryset(self):
        return Book.objects.all().order_by('-views', '-downloads')[:10]

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


class UserCartView(generics.ListAPIView):
    serializer_class = CartSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        decoded_token = unhash_token(self.request.headers)
        user_id = decoded_token['user_id']
        queryset = Cart.objects.filter(user_id=user_id)

        if not queryset.exists():
            raise NotFound('Cart not found for this user')

        return queryset




class AddToCardView(generics.CreateAPIView):
    serializer_class = CartSerializer
    permission_classes = [IsAuthenticated]






class RemoveFromCartView(generics.DestroyAPIView):
    serializer_class = CartSerializer
    permission_classes = [IsAuthenticated]

    def delete(self, request, *args, **kwargs):
        decoded_token = unhash_token(request.headers)
        user_id = decoded_token.get['user_id']
        book_id = kwargs.get('book_id')

        try:
            cart_item = Cart.objects.get(user_id=user_id, book_id=book_id)
        except Cart.DoesNotExist:
            raise NotFound("Book not found in cart")

        cart_item.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)






