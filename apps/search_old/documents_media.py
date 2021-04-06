# from django_elasticsearch_dsl import (
#     Document,
#     fields,
# )
# from django_elasticsearch_dsl.registries import registry
# from factory.django import get_model
#
# Album = get_model('media', 'Album')
# Song = get_model('media', 'Song')
#
#
# @registry.register_document
# class AlbumDocument(Document):
#     id = fields.IntegerField(attr='id')
#     title = fields.TextField(
#         attr='title',
#         fields={
#             'suggest': fields.Completion(),
#         }
#     )
#     # songs = fields.ObjectField(
#     #     properties={
#     #         'songs': fields.TextField(),
#     #     },
#     #     multi=True
#     # )
#
#     class Meta:
#         doc_type = 'album_document'
#
#     class Index:
#         name = 'albums'
#         doc_type = 'album_document'
#
#     class Django:
#         model = Album
#         fields = ['photo']
#         # related_models = [Song]
#
#     # def get_queryset(self):
#     #     return super().get_queryset().prefetch_related(
#     #         'songs'
#     #     )
#
#     def get_instances_from_related(self, related_instance):
#         if isinstance(related_instance, Song):
#             return related_instance.albums.all()
#
#
# from django_elasticsearch_dsl import (
#     Document,
#     fields,
# )
# from django_elasticsearch_dsl.registries import registry
# from factory.django import get_model
#
# Artist = get_model('media', 'Artist')
#
#
# @registry.register_document
# class ArtistDocument(Document):
#     id = fields.IntegerField(attr='id')
#     stage_name = fields.TextField(
#         attr='stage_name',
#         fields={
#             'suggest': fields.Completion(),
#         }
#     )
#
#     class Meta:
#         doc_type = 'artist_document'
#
#     class Index:
#         name = 'artists'
#         doc_type = 'artist_document'
#
#     class Django:
#         model = Artist
#         fields = ['photo']
#         related_models = [Song]
#
#     def get_instances_from_related(self, related_instance):
#         if isinstance(related_instance, Song):
#             return related_instance.artists.all()
