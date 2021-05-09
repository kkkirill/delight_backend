from django.conf import settings
from django_elasticsearch_dsl import (
    Document,
    fields,
)
from django_elasticsearch_dsl.registries import registry
from elasticsearch_dsl import analyzer
from factory.django import get_model

Artist = get_model('media', 'Artist')
html_strip = analyzer(
    'html_strip',
    tokenizer="standard",
    filter=["lowercase", "stop", "snowball"],
    char_filter=["html_strip"]
)

@registry.register_document
class ArtistDocument(Document):
    title = fields.TextField(
        attr='stage_name',
        analyzer=html_strip,
        fields={
            'raw': fields.KeywordField(),
            'suggest': fields.CompletionField(),
        }
    )

    class Meta:
        doc_type = 'artist_document'

    class Index:
        name = settings.ELASTICSEARCH_INDEX_NAMES[__name__]
        doc_type = 'artist_document'

    class Django:
        model = Artist
        fields = [
            'id',
            'photo'
        ]
