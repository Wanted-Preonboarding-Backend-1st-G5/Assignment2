import neomodel

from rest_framework              import status, viewsets
from rest_framework.decorators   import action
from rest_framework.response     import Response
from rest_framework.permissions  import IsAuthenticated, AllowAny
from rest_framework.exceptions   import ValidationError
from drf_yasg                    import openapi
from drf_yasg.utils              import swagger_auto_schema

from drf_yasg                    import openapi
from drf_yasg.utils              import swagger_auto_schema

from music_streaming.models      import Album, Musician, Song
from music_streaming.serializers import AlbumSerializer, MusicianSerializer, SongSerializer


class AlbumViewSet(viewsets.GenericViewSet):
    permission_classes = [AllowAny]

    @swagger_auto_schema (
        responses         = {
            "200": AlbumSerializer,
            "404": "NOT_FOUND",
        },
        operation_id          = "앨범 생성",
        operation_description = "새 앨범을 생성합니다"
    )
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

    @swagger_auto_schema (
        responses         = {
            "200": AlbumSerializer,
            "404": "NOT_FOUND",
        },
        operation_id          = "앨범 리스트 조회",
        operation_description = "모든 앨범 리스트를 조회합니다"
    )
    def list(self, request):
        """
        GET /albums/
        """
        albums = Album.nodes.all()
        rtn = AlbumSerializer(albums, many=True).data
        return Response(rtn, status=status.HTTP_200_OK)

    @swagger_auto_schema (
        responses         = {
            "200": AlbumSerializer,
            "404": "NOT_FOUND",
        },
        operation_id          = "앨범 조회",
        operation_description = "특정 앨범을 조회합니다"
    )
    def retrieve(self, request, pk):
        """
        GET /albums/{album_id}/
        """
        album = Album.nodes.get_or_none(uuid=pk)
        if album is None:
            return Response({'error': 'DoesNotExist'})
        rtn = AlbumSerializer(album).data
        return Response(rtn, status=status.HTTP_200_OK)

    @swagger_auto_schema (
        responses         = {
            "200": AlbumSerializer,
            "404": "NOT_FOUND",
        },
        operation_id          = "앨범 삭제",
        operation_description = "특정 앨범을 삭제합니다"
    )
    def destroy(self, request, pk):
        """
        DELETE /albums/{album_id}/
        """
        album = Album.nodes.get_or_none(uuid=pk)
        album.delete()
        return Response(status=status.HTTP_200_OK)

    @swagger_auto_schema (
        responses         = {
            "200": SongSerializer,
            "404": "NOT_FOUND",
        },
        operation_id          = "앨범의 곡들 조회",
        operation_description = "특정 앨범의 곡들을 조회합니다"
    )
    @action(detail=True, methods=['GET'])
    def songs(self, request, pk):
        """
        GET /albums/{album_id}/songs/
        """
        album = Album.nodes.get_or_none(uuid=pk)
        if album is None:
            return Response({'error': 'DoesNotExist'}, status=status.HTTP_400_BAD_REQUEST)
        songs = album.song.all()
        rtn = SongSerializer(songs, many=True).data
        return Response(rtn, status=status.HTTP_200_OK)
    
    @swagger_auto_schema (
        responses         = {
            "200": MusicianSerializer,
            "404": "NOT_FOUND",
        },
        operation_id          = "앨범의 뮤지션들 조회",
        operation_description = "특정 앨범의 뮤지션들을 곡을 통해서 조회합니다"
    )
    @action(detail=True, methods=['GET'])
    def musicians(self, request, pk):
        """
        GET /albums/{album_id}/musicians/
        """
        album = Album.nodes.get_or_none(uuid=pk)
        if album is None:
            return Response({'error': 'DoesNotExist'}, status=status.HTTP_400_BAD_REQUEST)
        query = f'''
            MATCH (a:Album {{uuid:'{pk}'}})<-[*]-(s:Song)-[*]->(m:Musician) return DISTINCT m
        '''
        rtn, meta = neomodel.db.cypher_query(query)
        musicians = [Musician.inflate(row[0]) for row in rtn]
        return Response(MusicianSerializer(musicians, many=True).data)

class MusicianViewSet(viewsets.GenericViewSet):
    permission_classes = [AllowAny]

    @swagger_auto_schema (
        responses         = {
            "200": MusicianSerializer,
            "404": "NOT_FOUND",
        },
        operation_id          = "뮤지션 생성",
        operation_description = "새 뮤지션을 생성합니다"
    )
    def create(self, request):
        """
        POST /musicians/

        data params
        - name(required)
        """
        name = request.data.get('name')
        if name is None:
            return Response({'error': 'name field is required.'},status=status.HTTP_400_BAD_REQUEST)
        musician = Musician(name=name).save()
        rtn = MusicianSerializer(musician).data
        return Response(rtn, status=status.HTTP_201_CREATED)

    @swagger_auto_schema (
        responses         = {
            "200": MusicianSerializer,
            "404": "NOT_FOUND",
        },
        operation_id          = "뮤지션 리스트 조회",
        operation_description = "모든 뮤지션 리스트를 조회합니다"
    )
    def list(self, request):
        """
        GET /musicians/

        """
        musicians = Musician.nodes.all()
        rtn = MusicianSerializer(musicians, many=True).data
        return Response(rtn, status=status.HTTP_200_OK)

    @swagger_auto_schema (
        responses         = {
            "200": MusicianSerializer,
            "404": "NOT_FOUND",
        },
        operation_id          = "뮤지션 조회",
        operation_description = "특정 뮤지션을 조회합니다"
    )
    def retrieve(self, request, pk):
        """
        GET /musicians/{musician_id}/
        """
        musician = Musician.nodes.get_or_none(uuid=pk)
        if musician is None:
            return Response({'error': 'DoesNotExist'})
        rtn = MusicianSerializer(musician).data
        return Response(rtn, status=status.HTTP_200_OK)

    @swagger_auto_schema (
        responses         = {
            "200": MusicianSerializer,
            "404": "NOT_FOUND",
        },
        operation_id          = "뮤지션 삭제",
        operation_description = "뮤지션을 삭제합니다"
    )
    def destroy(self, request, pk):
        """
        DELETE /musicians/{musician_id}/
        """
        musician = Musician.nodes.get_or_none(uuid=pk)
        musician.delete()
        return Response(status=status.HTTP_200_OK)
    
    @swagger_auto_schema (
        responses         = {
            "200": SongSerializer,
            "404": "NOT_FOUND",
        },
        operation_id          = "뮤지션의 곡들 조회",
        operation_description = "특정 뮤지션의 곡들을 조회합니다"
    )
    @action(detail=True, methods=['GET'])
    def songs(self, request, pk):
        """
        GET /musicians/{musician_id}/songs/
        """
        musician = Musician.nodes.get_or_none(uuid=pk)
        if musician is None:
            return Response({'error': 'DoesNotExist'})
        songs = musician.song.all()
        rtn = SongSerializer(songs, many=True).data
        return Response(rtn, status=status.HTTP_200_OK)
    
    @swagger_auto_schema (
        responses         = {
            "200": AlbumSerializer,
            "404": "NOT_FOUND",
        },
        operation_id          = "뮤지션의 앨범들 조회",
        operation_description = "특정 뮤지션의 앨범들을 곡을 통해서 조회합니다"
    )
    @action(detail=True, methods=['GET'])
    def albums(self, request, pk):
        """
        GET /musicians/{musician_id}/albums/
        """
        musician = Musician.nodes.get_or_none(uuid=pk)
        if musician is None:
            return Response({'error': 'DoesNotExist'})
        query = f'''
            MATCH (a:Musician {{uuid:'{pk}'}})<-[*]-(s:Song)-[*]->(m:Album) return DISTINCT m
        '''
        rtn, meta = neomodel.db.cypher_query(query)
        albums = [Album.inflate(row[0]) for row in rtn]
        return Response(AlbumSerializer(albums, many=True).data)


class SongViewSet(viewsets.GenericViewSet):
    permission_classes = [AllowAny]

    @swagger_auto_schema (
        responses         = {
            "200": MusicianSerializer,
            "404": "NOT_FOUND",
        },
        operation_id          = "곡 생성",
        operation_description = "새 곡을 생성합니다"
    )
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
    
    @swagger_auto_schema (
        responses         = {
            "200": SongSerializer,
            "404": "NOT_FOUND",
        },
        operation_id          = "곡 리스트 조회",
        operation_description = "모든 곡 리스트를 조회합니다"
    )
    def list(self, request):
        """
        GET /songs/
        """
        songs = Song.nodes.all()
        rtn = SongSerializer(songs, many=True).data
        return Response(rtn, status=status.HTTP_201_CREATED)
    
    @swagger_auto_schema (
        responses         = {
            "200": SongSerializer,
            "404": "NOT_FOUND",
        },
        operation_id          = "곡 조회",
        operation_description = "특정 곡을 조회합니다"
    )
    def retrieve(self, request, pk):
        """
        GET /songs/{songs_id}/
        """
        song = Song.nodes.get_or_none(uuid=pk)
        if song is None:
            return Response({'error': 'DoesNotExist'})
        rtn = AlbumSerializer(song).data
        return Response(rtn, status=status.HTTP_200_OK)

    @swagger_auto_schema (
        responses         = {
            "200": SongSerializer,
            "404": "NOT_FOUND",
        },
        operation_id          = "곡 삭제",
        operation_description = "곡을 삭제합니다"
    )
    def destroy(self, request, pk):
        """
        DELETE /songs/{songs_id}/
        """
        song = Song.nodes.get(uuid=pk)
        song.delete()
        return Response(status=status.HTTP_200_OK)
    
    @swagger_auto_schema (
        responses         = {
            "200": AlbumSerializer,
            "404": "NOT_FOUND",
        },
        operation_id          = "곡의 앨범 조회",
        operation_description = "특정 곡의 앨범을 조회합니다"
    )
    @action(detail=True, methods=['GET'])
    def albums(self, request, pk):
        """
        GET /songs/{song_id}/album/
        """
        song = Song.nodes.get_or_none(uuid=pk)
        if song is None:
            return Response({'error': 'DoesNotExist'})
        albums = song.album.all()
        rtn = AlbumSerializer(albums, many=True).data
        return Response(rtn, status=status.HTTP_200_OK)
    
    @swagger_auto_schema (
        responses         = {
            "200": AlbumSerializer,
            "404": "NOT_FOUND",
        },
        operation_id          = "곡의 뮤지션들 조회",
        operation_description = "특정 곡의 뮤지션들을 조회합니다"
    )
    @action(detail=True, methods=['GET'])
    def musicians(self, request, pk):
        """
        GET /songs/{song_id}/musicians/
        """
        song = Song.nodes.get_or_none(uuid=pk)
        if song is None:
            return Response({'error': 'DoesNotExist'})
        musicians = song.musician.all()
        rtn = MusicianSerializer(musicians, many=True).data
        return Response(rtn, status=status.HTTP_200_OK)

class ConnectionViewSet(viewsets.GenericViewSet):
    permission_classes = [AllowAny]

    def validate_connect_params(self, request):
        # return: (album:uuid, musician:uuid, song:uuid)
        song = request.data.get('song')
        album = request.data.get('album')
        musician = request.data.get('musician')

        if song and album and musician is None:
            return album, None, song
        if song and musician and not album:
            return None, musician, song
        else:
            raise ValidationError({'error': 'should be (song and album) or (song and musician)'})

    def get_connection_targets(self, request):
        # return: {Album_or_Musician}, {Song}
        album, musician, song = self.validate_connect_params(request)
        if album:
            target = Album.nodes.get_or_none(uuid=album)
        if musician:
            target = Musician.nodes.get_or_none(uuid=musician)
        song = Song.nodes.get_or_none(uuid=song)
        if target is None or song is None:
            raise ValidationError({'error': 'DoesNotExist'})
        return target, song

    def create(self, request):
        """
        POST /connections/

        data params
        - case1 : song and album
        - case2:  song and musician
        """
        target, song = self.get_connection_targets(request)
        if target.song.connect(song):
            return Response({'success': f'{target.name} and {song.name} connected'}, status=status.HTTP_201_CREATED)

    @action(methods=['DELETE'], detail=False)
    def dis(self, request):
        """
        DELETE /connections/dis/

        data params
        - case1 : song and album
        - case2:  song and musician
        """
        target, song = self.get_connection_targets(request)
        target.song.disconnect(song)
        return Response(status=status.HTTP_200_OK)
