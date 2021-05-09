from django.conf import settings
from django_elasticsearch_dsl import (
    Document,
)
from django_elasticsearch_dsl.registries import registry
from factory.django import get_model

Playlist = get_model('user', 'Playlist')


@registry.register_document
class PlaylistDocument(Document):
    class Meta:
        doc_type = 'playlist_document'

    class Index:
        name = settings.ELASTICSEARCH_INDEX_NAMES[__name__]
        doc_type = 'playlist_document'

    class Django:
        model = Playlist
        fields = [
            'id',
            'name',
            'photo'
        ]

    def get_queryset(self):
        return Playlist.objects.filter(is_private=False)
