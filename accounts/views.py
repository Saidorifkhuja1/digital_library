from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.response import Response
from .serializers import *
from rest_framework import generics, permissions, status
from rest_framework.permissions import IsAuthenticated
from .utils import unhash_token


class UserRegistrationAPIView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserRegistrationSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        refresh = RefreshToken.for_user(user)
        access_token = refresh.access_token
        token_data = {
            "refresh": str(refresh),
            "access": str(access_token),
        }
        return Response(token_data, status=status.HTTP_201_CREATED)


class UpdateProfileView(generics.UpdateAPIView):
    serializer_class = UserUpdateSerializer
    permission_classes = [IsAuthenticated]
    lookup_field = "id"

    def get_queryset(self):
        decoded_token = unhash_token(self.request.headers)
        user_id = decoded_token.get('user_id')
        return User.objects.filter(id=user_id)


class RetrieveProfileView(generics.RetrieveAPIView):
    serializer_class = UserProfileSerializer
    permission_classes = [IsAuthenticated]
    lookup_field = 'id'

    def get_queryset(self):
        decoded_token = unhash_token(self.request.headers)
        user_id = decoded_token.get('user_id')
        return User.objects.filter(id=user_id)


class DeleteProfileAPIView(generics.DestroyAPIView):
    serializer_class = UserProfileSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        decoded_token = unhash_token(self.request.headers)
        user_id = decoded_token.get('user_id')
        return User.objects.filter(id=user_id)







