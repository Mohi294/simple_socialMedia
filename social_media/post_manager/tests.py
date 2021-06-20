import json
import string
from random import randint
import factory

from django.conf import settings
from django.contrib.auth.models import User
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
