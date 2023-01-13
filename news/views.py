from django.shortcuts import render
from rest_framework import viewsets, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status
from rest_framework import generics
from rest_framework import filters
from rest_framework.pagination import PageNumberPagination, LimitOffsetPagination
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.permissions import IsAuthenticated

from .models import News, NewsStatus, CommentStatus, Status, Comment
from .permissions import PostPermission
from .serilaizers import NewsSerializer, CommentSerializer, NewsStatusSerializer, CommentSerializer, StatusSerializer


class PostPagePagination(PageNumberPagination):
    page_size = 3


class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer

    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['news_id']
    pagination_class = LimitOffsetPagination


class NewsViewSet(viewsets.ModelViewSet):
    queryset = News.objects.all()
    serializer_class = NewsSerializer

    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    # filterset_fields = ['']
    search_fields = ['title']
    ordering_fields = ['created']
    pagination_class = PostPagePagination

    @action(methods=['POST', 'GET'], detail=True, permission_classes=[permissions.IsAuthenticated])
    def slug(self, request, pk=None):
        serializer = NewsSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(
                author=request.user.author,
                news=self.get_object()
            )
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class StatusViewSet(viewsets.ModelViewSet):
    queryset = Status.objects.all()
    serializer_class = StatusSerializer


class CommentListCreateAPIView(generics.ListCreateAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [PostPermission, ]

    def get_queryset(self):
        return super().get_queryset().filter(news_id=self.kwargs.get('news_id'))

    def perform_create(self, serializer):
        serializer.save(
            author=self.request.user.author,
            news_id=self.kwargs.get('news_id')
        )