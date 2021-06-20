import json
import string
from random import randint

import factory
from django.conf import settings
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.forms.models import model_to_dict
from django.test import TestCase
from django.urls import reverse
from factory import Iterator, LazyAttribute, SubFactory, lazy_attribute
from factory.django import DjangoModelFactory, FileField
from factory.fuzzy import FuzzyInteger, FuzzyText
from faker import Factory as FakerFactory
from pytz import timezone
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase

from .models import Comment, Post
from .serializers import CommentSerializer, PostSerializer

faker = FakerFactory.create()


class UserFactory(DjangoModelFactory):
    class Meta:
        model = User

    name = faker.name()
    email = faker.email()

class PostFactory(DjangoModelFactory):
    class Meta:
        model = Post

    owner = SubFactory(UserFactory)
    created_at = LazyAttribute(lambda x: faker.date_time_between(start_date="-1y", end_date="now",
                                                                 tzinfo=timezone(settings.TIME_ZONE)))
    text = LazyAttribute(lambda x: faker.paragraph(
        nb_sentences=3, variable_nb_sentences=True))


class CommentFactory(DjangoModelFactory):
    class Meta:
        model = Comment

    comment_by = SubFactory(UserFactory)
    post = SubFactory(PostFactory)
    comment = LazyAttribute(lambda x: faker.paragraph(
        nb_sentences=3, variable_nb_sentences=True))


class TestCasePost(TestCase):

    def test_create(self):
        """
        Test the creation of a Post model using a factory
        """
        post = PostFactory.create()
        self.assertEqual(Post.objects.count(), 1)

    def test_create_batch(self):
        """
        Test the creation of 5 Post models using a factory
        """
        posts = PostFactory.create_batch(5)
        self.assertEqual(Post.objects.count(), 5)
        self.assertEqual(len(posts), 5)

    def test_attribute_count(self):
        """
        Test that all attributes of Post server are counted. It will count the primary key and all editable attributes.
        This test should break if a new attribute is added.
        """
        post = PostFactory.create()
        post_dict = model_to_dict(post)
        self.assertEqual(len(post_dict.keys()), 4)

    def test_attribute_content(self):
        """
        Test that all attributes of Post server have content. This test will break if an attributes name is changed.
        """
        post = PostFactory.create()
        self.assertIsNotNone(post.id)
        self.assertIsNotNone(post.owner)
        self.assertIsNotNone(post.created_at)
        self.assertIsNotNone(post.text)


class TestCaseComment(TestCase):

    def test_create(self):
        """
        Test the creation of a Comment model using a factory
        """
        comment = CommentFactory.create()
        self.assertEqual(Comment.objects.count(), 1)

    def test_create_batch(self):
        """
        Test the creation of 5 Comment models using a factory
        """
        comments = CommentFactory.create_batch(5)
        self.assertEqual(Comment.objects.count(), 5)
        self.assertEqual(len(comments), 5)

    def test_attribute_count(self):
        """
        Test that all attributes of Comment server are counted. It will count the primary key and all editable attributes.
        This test should break if a new attribute is added.
        """
        comment = CommentFactory.create()
        comment_dict = model_to_dict(comment)
        self.assertEqual(len(comment_dict.keys()), 4)

    def test_attribute_content(self):
        """
        Test that all attributes of Comment server have content. This test will break if an attributes name is changed.
        """
        comment = CommentFactory.create()
        self.assertIsNotNone(comment.id)
        self.assertIsNotNone(comment.comment_by)
        self.assertIsNotNone(comment.post)
        self.assertIsNotNone(comment.comment)
