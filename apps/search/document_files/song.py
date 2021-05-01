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
    id = fields.IntegerField(attr='id')
    title = fields.CompletionField(
        attr='title',
        fields={
            'suggest': fields.Completion(),
        }
    )
    image = fields.TextField(
        attr='image'
    )
    file = fields.TextField(
        attr='file'
    )
    artists = fields.NestedField(
        attr='artists',
        properties={
            'id': fields.IntegerField(attr='id'),
            'stage_name': fields.TextField(attr='stage_name'),
        },
        multi=True
    )
    genres = fields.NestedField(
        attr='genres',
        properties={
            'name': fields.TextField(attr='name'),
        },
        multi=True
    )

    class Meta:
        doc_type = 'song_document'

    class Index:
        name = 'songs'
        doc_type = 'song_document'

    class Django:
        model = Song
        fields = [
            'image',
            'explicit'
        ]
        related_models = [Artist]

    # def get_queryset(self):
    #     return super().get_queryset().prefetch_related('artists').only('artists__id', 'artists__stage_name', 'id', 'title')
    #
    # def get_instances_from_related(self, related_instance):
    #     if isinstance(related_instance, Artist):
    #         return related_instance.songs.all()
