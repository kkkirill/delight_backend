from rest_framework.fields import SerializerMethodField
from rest_framework.serializers import ModelSerializer

from apps.likes import mixin_tools as likes_services
from apps.media.serializers.song import SongShortInfoSerializer
from apps.user.models.post import Post


class PostSerializer(ModelSerializer):
    songs = SongShortInfoSerializer(many=True, )
    is_fan = SerializerMethodField()

    class Meta:
        model = Post
        fields = ('owner', 'pub_date', 'total_likes', 'text', 'images', 'songs', 'playlists', 'albums')
        read_only_fields = ('pub_date', )

    def get_is_fan(self, obj) -> bool:
        user = self.context.get('request').user
        return likes_services.is_fan(obj, user)


class PostShortInfoSerializer(ModelSerializer):
    class Meta(PostSerializer.Meta):
        fields = ()


class PostCUSerializer(ModelSerializer):
    class Meta(PostSerializer.Meta):
        fields = ('owner', 'text', 'images', 'songs', 'playlists', 'albums', )

    def get_fields(self, *args, **kwargs):
        fields = super(PostCUSerializer, self).get_fields()
        request = self.context.get('request', None)
        if request and getattr(request, 'method', None) == "PUT":
            for field in fields.values():
                field.required = False
        return fields
