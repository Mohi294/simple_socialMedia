from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
from rest_framework import serializers, status
from user.serializers import SimpleUserSerializer

from post_manager.models import Comment, Post


class PostSerializer(serializers.ModelSerializer):
    owner = SimpleUserSerializer(many=False, read_only=True)


    class Meta:
        model = Post
        fields = '__all__'

    def create(self, validated_data):
        return Post.objects.create(**validated_data)


class CommentSerializer(serializers.ModelSerializer):
    owner = SimpleUserSerializer(many=False, read_only=True)

    class Meta:
        model = Comment
        fields = '__all__'

    def create(self, validated_data):
        return Comment.objects.create(**validated_data)
