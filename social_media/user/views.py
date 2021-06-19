from django.shortcuts import render
from django.http import HttpResponse
from rest_framework import permissions
from rest_framework.generics import CreateAPIView
from django.contrib.auth import get_user_model, authenticate
from user.serializers import UserSerializer
from rest_framework.permissions import IsAuthenticated
from django.views.generic.edit import UpdateView
from rest_framework import generics


class CreateUserView(CreateAPIView):

    model = get_user_model()
    permission_classes = [
        permissions.AllowAny
    ]
    serializer_class = UserSerializer


