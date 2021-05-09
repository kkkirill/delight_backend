from django_elasticsearch_dsl_drf.filter_backends import (
    FilteringFilterBackend,
    IdsFilterBackend,
    OrderingFilterBackend,
    DefaultOrderingFilterBackend,
    SearchFilterBackend,
)
from django_elasticsearch_dsl_drf.viewsets import DocumentViewSet

from apps.search.documents.song import SongDocument
from apps.search.serializers.song import SongDocumentSerializer


class SongDocumentView(DocumentViewSet):
    document = SongDocument
    serializer_class = SongDocumentSerializer
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
