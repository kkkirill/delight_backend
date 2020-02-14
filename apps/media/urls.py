from django.urls import path
from apps.media.views.artist import ArtistCreateView, ArtistListView, ArtistUpdateDestroyView
from apps.media.views.album import AlbumCreateView, AlbumListView, AlbumUpdateDestroyView
from apps.media.views.genre import GenreCreateView, GenreListView, GenreUpdateDestroyView
from apps.media.views.song import SongCreateView, SongListView, SongUpdateDestroyView


app_name = 'media'
urlpatterns = [
    path('genre/create/', GenreCreateView.as_view()),
    path('genre/<int:pk>/', GenreUpdateDestroyView.as_view()),
    path('genre/', GenreListView.as_view()),
    path('artist/create/', ArtistCreateView.as_view()),
    path('artist/<int:pk>/', ArtistUpdateDestroyView.as_view()),
    path('artist/', ArtistListView.as_view()),
    path('album/create/', AlbumCreateView.as_view()),
    path('album/<int:pk>/', AlbumUpdateDestroyView.as_view()),
    path('album/', AlbumListView.as_view()),
    path('song/create/', SongCreateView.as_view()),
    path('song/<int:pk>/', SongUpdateDestroyView.as_view()),
    path('song/', SongListView.as_view()),
]
