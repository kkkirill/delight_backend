from django_elasticsearch_dsl_drf.filter_backends import (
    FilteringFilterBackend,
    IdsFilterBackend,
    OrderingFilterBackend,
    DefaultOrderingFilterBackend,
    SearchFilterBackend,
)
from django_elasticsearch_dsl_drf.viewsets import DocumentViewSet

from apps.search.documents.playlist import PlaylistDocument
from apps.search.serializers.playlist import PlaylistDocumentSerializer


class PlaylistDocumentView(DocumentViewSet):
    document = PlaylistDocument
    serializer_class = PlaylistDocumentSerializer
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
