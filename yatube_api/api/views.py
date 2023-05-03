from .serializers import (PostSerializer,
                          CommentSerializer,
                          GroupSerializer,
                          FollowSerializer)
from posts.models import Group, Post, Follow
from django.shortcuts import get_object_or_404
from rest_framework import viewsets, status, filters
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.exceptions import AuthenticationFailed
from .permissions import IsPostAuthor


class GroupViewSet(viewsets.ModelViewSet):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    permission_classes = [IsPostAuthor]

    def create(self, request):
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)


class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    pagination_class = LimitOffsetPagination
    permission_classes = (IsPostAuthor,)

    def perform_create(self, serializer):
        if self.request.user.is_authenticated:
            serializer.save(author=self.request.user)
        else:
            raise AuthenticationFailed('Нужно пройти авторизацию.')


class FollowViewSet(viewsets.ModelViewSet):
    queryset = Follow.objects.all()
    serializer_class = FollowSerializer
    permission_classes = (IsAuthenticated,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ('following__username',)

    def get_queryset(self):
        return self.request.user.follower.all()

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = (IsPostAuthor,)

    def get_queryset(self):
        post = get_object_or_404(Post, pk=self.kwargs.get('post_id'))
        return post.comments

    def perform_create(self, serializer):
        post = get_object_or_404(Post, pk=self.kwargs.get('post_id'))
        if not self.request.user.is_authenticated:
            raise AuthenticationFailed('Нужно пройти авторизацию.')
        serializer.save(author=self.request.user, post=post)

    def update(self, request, *args, **kwargs):
        comment = self.get_object()
        if comment.author != request.user:
            return Response(status=status.HTTP_403_FORBIDDEN)
        serializer = self.get_serializer(comment,
                                         data=request.data,
                                         partial=True)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)
