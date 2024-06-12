from django.urls import path
from .views import *


urlpatterns = [
    path('create_book/', CreateBookAPIView.as_view()),
    path('update_book/<int:pk>/', UpdateBookAPIView.as_view()),
    path('book_list/', BookListAPIView.as_view()),
    path('book_detail/<int:pk>/', BookDetailAPIView.as_view()),
    path('book_type_list/', BookGenreList.as_view()),
    path('book_type_search/', BookGenreSearch.as_view()),
    path('book_author_list/', BookAuthorList.as_view()),
    path('book_author_search/', BookAuthorSearch.as_view()),
    path('book_name_search/', SearchByNameAPIView.as_view()),
    path('dele_tebook/<int:pk>/', DeleteBookAPIView.as_view()),
    path('recomended_books/', RecommendedBooksView.as_view()),
    path('get_cart/', UserCartView.as_view()),
    path('add_cart/', AddToCardView.as_view()),
    path('cart_delete/', RemoveFromCartView.as_view()),
    path('books/download/<int:pk>/', BookDownloadView.as_view(), name='book-download'),

    # path('reviews/', ReviewListCreateAPIView.as_view(), name='review-list-create'),
    # path('reviewsupdate/<int:pk>/', ReviewDetailAPIView.as_view(), name='review-detail'),

]

