from itertools import chain

from django.db.models import Q
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.permissions import AllowAny, IsAuthenticatedOrReadOnly
from rest_framework.viewsets import ModelViewSet
from rest_framework_extensions.mixins import NestedViewSetMixin

from apps.likes.mixins import LikedMixin
from apps.likes.serializers.like import FanSerializer
from apps.user.models.post import Post
from apps.user.permissions import IsOwnerOrAdmin
from apps.user.serializers.post import PostSerializer, PostCUSerializer, PostShortInfoSerializer
from utils.permission_tools import ActionBasedPermission


class PostView(NestedViewSetMixin,
               LikedMixin,
               ModelViewSet):
    queryset = Post.objects.all()
    http_method_names = ('get', 'post', 'delete')
    permission_classes = (ActionBasedPermission,)
    action_permissions = {
        AllowAny: ('retrieve', 'list'),
        IsOwnerOrAdmin: ('create', 'destroy'),
        IsAuthenticatedOrReadOnly: ('like', 'fans'),
    }
    filter_backends = (DjangoFilterBackend, SearchFilter, OrderingFilter,)
    ordering_fields = ('id', 'likes', 'pub_date')
    search_fields = ('owner__id',)
    ordering = ('-pub_date',)

    def get_serializer_class(self):
        if self.request.method == 'GET':
            if self.action == 'list':
                return PostShortInfoSerializer
            elif self.action == 'retrieve':
                return PostSerializer
            elif self.action == 'fans':
                return FanSerializer
        elif self.request.method == 'POST':
            return PostCUSerializer

        return super().get_serializer_class()

    def get_queryset(self):
        if getattr(self, 'swagger_fake_view', False):
            return Post.objects.none()

        if self.request.user.is_staff:
            return Post.objects.all()

        user_id = int(self.kwargs['parent_lookup_user'])
        if user_id == -1:
            posts = Post.objects.all().order_by('-total_likes')
        elif self.request.user.is_anonymous:
            posts = Post.objects.filter(owner_id=user_id)
        else:
            following = self.request.user.following.values_list('id')
            posts = Post.objects.filter(
                Q(owner__in=chain(*following)) | Q(owner=user_id)
            )
        return posts
