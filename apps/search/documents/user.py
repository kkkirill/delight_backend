from django.conf import settings
from django_elasticsearch_dsl import (
    Document,
)
from django_elasticsearch_dsl.registries import registry
from factory.django import get_model

User = get_model('user', 'User')


@registry.register_document
class UserDocument(Document):
    class Meta:
        doc_type = 'user_document'

    class Index:
        name = settings.ELASTICSEARCH_INDEX_NAMES[__name__]
        doc_type = 'user_document'

    class Django:
        model = User
        fields = [
            'id',
            'username',
            'photo'
        ]
