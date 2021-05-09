from django_elasticsearch_dsl_drf.filter_backends import (
    FilteringFilterBackend,
    IdsFilterBackend,
    OrderingFilterBackend,
    DefaultOrderingFilterBackend,
    SearchFilterBackend,
)
from django_elasticsearch_dsl_drf.viewsets import DocumentViewSet

from apps.search.documents.album import AlbumDocument
from apps.search.serializers.album import AlbumDocumentSerializer


class AlbumDocumentView(DocumentViewSet):
    document = AlbumDocument
    serializer_class = AlbumDocumentSerializer
    lookup_field = 'id'
    filter_backends = [
        FilteringFilterBackend,
        IdsFilterBackend,
        OrderingFilterBackend,
        DefaultOrderingFilterBackend,
        SearchFilterBackend,
    ]
    search_fields = ()
    filter_fields = {}
    ordering_fields = {}
    ordering = ('id',)
