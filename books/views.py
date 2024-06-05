from django.http import FileResponse, Http404
from .serializers import *
from accounts.utils import unhash_token
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter
from rest_framework.permissions import IsAuthenticated
from rest_framework import generics
from rest_framework.exceptions import AuthenticationFailed


class BookListAPIView(generics.ListAPIView):
    queryset = Book.objects.all()
    serializer_class = BookBaseSerializer



class BookDetailAPIView(generics.RetrieveAPIView):
    serializer_class = BookBaseSerializer
    queryset = Book.objects.all()




class CreateBookAPIView(generics.CreateAPIView):
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        decoded_token = unhash_token(self.request.headers)
        user_id = decoded_token.get('user_id')
        serializer.save(uploaded_by=user_id)



class UpdateBookAPIView(generics.UpdateAPIView):
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        try:
            decoded_token = unhash_token(self.request.headers)
            user_id = decoded_token.get('user_id')
            return Book.objects.filter(uploaded_by=user_id)
        except AuthenticationFailed as e:
            return Book.objects.none()



class DeleteBookAPIView(generics.DestroyAPIView):
    queryset = Book.objects.all()
    serializer_class = BookBaseSerializer
    permission_classes = [IsAuthenticated]


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




class BookDownloadView(generics.GenericAPIView):
    queryset = Book.objects.all()
    serializer_class = BookBaseSerializer
    lookup_field = 'pk'
    def get(self, request, *args, **kwargs):
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






