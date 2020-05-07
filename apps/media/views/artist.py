from django.utils.decorators import method_decorator
from django_filters.rest_framework import DjangoFilterBackend
from drf_yasg.openapi import Response as SwaggerResponse
from drf_yasg.utils import swagger_auto_schema
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.mixins import (
    CreateModelMixin, ListModelMixin, RetrieveModelMixin, UpdateModelMixin)
from rest_framework.permissions import (
    AllowAny, IsAdminUser, IsAuthenticatedOrReadOnly)
from rest_framework.viewsets import GenericViewSet, ModelViewSet

from apps.likes.mixins import LikedMixin
from apps.likes.serializers.like import FanSerializer
from apps.media.models.artist import Artist
from apps.media.serializers.artist import (
    ArtistCUSerializer, ArtistDetailSerializer, ArtistShortInfoSerializer)
from utils.permission_tools import ActionBasedPermission


@method_decorator(name='list', decorator=swagger_auto_schema(
    operation_description='# Get list of all artists',
    responses={
        '200': SwaggerResponse(
            'The list of artists has been retrieved successfully',
            ArtistShortInfoSerializer()
        )
    }
))
@method_decorator(name='retrieve', decorator=swagger_auto_schema(
    operation_description='# Get artist with the specified id',
    responses={
        '200': SwaggerResponse(
            'Artist has been retrieved successfully',
            ArtistDetailSerializer()
        ),
        '404': "Artist with specified id doesn't exist"
    }
))
@method_decorator(name='create', decorator=swagger_auto_schema(
    operation_description='# Create new Artist',
    responses={
        '200': SwaggerResponse(
            'Artist has been created successfully',
            ArtistCUSerializer()
        ),
        '400': 'Bad request',
        '401': 'Unauthorized',
        '403': 'Permission denied'
    }
))
@method_decorator(name='update', decorator=swagger_auto_schema(
    operation_description='# Full or partial update of the Artist'
                          ' with the specified id',
    responses={
        '200': SwaggerResponse(
            'Artist with specified id has been updated successfully',
            ArtistCUSerializer()
        ),
        '400': 'Bad request',
        '401': 'Unauthorized',
        '403': 'Permission denied',
        '404': "Artist with specified id doesn't exist"
    }
))
class ArtistView(LikedMixin,
                 ModelViewSet):
    queryset = Artist.objects.all()
    filter_backends = (DjangoFilterBackend, SearchFilter, OrderingFilter,)
    filterset_fields = ('genres',)
    ordering_fields = ('id', 'likes')
    search_fields = ('id', 'stage_name')
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
            elif self.action == 'fans':
                return FanSerializer
        elif self.request.method in ('POST', 'PUT'):
            return ArtistCUSerializer

        return super().get_serializer_class()
