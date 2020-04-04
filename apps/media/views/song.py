from django_filters.rest_framework import DjangoFilterBackend
from django_redis import get_redis_connection
from rest_framework.decorators import action
from rest_framework.mixins import (
    CreateModelMixin, ListModelMixin, RetrieveModelMixin, UpdateModelMixin)
from rest_framework.permissions import (
    AllowAny, IsAdminUser, IsAuthenticatedOrReadOnly)
from rest_framework.response import Response
from rest_framework.status import HTTP_400_BAD_REQUEST
from rest_framework.viewsets import GenericViewSet

from apps.likes.mixins import LikedMixin
from apps.media.models.song import Song
from apps.media.serializers.song import (
    SongCUSerializer, SongDetailSerializer, SongShortInfoSerializer)
from utils.permission_tools import ActionBasedPermission


class SongView(LikedMixin,
               CreateModelMixin,
               RetrieveModelMixin,
               UpdateModelMixin,
               ListModelMixin,
               GenericViewSet):
    queryset = Song.objects.all()
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ('genres', 'artists',)
    http_method_names = ('get', 'post', 'put', 'delete')
    permission_classes = (ActionBasedPermission,)
    action_permissions = {
        AllowAny: ('retrieve', 'list'),
        IsAdminUser: ('create', 'update'),
        IsAuthenticatedOrReadOnly: ('like', 'fans', 'listen'),
    }

    def get_serializer_class(self):
        if self.request.method == 'GET':
            if self.action == 'list':
                return SongShortInfoSerializer
            elif self.action == 'retrieve':
                return SongDetailSerializer
        elif self.request.method in ('POST', 'PUT'):
            return SongCUSerializer


    @action(methods=['POST'], detail=True)
    def listen(self, request, *args, **kwargs):
        start_second = request.data.get('start_second')
        end_second = request.data.get('end_second')
        song = Song.objects.get(pk=kwargs['pk'])
        err_details = None

        if type(start_second) is not int or type(end_second) is not int:
            err_details = "'start_second' and 'end_second' must be integer"
        elif start_second is None or end_second is None:
            err_details = "'start_secnod' or 'end_second' parameter is missing"
        elif start_second >= end_second:
            err_details = "'start_second' have to be less than 'end_second'"
        elif start_second < 0:
            err_details = "'start_second' have to be positive'"
        elif end_second > song.duration:
            err_details = "'end_second' must not exceed song duration"
        elif end_second - start_second > 30:
            err_details = 'piece have to be 30 seconds or less'

        if err_details:
            return Response({'Details': err_details}, status=HTTP_400_BAD_REQUEST)

        user = request.user
        con = get_redis_connection('default')
        con.sadd(f'{user.id}-{song.id}-piece', f'{start_second}-{end_second}')

        return Response({'title': song.title, 'duration': song.duration})
