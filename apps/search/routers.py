from rest_framework import routers

from apps.search.views.album import AlbumDocumentView
from apps.search.views.artist import ArtistDocumentView
from apps.search.views.playlist import PlaylistDocumentView
from apps.search.views.song import SongDocumentView
from apps.search.views.user import UserDocumentView

router = routers.DefaultRouter()
router.register('album', AlbumDocumentView, basename='album')
router.register('artist', ArtistDocumentView, basename='artist')
router.register('playlist', PlaylistDocumentView, basename='playlist')
router.register('song', SongDocumentView, basename='song')
router.register('user', UserDocumentView, basename='user')
