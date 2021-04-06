from django_elasticsearch_dsl import (
    Document,
    fields,
)
from django_elasticsearch_dsl.registries import registry
from factory.django import get_model

Album = get_model('media', 'Album')


@registry.register_document
class AlbumDocument(Document):
    id = fields.IntegerField(attr='id')
    title = fields.TextField(
        attr='title',
        fields={
            'suggest': fields.Completion(),
        }
    )

    class Meta:
        doc_type = 'album_document'

    class Index:
        name = 'albums'
        doc_type = 'album_document'

    class Django:
        model = Album
        fields = ['photo']
