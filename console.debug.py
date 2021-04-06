# from apps.search_old.documents.artist import ArtistDocument
from apps.search_old.documents.album import AlbumDocument
# from apps.search_old.documents.song import SongDocument

sa = AlbumDocument.search()
res = sa.query("match_all").execute()

