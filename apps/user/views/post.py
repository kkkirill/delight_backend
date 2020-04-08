from django.db.models import Q
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.mixins import CreateModelMixin, RetrieveModelMixin, UpdateModelMixin, ListModelMixin
from rest_framework.permissions import AllowAny, IsAuthenticatedOrReadOnly
from rest_framework.viewsets import GenericViewSet
from rest_framework_extensions.mixins import NestedViewSetMixin

from apps.likes.mixins import LikedMixin
from apps.likes.serializers.like import FanSerializer
from apps.user.models.post import Post
from apps.user.permissions import IsOwnerOrAdmin
from apps.user.serializers.post import PostSerializer, PostCUSerializer, PostShortInfoSerializer
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
    filter_backends = (DjangoFilterBackend, SearchFilter, OrderingFilter,)
    filterset_fields = '__all__'
    ordering_fields = '__all__'
    ordering = ('pub_date',)
    search_fields = ('id',)  # TODO SearchFilter fields

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

        if self.request.user.is_staff:
            return Post.objects.all()

        # TODO user post POST, DELETE, LIKE, UNLINE
        
        user_id = self.kwargs['parent_lookup_user_posts']  # TODO lookup
        # ids = [User.objects.filter(following=user_id).values_list('id', flat=True), user_id]
        # Post.objects.filter(owner__following__)
        return Post.objects.filter(Q(owner__following__followers__exact=user_id) & Q(owner=user_id))

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
