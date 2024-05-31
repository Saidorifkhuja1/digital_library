from django.urls import path
from .views import *


urlpatterns = [
    path('createbook/', CreateBookAPIView.as_view()),
    path('updatebook/<int:pk>/', UpdateBookAPIView.as_view()),
    path('booklist/', BookListAPIView.as_view()),
    path('bookupdate/<int:pk>/', BookDetailAPIView.as_view()),
    path('booktypesearch/', SearchByTypeAPIView.as_view()),
    path('booknamesearch/', SearchByNameAPIView.as_view()),
    path('deletebook/<int:pk>/', DeleteBookAPIView.as_view()),
    path('reviews/', ReviewListCreateAPIView.as_view(), name='review-list-create'),
    path('reviewsupdate/<int:pk>/', ReviewDetailAPIView.as_view(), name='review-detail'),

]

