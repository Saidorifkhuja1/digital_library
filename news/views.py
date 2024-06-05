from django.shortcuts import render
from rest_framework import generics, permissions
from rest_framework.exceptions import AuthenticationFailed, PermissionDenied

from accounts.utils import unhash_token
from .models import *
from .serializers import *

class CreateNewsAPIView(generics.CreateAPIView):
    queryset = News.objects.all()
    serializer_class = NewsSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        decoded_token = unhash_token(self.request.headers)
        user_id = decoded_token.get('user_id')
        if not user_id:
            raise AuthenticationFailed("User ID not found")
        serializer.save(author_id=user_id)

class NewsListAPIView(generics.ListAPIView):
    queryset = News.objects.all()
    serializer_class = NewsSerializer

class NewsUpdateAPIView(generics.UpdateAPIView):
    queryset = News.objects.all()
    serializer_class = NewsSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        print(self.request.headers)
        if getattr(self, 'swagger_fake_view', False):
            return News.objects.none()
        decoded_token = unhash_token(self.request.headers)
        user_id = decoded_token.get('user_id')
        if not user_id:
            raise AuthenticationFailed("User ID not found")
        return News.objects.filter(author_id=user_id)
    def perform_update(self, serializer):
        instance = self.get_object()
        decoded_token = unhash_token(self.request.headers)
        user_id = decoded_token.get('user_id')
        if instance.author_id != user_id:
            raise PermissionDenied("You do not have permission to edit this news article")
        serializer.save()


class NewsDetailAPIView(generics.RetrieveAPIView):
    queryset = News.objects.all()
    serializer_class = NewsSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        obj = super().get_object()
        decoded_token = unhash_token(self.request.headers)
        user_id = decoded_token.get('user_id')
        if obj.author_id != user_id:
            raise PermissionDenied("You do not have permission to access this news article")
        return obj




class NewsDeleteAPIView(generics.DestroyAPIView):
    queryset = News.objects.all()
    serializer_class = NewsSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        obj = super().get_object()
        decoded_token = unhash_token(self.request.headers)
        user_id = decoded_token.get('user_id')
        if obj.author_id != user_id:
            raise PermissionDenied("You do not have permission to delete this news article")
        return obj



