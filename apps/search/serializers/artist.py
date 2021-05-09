from django_elasticsearch_dsl_drf.serializers import DocumentSerializer

from apps.search.documents.artist import ArtistDocument


class ArtistDocumentSerializer(DocumentSerializer):
    class Meta:
        document = ArtistDocument

        fields = (
            'id',
            'title',
            'photo',
        )
