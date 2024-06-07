from django.urls import path
from .views import *
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView, TokenVerifyView


urlpatterns = [
    path('register/', UserRegistrationAPIView.as_view()),
    path('profile/update/<int:id>/', UpdateProfileView.as_view()),
    path('profile/delete/<int:id>/', DeleteProfileAPIView.as_view()),
    path('profile/retrieve/', RetrieveProfileView.as_view()),
    path('login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    # path('notifications/', NotificationListCreateAPIView.as_view(), name='notification-list-create'),
    # path('notificationsupdate/<int:pk>/', NotificationDetailAPIView.as_view(), name='notification-detail'),

]

