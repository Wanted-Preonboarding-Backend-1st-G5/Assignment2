from rest_framework              import status, viewsets
from rest_framework.decorators   import action
from rest_framework.response     import Response
from rest_framework.permissions  import IsAuthenticated, AllowAny

from music_streaming.models      import Album, Musician
from music_streaming.serializers import AlbumSerializer, MusicianSerializer, SongSerializer


class AlbumViewSet(viewsets.GenericViewSet):
    permission_classes = [AllowAny]

    def create(self, request):
        """
        POST /albums/

        data params
        - name(required)
        """
        name = request.data.get('name')
        if name is None:
            return Response({'error': 'name field is required.'}, status=status.HTTP_400_BAD_REQUEST)
        album = Album(name=name).save()
        rtn = AlbumSerializer(album).data
        return Response(rtn, status=status.HTTP_201_CREATED)

    def list(self, request):
        """
        GET /albums/
        """
        albums = Album.nodes.all()
        rtn = AlbumSerializer(albums, many=True).data
        return Response(rtn, status=status.HTTP_200_OK)

    def retrieve(self, request, pk):
        """
        GET /albums/{album_id}/
        """
        album = Album.nodes.get_or_none(uuid=pk)
        if album is None:
            return Response({'error': 'DoesNotExist'})
        rtn = AlbumSerializer(album).data
        return Response(rtn, status=status.HTTP_200_OK)

    def partial_update(self, request, pk):
        """
        PATCH /albums/{album_id}/

        data params
        - name(required)
        """
        album = Album.nodes.get_or_none(uuid=pk)
        album.delete()
        name = request.data.get('name')
        if name is None:
            return Response({'error': 'name field is required.'}, status=status.HTTP_400_BAD_REQUEST)
        album = Album(name=name).save()
        rtn = AlbumSerializer(album).data
        return Response(rtn, status=status.HTTP_200_OK)

    def destroy(self, request, pk):
        """
        DELETE /albums/{album_id}/
        """
        album = Album.nodes.get_or_none(uuid=pk)
        album.delete()
        return Response(status=status.HTTP_200_OK)

    @action(detail=True, methods=['GET'])
    def songs(self, request, pk):
        """
        GET /albums/{album_id}/songs/
        """
        album = Album.nodes.get_or_none(uuid=pk)
        if album is None:
            return Response({'error': 'DoesNotExist'})
        songs = album.song.all()
        rtn = SongSerializer(songs, many=True).data
        return Response(rtn, status=status.HTTP_200_OK)
    
    @action(detail=True, methods=['GET'])
    def musicians(self, request, pk):
        """
        GET /albums/{album_id}/musicians/
        """
        album = Album.nodes.get_or_none(uuid=pk)
        if album is None:
            return Response({'error': 'DoesNotExist'})
        query = f'''
            MATCH (a:Album {{uuid:'{pk}'}})<-[*]-(s:Song)-[*]->(m:Musician) return DISTINCT m
        '''
        rtn, meta = neomodel.db.cypher_query(query)
        musicians = [Musician.inflate(row[0]) for row in rtn]
        return Response(MusicianSerializer(musicians, many=True).data)

class MusicianViewSet(viewsets.GenericViewSet):
    permission_classes = [AllowAny]

    def create(self, request):
        """
        POST /musicians/

        data params
        - name(required)
        """
        name = request.data.get('name')
        if name is None:
            return Response({'error':'name field is required.'},status=status.HTTP_400_BAD_REQUEST)
        musician = Musician(name=name).save()
        rtn = MusicianSerializer(musician).data
        return Response(rtn, status=status.HTTP_201_CREATED)

    def list(self, request):
        """
        GET /musicians/

        """
        musicians = Musician.nodes.all()
        rtn = MusicianSerializer(musicians, many=True).data
        return Response(rtn, status=status.HTTP_200_OK)

    def retrieve(self, request, pk):
        """
        GET /musicians/{musician_id}/
        """
        musician = Musician.nodes.get_or_none(uuid=pk)
        if musician is None:
            return Response({'error': 'DoesNotExist'})
        rtn = MusicianSerializer(musician).data
        return Response(rtn, status=status.HTTP_200_OK)

    def partial_update(self, request, pk):
        """
        PATCH /musicians/{musician_id}/

        data params
        - name(required)
        """
        musician = Musician.nodes.get_or_none(uuid=pk)
        musician.delete()
        name = request.data.get('name')
        if name is None:
            return Response({'error': 'name field is required.'}, status=status.HTTP_400_BAD_REQUEST)
        musician = Musician(name=name).save()
        rtn = MusicianSerializer(musician).data
        return Response(rtn, status=status.HTTP_200_OK)

    def destroy(self, request, pk):
        """
        DELETE /musicians/{musician_id}/
        """
        musician = Musician.nodes.get_or_none(uuid=pk)
        musician.delete()
        return Response(status=status.HTTP_200_OK)
    
    @action(detail=True, methods=['GET'])
    def albums(self, request, pk):
        """
        GET /musicians/{musician_id}/albums/
        """
        musician = Musician.nodes.get_or_none(uuid=pk)
        if musician is None:
            return Response({'error': 'DoesNotExist'})
        albums = musicians.album.all()
        rtn = AlbumSerializer(albums, many=True).data
        return Response(rtn, status=status.HTTP_200_OK)

class SongViewSet(viewsets.GenericViewSet):
    permission_classes = [AllowAny]

    def create(self, request):
        """
        POST /songs/
        data params
        - name(required)
        """
        name = request.data.get('name')
        if name is None:
            return Response({'error':'name field is required.'},status=status.HTTP_400_BAD_REQUEST)
        song = Song(name=name).save()
        rtn = SongSerializer(song).data
        return Response(rtn, status=status.HTTP_201_CREATED)
    
    def list(self, request):
        """
        GET /albums/
        """
        songs = Song.nodes.all()
        rtn = SongSerializer(songs, many=True).data
        return Response(rtn, status=status.HTTP_201_CREATED)

    def destroy(self, request, pk):
        """
        DELETE /songs/{songs_id}/
        """
        song = Song.nodes.get(uuid=pk)
        song.delete()
        return Response(status=status.HTTP_200_OK)
    
    @action(detail=True, methods=['GET'])
    def albums(self, request, pk):
        """
        GET /songs/{song_id}/albums/
        """
        song = Song.nodes.get_or_none(uuid=pk)
        if song is None:
            return Response({'error': 'DoesNotExist'})
        albums = song.album.all()
        rtn = AlbumSerializer(albums, many=True).data
        return Response(rtn, status=status.HTTP_200_OK)
