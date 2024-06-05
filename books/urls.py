from django.urls import path
from .views import *


urlpatterns = [
    path('createbook/', CreateBookAPIView.as_view()),
    path('updatebook/<int:pk>/', UpdateBookAPIView.as_view()),
    path('booklist/', BookListAPIView.as_view()),
    path('bookdetail/<int:pk>/', BookDetailAPIView.as_view()),
    path('booktypesearch/', SearchByTypeAPIView.as_view()),
    path('booknamesearch/', SearchByNameAPIView.as_view()),
    path('deletebook/<int:pk>/', DeleteBookAPIView.as_view()),
    path('savebook/<int:pk>/', SaveBookAPIView.as_view()),
    path('books/download/<int:pk>/', BookDownloadView.as_view(), name='book-download'),
    # path('reviews/', ReviewListCreateAPIView.as_view(), name='review-list-create'),
    # path('reviewsupdate/<int:pk>/', ReviewDetailAPIView.as_view(), name='review-detail'),

]

