from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter
from rest_framework.mixins import (
    CreateModelMixin, ListModelMixin, RetrieveModelMixin, UpdateModelMixin)
from rest_framework.permissions import (
    AllowAny, IsAdminUser, IsAuthenticatedOrReadOnly)
from rest_framework.viewsets import GenericViewSet

from apps.likes.mixins import LikedMixin
from apps.media.models.album import Album
from apps.media.serializers.album import (
    AlbumCUSerializer, AlbumDetailSerializer, AlbumShortInfoSerializer)
from utils.permission_tools import ActionBasedPermission


class AlbumView(LikedMixin,
                CreateModelMixin,
                RetrieveModelMixin,
                UpdateModelMixin,
                ListModelMixin,
                GenericViewSet):
    queryset = Album.objects.all()
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_fields = ('genres', 'artists')
    ordering_fields = ('release_year',)
    http_method_names = ('get', 'post', 'put', 'delete')
    permission_classes = (ActionBasedPermission,)
    action_permissions = {
        AllowAny: ('retrieve', 'list'),
        IsAdminUser: ('create', 'update'),
        IsAuthenticatedOrReadOnly: ('like', 'fans'),
    }

    def get_serializer_class(self):
        if self.request.method == 'GET':
            if self.action == 'list':
                return AlbumShortInfoSerializer
            elif self.action == 'retrieve':
                return AlbumDetailSerializer
        elif self.request.method in ('POST', 'PUT'):
            return AlbumCUSerializer
