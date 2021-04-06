from collections import OrderedDict
from operator import itemgetter

from rest_framework import serializers


class GlobalDocumentSerializer(serializers.Serializer):

    id = serializers.ReadOnlyField()
    title = serializers.SerializerMethodField()
    index = serializers.SerializerMethodField()
    photo = serializers.SerializerMethodField()
    image = serializers.SerializerMethodField()
    is_explicit = serializers.SerializerMethodField()

    def get_title(self, obj):
        return getattr(obj, 'title', None)

    def get_index(self, obj):
        return obj.meta['index']

    def get_photo(self, obj):
        return getattr(obj, 'photo', None)

    def get_image(self, obj):
        return getattr(obj, 'image', None)

    def get_is_explicit(self, obj):
        return getattr(obj, 'explicit', None)

    def to_representation(self, instance):
        ret = super().to_representation(instance)
        # Here we filter the null values and creates a new dictionary
        # We use OrderedDict like in original method

        ret = {k: v for k, v in ret.items() if v is not None}
        return ret

    class Meta:
        fields = (
            'id',
        )
        read_only_fields = fields
