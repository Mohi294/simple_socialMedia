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

from .serializers import CommentSerializer, PostSerializer, RepostSerializer


class CreatePost(CreateAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = PostSerializer

    def perform_create(self, serializer):        
        serializer.save(owner = self.request.user)


class CreateRepost(UpdateAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = RepostSerializer
    lookup_url = 'pk'

    def get_queryset(self):
        pk = int(self.kwargs.get(self.lookup_url))
        post = get_object_or_404(Post, pk=pk)
        
        return post

    def update(self, request, pk):
        posts = Post.objects.filter(id=pk)
        for post in posts:            
            post.users.add(self.request.user)
            post.save()
        serializer = RepostSerializer(posts, many = True)
        return Response(serializer.data)

    

class AddComment(CreateAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = CommentSerializer

    def perform_create(self, serializer):
        serializer.save(comment_by=self.request.user)


class DeletePost(APIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = PostSerializer

    def delete(self, request, post_id):         
        post = Post.objects.filter(id=post_id, owner=self.request.user)
        post.delete()

        return Response(status=status.HTTP_204_NO_CONTENT)


class UndoRepost(UpdateAPIView):    
    permission_classes = (IsAuthenticated,)
    serializer_class = RepostSerializer
    

    def get_queryset(self):
        post = Post.objects.filter(owner = self.request.user)

        return post

    def update(self, request, post_id):
        posts = Post.objects.filter(id=post_id)
        for instance in posts:
            instance.users.remove(self.request.user.id)
            instance.save()
        serializer = RepostSerializer(posts, many = True)
        return Response(serializer.data)

class ShowAllPosts(ListAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = RepostSerializer
    
    def get_queryset(self):
        queryset = self.request.user.Reposts
        queryset1 = Post.objects.filter(owner=self.request.user)
        serializer = self.serializer_class(queryset, many=True)
        serializer1 = self.serializer_class(queryset1, many=True)
        querylist = chain(serializer.data, serializer1.data)
        return querylist


class DeleteComment(APIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = CommentSerializer

    def delete(self, request, comment_id):
        comment = Comment.objects.filter(
            id=comment_id, comment_by=self.request.user)
        comment.delete()

        return Response(status=status.HTTP_204_NO_CONTENT)

class PostComments(ListAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = CommentSerializer
    lookup_url = 'pk'


    def get_queryset(self):
        pk = int(self.kwargs.get(self.lookup_url))
        comments = Comment.objects.filter(post__id = pk)
        # serializer = CommentSerializer(comments)
        return comments
