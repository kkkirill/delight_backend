from rest_framework.serializers import ModelSerializer

from apps.s3.models import File


class FileSerializer(ModelSerializer):
    class Meta:
        model = File
        fields = ('file', 'type')
