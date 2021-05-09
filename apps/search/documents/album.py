from django.conf import settings
from django_elasticsearch_dsl import (
    Document,
    fields,
)
from django_elasticsearch_dsl.registries import registry
from factory.django import get_model

Album = get_model('media', 'Album')
Artist = get_model('media', 'Artist')


@registry.register_document
class AlbumDocument(Document):
    title = fields.TextField(
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

    def prepare_id(self, instance):
        return instance.id

    class Meta:
        doc_type = 'album_document'

    class Index:
        name = settings.ELASTICSEARCH_INDEX_NAMES[__name__]
        doc_type = 'album_document'

    class Django:
        model = Album
        fields = ['id', 'photo']
        related_models = [Artist]

    def get_queryset(self):
        return super().get_queryset().prefetch_related('artists')

    def get_instances_from_related(self, related_instance):
        return related_instance.albums.all()
