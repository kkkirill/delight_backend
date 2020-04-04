from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.mixins import (
    CreateModelMixin, ListModelMixin, RetrieveModelMixin, UpdateModelMixin)
from rest_framework.permissions import (
    AllowAny, IsAdminUser, IsAuthenticatedOrReadOnly)
from rest_framework.viewsets import GenericViewSet

from apps.likes.mixins import LikedMixin
from apps.media.models.artist import Artist
from apps.media.serializers.artist import (
    ArtistCUSerializer, ArtistDetailSerializer, ArtistShortInfoSerializer)
from utils.permission_tools import ActionBasedPermission


class ArtistView(LikedMixin,
                 CreateModelMixin,
                 RetrieveModelMixin,
                 UpdateModelMixin,
                 ListModelMixin,
                 GenericViewSet):
    queryset = Artist.objects.all()
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ('genres',)
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
                return ArtistShortInfoSerializer
            elif self.action == 'retrieve':
                return ArtistDetailSerializer
        elif self.request.method in ('POST', 'PUT'):
            return ArtistCUSerializer
