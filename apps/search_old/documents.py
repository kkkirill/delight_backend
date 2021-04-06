from elasticsearch_dsl import Document
from apps.search_old.document_files.album import AlbumDocument
from apps.search_old.document_files.song import SongDocument
from apps.search_old.document_files.artist import ArtistDocument


class GlobalDocument(Document):
    class Meta:
        index = ['albums', 'artists', 'songs']

    class Django:
        model = None

# from elasticsearch import Elasticsearch
# client = Elasticsearch(hosts=['elasticsearch:9200'])

# search_old = GlobalDocument.search_old()

# from django_elasticsearch_dsl_drf.helpers import more_like_this
# more_like_this()
