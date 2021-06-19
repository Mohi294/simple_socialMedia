from itertools import chain

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

    def perform_create(self, serializer):        
        serializer.save(owner = self.request.user)


class CreateRepost(UpdateAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = PostSerializer
    lookup_url = 'pk'

    def get_queryset(self):
        pk = int(self.kwargs.get(self.lookup_url))
        post = get_object_or_404(Post, pk=pk)
        
        return post

    def update(self, request, pk):
        data = JSONParser().parse(request)
        post = Post.objects.filter(id=pk)
        serializer = PostSerializer(post, data=data)
        repost = serializer.save()

        return repost

    

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

class ShowAllPosts(ListAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = PostSerializer
    
    def get_queryset(self):
        queryset = self.request.user.Reposts
        queryset1 = Post.objects.filter(owner=self.request.user)
        serializer = self.serializer_class(queryset, many=True)
        serializer1 = self.serializer_class(queryset1, many=True)
        querylist = [serializer, serializer1]
        return queryset


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
