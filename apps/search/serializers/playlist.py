from django_elasticsearch_dsl_drf.serializers import DocumentSerializer

from apps.search.documents.playlist import PlaylistDocument


class PlaylistDocumentSerializer(DocumentSerializer):
    class Meta:
        document = PlaylistDocument

        fields = (
            'id',
            'name',
            'photo'
        )
