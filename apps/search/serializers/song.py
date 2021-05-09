from django_elasticsearch_dsl_drf.serializers import DocumentSerializer

from apps.search.documents.song import SongDocument


class SongDocumentSerializer(DocumentSerializer):
    class Meta:
        document = SongDocument

        fields = (
            'id',
            'title',
            'image',
            'artists'
        )
