from rest_framework.serializers import ModelSerializer
from ..models.album import Album


class AlbumSerializer(ModelSerializer):

    class Meta:
        model = Album
        fields = '__all__'
        read_only_fields = ('songs_amount', )
