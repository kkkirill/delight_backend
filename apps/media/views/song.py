from django.shortcuts import get_object_or_404
from django.utils.decorators import method_decorator
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter, SearchFilter
from django_redis import get_redis_connection
from drf_yasg.openapi import Response as SwaggerResponse
from drf_yasg.utils import swagger_auto_schema
from rest_framework.decorators import action
from rest_framework.mixins import (
    CreateModelMixin, ListModelMixin, RetrieveModelMixin, UpdateModelMixin, DestroyModelMixin)
from rest_framework.permissions import (
    AllowAny, IsAdminUser, IsAuthenticatedOrReadOnly)
from rest_framework.response import Response
from rest_framework.status import HTTP_400_BAD_REQUEST
from rest_framework.viewsets import GenericViewSet, ModelViewSet

from apps.likes.mixins import LikedMixin
from apps.likes.serializers.like import FanSerializer
from apps.media.models.song import Song
from apps.media.serializers.song import (
    SongCUSerializer, SongDetailSerializer, SongShortInfoSerializer)
from utils.permission_tools import ActionBasedPermission


@method_decorator(name='list', decorator=swagger_auto_schema(
    operation_description='# Get list of all songs',
    responses={
        '200': SwaggerResponse(
            'The list of songs has been retrieved successfully',
            SongShortInfoSerializer()
        )
    }
))
@method_decorator(name='retrieve', decorator=swagger_auto_schema(
    operation_description='# Get songs with the specified id',
    responses={
        '200': SwaggerResponse(
            'Song has been retrieved successfully',
            SongDetailSerializer()
        ),
        '404': "Song with specified id doesn't exist"
    }
))
@method_decorator(name='create', decorator=swagger_auto_schema(
    operation_description='# Create new Song',
    responses={
        '200': SwaggerResponse(
            'Song has been created successfully',
            SongCUSerializer()
        ),
        '400': 'Bad request',
        '401': 'Unauthorized',
        '403': 'Permission denied'
    }
))
@method_decorator(name='update', decorator=swagger_auto_schema(
    operation_description='# Full update of the Song'
                          ' with the specified id',
    responses={
        '200': SwaggerResponse(
            'Song with specified id has been updated successfully',
            SongCUSerializer()
        ),
        '400': 'Bad request',
        '401': 'Unauthorized',
        '403': 'Permission denied',
        '404': "Song with specified id doesn't exist"
    }
))
class SongView(LikedMixin,
               ModelViewSet):
    queryset = Song.objects.all()
    filter_backends = (DjangoFilterBackend, SearchFilter, OrderingFilter,)
    filterset_fields = ('genres', 'artists',)
    ordering_fields = ('id', 'listens', 'duration')
    search_fields = ('id', 'title')
    ordering = ('title',)
    http_method_names = ('get', 'post', 'put', 'delete')
    permission_classes = (ActionBasedPermission,)
    action_permissions = {
        AllowAny: ('retrieve', 'list'),
        IsAdminUser: ('create', 'update', 'destroy'),
        IsAuthenticatedOrReadOnly: ('like', 'fans', 'listen'),
    }

    def get_serializer_class(self):
        if self.request.method == 'GET':
            if self.action == 'list':
                return SongShortInfoSerializer
            elif self.action == 'retrieve':
                return SongDetailSerializer
            elif self.action == 'fans':
                return FanSerializer
        elif self.request.method in ('POST', 'PUT'):
            return SongCUSerializer

        return super().get_serializer_class()

    @action(methods=['POST'], detail=True)
    def listen(self, request, *args, **kwargs):
        start_second = request.data.get('start_second')
        end_second = request.data.get('end_second')
        song = get_object_or_404(Song, pk=kwargs['pk'])
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
            return Response(
                {'Details': err_details}, status=HTTP_400_BAD_REQUEST
            )

        user = request.user
        con = get_redis_connection('default')
        con.sadd(f'{user.id}-{song.id}-piece', f'{start_second}-{end_second}')

        return Response({'title': song.title, 'duration': song.duration})
