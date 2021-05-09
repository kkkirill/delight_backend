from django_elasticsearch_dsl_drf.serializers import DocumentSerializer

from apps.search.documents.user import UserDocument


class UserDocumentSerializer(DocumentSerializer):
    class Meta:
        document = UserDocument

        fields = (
            'id',
            'username',
            'photo'
        )
