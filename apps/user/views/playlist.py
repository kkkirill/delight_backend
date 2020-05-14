from django.utils.decorators import method_decorator
from django_filters.rest_framework import DjangoFilterBackend
from drf_yasg.openapi import Response as SwaggerResponse
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status, viewsets
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.permissions import AllowAny, IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework_extensions.mixins import NestedViewSetMixin

from apps.likes.mixins import LikedMixin
from apps.likes.serializers.like import FanSerializer
from apps.user.models.playlist import Playlist
from apps.user.permissions import IsOwnerOrAdmin, IsOwnerOrAdminSong
from apps.user.serializers.playlist import (
    PlaylistCUSerializer, PlaylistSerializer, PlaylistShortInfoSerializer,
    SongsInPlaylistSerializer)
from delight.settings import MY_SONGS_PLAYLIST_NAME, FAVORITES_PLAYLIST_NAME
from utils.permission_tools import ActionBasedPermission


@method_decorator(name='list', decorator=swagger_auto_schema(
    operation_description='# Get list of all playlists',
    responses={
        '200': SwaggerResponse(
            'The list of playlists has been retrieved successfully',
            PlaylistShortInfoSerializer()
        )
    }
))
@method_decorator(name='retrieve', decorator=swagger_auto_schema(
    operation_description='# Get playlists with the specified id',
    responses={
        '200': SwaggerResponse(
            'Playlist has been retrieved successfully',
            PlaylistSerializer()
        ),
        '401': 'Unauthorized',
        '404': "Playlist with specified id doesn't exist"
    }
))
@method_decorator(name='create', decorator=swagger_auto_schema(
    operation_description='# Create new Playlist',
    responses={
        '200': SwaggerResponse(
            'Playlist has been created successfully',
            PlaylistCUSerializer()
        ),
        '400': 'Bad request',
        '401': 'Unauthorized',
        '403': 'Permission denied'
    }
))
@method_decorator(name='update', decorator=swagger_auto_schema(
    operation_description='# Full update of the Playlist'
                          ' with the specified id',
    responses={
        '200': SwaggerResponse(
            'Playlist with specified id has been updated successfully',
            PlaylistCUSerializer()
        ),
        '400': 'Bad request',
        '401': 'Unauthorized',
        '403': 'Permission denied',
        '404': "Playlist with specified id doesn't exist"
    }
))
class PlaylistView(NestedViewSetMixin,
                   LikedMixin,
                   ModelViewSet):
    queryset = Playlist.objects.all()
    http_method_names = ('get', 'post', 'put', 'delete')
    permission_classes = (ActionBasedPermission,)
    action_permissions = {
        AllowAny: ('retrieve', 'list'),
        IsOwnerOrAdmin: ('create', 'update', 'destroy'),
        IsAuthenticatedOrReadOnly: ('like', 'fans'),
    }
    filter_backends = (DjangoFilterBackend, SearchFilter, OrderingFilter,)
    ordering_fields = ('id', 'likes', 'songs_amount')
    ordering = ['id']
    search_fields = ('=id', '=name', '=owner__id')

    def get_serializer_class(self):
        if self.request.method == 'GET':
            if self.action == 'list':
                return PlaylistShortInfoSerializer
            elif self.action == 'retrieve':
                return PlaylistSerializer
            elif self.action == 'fans':
                return FanSerializer
        elif self.request.method in ('POST', 'PUT'):
            return PlaylistCUSerializer

        return super().get_serializer_class()

    def get_queryset(self):

        if getattr(self, 'swagger_fake_view', False):
            return Playlist.objects.none()

        user_id = int(self.kwargs['parent_lookup_user_playlists'])
        if user_id == -1:
            return Playlist.objects.filter(is_private=False).order_by('-total_likes')
        if self.request.user.is_staff:
            return Playlist.objects.all()
        if self.request.user.id == user_id:
            qs = Playlist.objects.filter(owner_id=user_id)
            if self.action in ['create', 'destroy']:
                return qs.exclude(name__in=[FAVORITES_PLAYLIST_NAME, MY_SONGS_PLAYLIST_NAME])
            return qs
        return Playlist.objects.filter(owner=user_id, is_private=False)


@method_decorator(name='create', decorator=swagger_auto_schema(
    operation_description='# Create new Playlist',
    responses={
        '200': SwaggerResponse(
            'Playlist has been created successfully',
            PlaylistCUSerializer()
        ),
        '400': 'Bad request',
        '401': 'Unauthorized',
        '403': 'Permission denied'
    }
))
@method_decorator(name='destroy', decorator=swagger_auto_schema(
    operation_description='# Delete Song by id from the Playlist'
                          ' with the specified id',
    responses={
        '200': SwaggerResponse(
            'Song with specified id has been updated successfully',
            PlaylistCUSerializer()
        ),
        '400': 'Bad request',
        '401': 'Unauthorized',
        '403': 'Permission denied',
        '404': "Playlist with specified id doesn't exist"
    }
))
class SongsInPlaylistView(NestedViewSetMixin, viewsets.ModelViewSet):
    http_method_names = ('post', 'delete',)
    serializer_class = SongsInPlaylistSerializer
    permission_classes = (IsOwnerOrAdminSong,)

    def get_queryset(self):
        if getattr(self, 'swagger_fake_view', False):
            return Playlist.objects.none()

        playlist_id = self.kwargs['parent_lookup_playlist']
        return Playlist.objects.filter(pk=playlist_id)

    def destroy(self, request, *args, **kwargs):
        playlist_id = self.kwargs['parent_lookup_playlist']
        playlist = Playlist.objects.get(pk=playlist_id)
        song_id = self.kwargs.get('pk')
        playlist.songs.remove(song_id)
        return Response(status=status.HTTP_204_NO_CONTENT)
