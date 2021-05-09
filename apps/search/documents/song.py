from django.conf import settings
from django_elasticsearch_dsl import (
    Document,
    fields,
)
from django_elasticsearch_dsl.registries import registry
from factory.django import get_model

Artist = get_model('media', 'Artist')
Song = get_model('media', 'Song')


@registry.register_document
class SongDocument(Document):
    title = fields.CompletionField(
        attr='title',
        fields={
            'suggest': fields.Completion(),
        }
    )
    artists = fields.NestedField(
        attr='artists',
        properties={
            'id': fields.IntegerField(attr='id'),
            'stage_name': fields.TextField(attr='stage_name'),
        },
        multi=True
    )

    class Meta:
        doc_type = 'song_document'

    class Index:
        name = settings.ELASTICSEARCH_INDEX_NAMES[__name__]
        doc_type = 'song_document'

    class Django:
        model = Song
        fields = [
            'id',
            'image',
        ]
        related_models = [Artist]

    def get_queryset(self):
        return super().get_queryset().prefetch_related('artists') # .only('artists__id', 'artists__stage_name', 'id', 'title')

    def get_instances_from_related(self, related_instance):
        return related_instance.songs.all()
