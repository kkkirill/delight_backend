from rest_framework import routers

from apps.media.views.album import AlbumListView
from apps.media.views.artist import ArtistListView
from apps.media.views.genre import GenreListView
from apps.media.views.song import SongListView

router = routers.DefaultRouter()
router.register('genre', GenreListView)
router.register('artist', ArtistListView)
router.register('album', AlbumListView)
router.register('song', SongListView)
