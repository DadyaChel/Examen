from django.shortcuts import render
from rest_framework import viewsets
from rest_framework import mixins
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import status

from .serializers import AuthorRegisterSerializer
from .models import Author, User

from django.shortcuts import render
from rest_framework import viewsets, mixins
from rest_framework.permissions import AllowAny

from .models import Author
from .serializers import AuthorRegisterSerializer


class AuthorViewSet(mixins.CreateModelMixin, viewsets.GenericViewSet):
    queryset = Author.objects.all()
    serializer_class = AuthorRegisterSerializer
    permission_classes = [AllowAny]