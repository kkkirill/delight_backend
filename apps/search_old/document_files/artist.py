from django_elasticsearch_dsl import (
    Document,
    fields,
)
from django_elasticsearch_dsl.registries import registry
from factory.django import get_model

Artist = get_model('media', 'Artist')


@registry.register_document
class ArtistDocument(Document):
    id = fields.IntegerField(attr='id')
    title = fields.TextField(
        attr='stage_name',
        fields={
            'suggest': fields.Completion(),
        }
    )

    class Meta:
        doc_type = 'artist_document'

    class Index:
        name = 'artists'
        doc_type = 'artist_document'

    class Django:
        model = Artist
        fields = ['photo']
