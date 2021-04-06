from haystack import indexes

from apps.media.models import Album


class AlbumIndex(indexes.ModelSearchIndex, indexes.Indexable):
    class Meta:
        model = Album
        fields = [
            'title',
            'photo',
            'artists'
        ]

        def prepare_artists(self, obj):
            return [artist.stage_name for artist in obj.artists]


# class AlbumIndex(indexes.SearchIndex, indexes.Indexable):
#     text = indexes.CharField(document=True, use_template=True)
#     address = indexes.CharField(model_attr="address")
#     city = indexes.CharField(model_attr="city")
#     zip_code = indexes.CharField(model_attr="zip_code")
#
#     autocomplete = indexes.EdgeNgramField()
#     coordinates = indexes.LocationField(model_attr="coordinates")
#
#     @staticmethod
#     def prepare_autocomplete(obj):
#         return " ".join((
#             obj.address, obj.city, obj.zip_code
#         ))
#
#     def get_model(self):
#         return Location
#
#     def index_queryset(self, using=None):
#         return self.get_model().objects.filter(
#             created__lte=timezone.now()
#         )
