from django.http import FileResponse, Http404
from .serializers import *
from accounts.utils import unhash_token
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework import generics, permissions
from rest_framework.exceptions import AuthenticationFailed, PermissionDenied
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt


class BookListAPIView(generics.ListAPIView):
    queryset = Book.objects.all()
    serializer_class = BookBaseSerializer




class BookDetailAPIView(generics.RetrieveAPIView):
    serializer_class = BookBaseSerializer
    queryset = Book.objects.all()
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.is_authenticated:
            return self.queryset.filter(author=user)
        else:
            return self.queryset.none()




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


class SearchByTypeAPIView(generics.ListAPIView):
    queryset = Book.objects.all()
    serializer_class = BookBaseSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter]
    search_fields = ['type']




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
        if book.pdf:
            try:
                response = FileResponse(book.pdf.open('rb'), content_type='application/pdf')
                response['Content-Disposition'] = f'attachment; filename="{book.pdf.name}"'
                return response
            except FileNotFoundError:
                raise Http404("File not found")
        else:
            raise Http404("PDF file not available for this book")





class SaveBookAPIView(APIView):
    def post(self, request, *args, **kwargs):
        try:
            decoded_token = unhash_token(request.headers)
            user_id = decoded_token.get('user_id')
            if not user_id:
                raise AuthenticationFailed("User ID not found")

            book_id = request.data.get('book_id')
            if not book_id:
                return Response({'error': 'Book ID is required'}, status=status.HTTP_400_BAD_REQUEST)

            book = Book.objects.filter(id=book_id).first()
            if not book:
                return Response({'error': 'Book not found'}, status=status.HTTP_404_NOT_FOUND)

            user = request.user
            user.saved_books.add(book)
            return Response({'message': 'Book saved successfully'}, status=status.HTTP_200_OK)

        except AuthenticationFailed as e:
            return Response({'error': str(e)}, status=status.HTTP_401_UNAUTHORIZED)
