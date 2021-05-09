from django_elasticsearch_dsl_drf.constants import SUGGESTER_COMPLETION
from django_elasticsearch_dsl_drf.filter_backends import (
    FilteringFilterBackend,
    IdsFilterBackend,
    OrderingFilterBackend,
    DefaultOrderingFilterBackend,
    SearchFilterBackend,
    SuggesterFilterBackend
)
from django_elasticsearch_dsl_drf.viewsets import DocumentViewSet

from apps.search.documents.artist import ArtistDocument
from apps.search.serializers.artist import ArtistDocumentSerializer


class ArtistDocumentView(DocumentViewSet):
    document = ArtistDocument
    serializer_class = ArtistDocumentSerializer
    lookup_field = 'id'
    filter_backends = [
        FilteringFilterBackend,
        IdsFilterBackend,
        OrderingFilterBackend,
        DefaultOrderingFilterBackend,
        SearchFilterBackend,
        SuggesterFilterBackend
    ]
    search_fields = ('title', )
    filter_fields = {}
    ordering_fields = {}
    ordering = ('id',)

    suggester_fields = {
        'title_suggest': {
            'field': 'title.suggest',
            'suggesters': [
                SUGGESTER_COMPLETION,
            ],
            'options': {
                'size': 20,
                'skip_duplicates': True,
            },
        },
    }
