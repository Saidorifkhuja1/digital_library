from .models import *
from .permissions import IsOwnerOrReadOnly
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
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        try:
            decoded_token = unhash_token(self.request.headers)
            user_id = decoded_token.get('user_id')
            return Book.objects.filter(uploaded_by=user_id)
        except AuthenticationFailed as e:
            return Book.objects.none()



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
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        decoded_token = unhash_token(self.request.headers)
        user_id = decoded_token.get('user_id')
        genre_name = self.request.query_params.get('genre')
        if genre_name:
            try:
                genre = Type.objects.get(name=genre_name)
                return Book.objects.filter(genre=genre, uploaded_by=user_id)
            except Type.DoesNotExist:
                return Book.objects.none()
        return Book.objects.filter(uploaded_by=user_id)


class SearchByNameAPIView(generics.ListAPIView):
    queryset = Book.objects.all()
    serializer_class = BookBaseSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, SearchFilter]
    search_fields = ['title']


class ReviewListCreateAPIView(generics.ListCreateAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        decoded_token = unhash_token(self.request.headers)
        user_id = decoded_token.get('user_id')
        serializer.save(user_id=user_id)


class ReviewDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = [IsOwnerOrReadOnly]

















# class BookListAPIView(generics.ListAPIView):
#     queryset = Book.objects.all()
#     serializer_class = BookBaseSerializer
#
#
# class BookDetailAPIView(generics.RetrieveAPIView):
#     queryset = Book.objects.all()
#     serializer_class = BookBaseSerializer
#     permission_classes = [IsAuthenticated]
#
#     def get_queryset(self):
#         user = self.request.user
#         return Book.objects.filter(uploaded_by=user)
#
#
# class CreateBookAPIView(generics.CreateAPIView):
#     queryset = Book.objects.all()
#     serializer_class = BookSerializer
#     permission_classes = [IsAuthenticated]
#
#     def perform_cretae(self, serializer):
#         serializer.save(uploaded_by=[self.request.user])
#
#
# class UpdateBookAPIView(generics.UpdateAPIView):
#     queryset = Book.objects.all()
#     serializer_class = BookSerializer
#     permission_classes = [IsAuthenticated]
#
#     def get_queryset(self):
#         user = self.request.user
#         return Book.objects.filter(uploaded_by=user)
#
# class DeleteBookAPIView(generics.DestroyAPIView):
#     queryset = Book.objects.all()
#     serializer_class = BookBaseSerializer
#     permission_classes = [IsAuthenticated]
#
#
# class SearchByTypeAPIView(generics.ListAPIView):
#     queryset = Book.objects.all()
#     serializer_class = BookBaseSerializer
#     permission_classes = [IsAuthenticated]
#
#     def get_queryset(self):
#         genre_name = self.request.query_params.get('genre')
#         if genre_name:
#             try:
#                 genre = Type.objects.get(name=genre_name)
#                 return Book.objects.filter(genre=genre)
#             except Type.DoesNotExist:
#                 return Book.objects.none()
#         return Book.objects.all()
#
#
#
# class SearchByNameAPIView(generics.ListAPIView):
#     queryset = Book.objects.all()
#     serializer_class = BookBaseSerializer
#     permission_classes = [IsAuthenticated]
#     filter_backends = [DjangoFilterBackend, SearchFilter]
#     search_fields = ['title']
#
#
#
# class ReviewListCreateAPIView(generics.ListCreateAPIView):
#     queryset = Review.objects.all()
#     serializer_class = ReviewSerializer
#     permission_classes = [permissions.IsAuthenticatedOrReadOnly]
#
#     def perform_create(self, serializer):
#         serializer.save(user=self.request.user)
#
# class ReviewDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
#     queryset = Review.objects.all()
#     serializer_class = ReviewSerializer
#     permission_classes = [IsOwnerOrReadOnly]