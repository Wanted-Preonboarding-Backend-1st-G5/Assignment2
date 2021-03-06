from django.urls import path, include
from rest_framework.routers import SimpleRouter

from music_streaming.views import AlbumViewSet, MusicianViewSet,\
    SongViewSet, ConnectionViewSet


app_name = 'music_streaming'

router = SimpleRouter()

router.register('albums', AlbumViewSet, basename='albums')
router.register('songs', SongViewSet, basename='songs')
router.register('musicians', MusicianViewSet, basename='musicians')
router.register('connections', ConnectionViewSet, basename='connections')

urlpatterns = [
    path('', include((router.urls, 'music_streaming'))),

]
