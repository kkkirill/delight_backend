from django.utils.decorators import method_decorator
from drf_yasg.openapi import Response as SwaggerResponse
from drf_yasg.utils import swagger_auto_schema
from rest_framework import viewsets

from apps.media.models.genre import Genre
from apps.media.serializers.genre import GenreDetailSerializer


@method_decorator(name='list', decorator=swagger_auto_schema(
    operation_description='# Get list of all genres',
    responses={
        '200': SwaggerResponse(
            'The list of genres has been retrieved successfully',
            GenreDetailSerializer()
        )
    }
))
@method_decorator(name='retrieve', decorator=swagger_auto_schema(
    operation_description='# Get genres with the specified id',
    responses={
        '200': SwaggerResponse(
            'Genre has been retrieved successfully',
            GenreDetailSerializer()
        ),
        '404': "Genre with specified id doesn't exist"
    }
))
class GenreView(viewsets.ModelViewSet):
    serializer_class = GenreDetailSerializer
    queryset = Genre.objects.all()
    http_method_names = ('get',)
    ordering_fields = ('=id', )
    search_fields = ('id', 'name')
