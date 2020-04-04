from rest_framework import status, viewsets
from rest_framework.mixins import (
    CreateModelMixin, ListModelMixin, RetrieveModelMixin, UpdateModelMixin)
from rest_framework.permissions import AllowAny, IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet
from rest_framework_extensions.mixins import NestedViewSetMixin

from apps.likes.mixins import LikedMixin
from apps.user.models.playlist import Playlist
from apps.user.permissions import IsOwnerOrAdmin, IsOwnerOrAdminSong
from apps.user.serializers.playlist import (
    PlaylistCUSerializer, PlaylistSerializer, PlaylistShortInfoSerializer,
    SongsInPlaylistSerializer)
from utils.permission_tools import ActionBasedPermission


class PlaylistView(NestedViewSetMixin,
                   LikedMixin,
                   CreateModelMixin,
                   RetrieveModelMixin,
                   UpdateModelMixin,
                   ListModelMixin,
                   GenericViewSet):
    http_method_names = ('get', 'post', 'put')
    permission_classes = (ActionBasedPermission,)
    action_permissions = {
        AllowAny: ('retrieve', 'list'),
        IsOwnerOrAdmin: ('create', 'update'),
        IsAuthenticatedOrReadOnly: ('like', 'fans'),
    }

    def get_serializer_class(self):
        if self.request.method == 'GET':
            if self.action == 'list':
                return PlaylistShortInfoSerializer
            elif self.action == 'retrieve':
                return PlaylistSerializer
        elif self.request.method in ('POST', 'PUT'):
            return PlaylistCUSerializer

    def get_queryset(self):
        user_id = self.kwargs['parent_lookup_user_playlists']
        if self.request.user.id == user_id or self.request.user.is_staff:
            return Playlist.objects.filter(owner_id=user_id)
        return Playlist.objects.filter(owner=user_id,
                                       is_private=False)


class SongsInPlaylistView(NestedViewSetMixin, viewsets.ModelViewSet):
    http_method_names = ('post', 'delete',)
    serializer_class = SongsInPlaylistSerializer
    permission_classes = (IsOwnerOrAdminSong,)

    def get_queryset(self):
        playlist_id = self.kwargs['parent_lookup_playlist']
        return Playlist.objects.filter(pk=playlist_id)

    def destroy(self, request, *args, **kwargs):
        playlist_id = self.kwargs['parent_lookup_playlist']
        playlist = Playlist.objects.get(pk=playlist_id)
        song_id = self.kwargs.get('pk')
        playlist.songs.remove(song_id)
        return Response(status=status.HTTP_204_NO_CONTENT)
