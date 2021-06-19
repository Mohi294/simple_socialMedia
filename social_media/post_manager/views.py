from django.contrib.auth import authenticate, get_user_model
from django.db.models import F, Func
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.csrf import csrf_exempt
from rest_framework import status
from rest_framework.generics import CreateAPIView, ListAPIView, UpdateAPIView
from rest_framework.parsers import JSONParser
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.serializers import ValidationError
from rest_framework.views import APIView
from user.serializers import SimpleUserSerializer

from post_manager.models import Comment, Post

from .serializers import CommentSerializer, PostSerializer


class CreatePost(CreateAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = PostSerializer

    def post(self, request):
        data = JSONParser().parse(request)
        serializer = PostSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)


class CreateRepost(UpdateAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = PostSerializer

    def update(self, request, post_id):
        instance = Post.objects.filter(id = post_id)
        serializer = self.get_serializer(
            instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)

        
        instance.users.add(self.request.user.id)
        instance.save()
        self.perform_update(serializer)

class AddComment(CreateAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = CommentSerializer

    def post(self, request):
        data = JSONParser().parse(request)
        serializer = CommentSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)


class DeletePost(APIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = PostSerializer

    def delete(self, request, post_id):         
        post = Post.objects.filter(id=post_id, owner=self.request.user)
        serializer = self.get_serializer(
            post, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        post.delete()

        return Response(serializer.data, status=status.HTTP_202_ACCEPTED)


class UndoRepost(UpdateAPIView):    
    permission_classes = (IsAuthenticated,)
    serializer_class = PostSerializer

    def update(self, request, post_id):
        instance = Post.objects.filter(id=post_id)
        serializer = self.get_serializer(
            instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)

        instance.users.remove(self.request.user.id)
        instance.save()
        self.perform_update(serializer)

class ShowAllPosts(APIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = PostSerializer

    def show_posts(self, request):
        posts = Post.objects,filter(owner = self.request.user)
        return self.request.user.Reposts, posts


class DeleteComment(APIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = CommentSerializer

    def delete(self, request, comment_id):
        comment = Comment.objects.filter(id=comment_id, owner=self.request.user)
        serializer = self.get_serializer(
            comment, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        comment.delete()

        return Response(serializer.data, status=status.HTTP_202_ACCEPTED)
