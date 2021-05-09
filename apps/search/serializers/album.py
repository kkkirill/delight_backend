from django_elasticsearch_dsl_drf.serializers import DocumentSerializer

from apps.search.documents.album import AlbumDocument


class AlbumDocumentSerializer(DocumentSerializer):
    class Meta:
        document = AlbumDocument

        fields = (
            'id',
            'title',
            'photo',
            'artists'
        )
