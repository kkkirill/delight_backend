from django.utils.decorators import method_decorator
from django_filters.rest_framework import DjangoFilterBackend
from drf_yasg.openapi import Response as SwaggerResponse
from drf_yasg.utils import swagger_auto_schema
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.mixins import (
    CreateModelMixin, ListModelMixin, RetrieveModelMixin, UpdateModelMixin)
from rest_framework.permissions import (
    AllowAny, IsAdminUser, IsAuthenticatedOrReadOnly)
from rest_framework.viewsets import GenericViewSet

from apps.likes.mixins import LikedMixin
from apps.likes.serializers.like import FanSerializer
from apps.media.models.album import Album
from apps.media.serializers.album import (
    AlbumCUSerializer, AlbumDetailSerializer, AlbumShortInfoSerializer)
from utils.permission_tools import ActionBasedPermission


@method_decorator(name='list', decorator=swagger_auto_schema(
    operation_description='# Get list of all albums',
    responses={
        '200': SwaggerResponse(
            'The list of albums has been retrieved successfully',
            AlbumShortInfoSerializer()
        )
    }
))
@method_decorator(name='retrieve', decorator=swagger_auto_schema(
    operation_description='# Get album with the specified id',
    responses={
        '200': SwaggerResponse(
            'Album has been retrieved successfully',
            AlbumDetailSerializer()
        ),
        '404': "Album with specified id doesn't exist"
    }
))
@method_decorator(name='create', decorator=swagger_auto_schema(
    operation_description='# Create new Album',
    responses={
        '200': SwaggerResponse(
            'Album has been created successfully',
            AlbumCUSerializer()
        ),
        '400': 'Bad request',
        '401': 'Unauthorized',
        '403': 'Permission denied'
    }
))
@method_decorator(name='update', decorator=swagger_auto_schema(
    operation_description='# Full or partial update of the Album'
                          ' with the specified id',
    responses={
        '200': SwaggerResponse(
            'Album with specified id has been updated successfully',
            AlbumCUSerializer()
        ),
        '400': 'Bad request',
        '401': 'Unauthorized',
        '403': 'Permission denied',
        '404': "Album with specified id doesn't exist"
    }
))
class AlbumView(LikedMixin,
                CreateModelMixin,
                RetrieveModelMixin,
                UpdateModelMixin,
                ListModelMixin,
                GenericViewSet):
    queryset = Album.objects.all()
    filter_backends = (DjangoFilterBackend, SearchFilter, OrderingFilter,)
    filterset_fields = '__all__'
    ordering_fields = '__all__'
    search_fields = ('id',)  # TODO SearchFilter fields
    ordering = ('title',)
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
            elif self.action == 'fans':
                return FanSerializer
        elif self.request.method in ('POST', 'PUT'):
            return AlbumCUSerializer

        return super().get_serializer_class()
