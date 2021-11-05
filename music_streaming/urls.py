from django.urls import path, include
from rest_framework.routers import SimpleRouter

from music_streaming.views import AlbumViewSet, MusicianViewSet

app_name = 'music_streaming'

router = SimpleRouter()

router.register('albums', AlbumViewSet, basename='albums')
# router.register('songs', SongViewSet, basename='songs')
router.register('musicians', MusicianViewSet, basename='musicians')

urlpatterns = [
    path('', include((router.urls, 'music_streaming'))),

]
