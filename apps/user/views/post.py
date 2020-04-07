from rest_framework.mixins import CreateModelMixin, RetrieveModelMixin, UpdateModelMixin, ListModelMixin
from rest_framework.permissions import AllowAny, IsAuthenticatedOrReadOnly
from rest_framework.viewsets import GenericViewSet
from rest_framework_extensions.mixins import NestedViewSetMixin

from apps.likes.mixins import LikedMixin
from apps.likes.serializers.like import FanSerializer
from apps.user.models.post import Post
from apps.user.permissions import IsOwnerOrAdmin
from apps.user.serializers.post import PostSerializer, PostCUSerializer
from utils.permission_tools import ActionBasedPermission


class PostView(NestedViewSetMixin,
               LikedMixin,
               CreateModelMixin,
               RetrieveModelMixin,
               UpdateModelMixin,
               ListModelMixin,
               GenericViewSet):
    http_method_names = ('get', 'post', 'put', 'delete')
    permission_classes = (ActionBasedPermission,)
    action_permissions = {
        AllowAny: ('retrieve', 'list'),
        IsOwnerOrAdmin: ('create', 'update'),
        IsAuthenticatedOrReadOnly: ('like', 'fans'),
    }

    def get_serializer_class(self):
        if self.request.method == 'GET':
            if self.action == 'list':
                return PostShortInfoSerializer
            elif self.action == 'retrieve':
                return PostSerializer
            elif self.action == 'fans':
                return FanSerializer
        elif self.request.method in ('POST', 'PUT'):
            return PostCUSerializer

        return super().get_serializer_class()

    def get_queryset(self):

        if getattr(self, 'swagger_fake_view', False):
            return Post.objects.none()

        user_id = self.kwargs['parent_lookup_user_playlists']  # TODO lookup

        if self.request.user.is_staff:
            return Post.objects.all()

        return Playlist.objects.filter(owner=user_id, is_private=False)

# class SongsInPlaylistView(NestedViewSetMixin, viewsets.ModelViewSet):
#     http_method_names = ('post', 'delete',)
#     serializer_class = SongsInPlaylistSerializer
#     permission_classes = (IsOwnerOrAdminSong,)
#
#     def get_queryset(self):
#         if getattr(self, 'swagger_fake_view', False):
#             return Playlist.objects.none()
#
#         playlist_id = self.kwargs['parent_lookup_playlist']
#         return Playlist.objects.filter(pk=playlist_id)
#
#     def destroy(self, request, *args, **kwargs):
#         playlist_id = self.kwargs['parent_lookup_playlist']
#         playlist = Playlist.objects.get(pk=playlist_id)
#         song_id = self.kwargs.get('pk')
#         playlist.songs.remove(song_id)
#         return Response(status=status.HTTP_204_NO_CONTENT)
