import typing
import strawberry
from neomodel import db

from .types  import AlbumType, SongType, MusicianType
from .models import Album, Musician, Song


@strawberry.type
class Query:
    @strawberry.field
    def get_musicians_of_song(self, uuid: str) -> typing.Optional[typing.List[MusicianType]]:
        try:
            song = Song.nodes.get(uuid=uuid)
            musicians = song.musician.all()
            return [MusicianType(**m.to_dictionary()) for m in musicians]
        except:
            return None

    @strawberry.field
    def get_album_of_song(self, uuid: str) -> typing.Optional[AlbumType]:
        try:
            s = Song.nodes.get(uuid=uuid)
            a = s.album.get_or_none()
            return AlbumType(uuid=a.uuid, name=a.name)
        except:
            return None


    @strawberry.field
    def get_song_of_album(self, uuid: str) -> typing.Optional[typing.List[SongType]]:
        try:
            album = Album.nodes.get(uuid=uuid)
            songs = album.song.all()
            return [SongType(**s.to_dictionary()) for s in songs]
        except:
            return None

    @strawberry.field
    def get_musician_of_album(self, uuid: str) -> typing.Optional[typing.List[MusicianType]]:
        try:
            results, _ = db.cypher_query(f'MATCH (a:Album {{uuid:"{uuid}"}})<-[*]-(s:Song)-[*]->(m:Musician) return DISTINCT m')
            musicians = [Musician.inflate(row[0]) for row in results]
            return [MusicianType(**m.to_dictionary()) for m in musicians]
        except:
            return None

    @strawberry.field
    def get_album_of_musician(self, uuid: str) -> typing.Optional[typing.List[AlbumType]]:
        try:
            results, _ = db.cypher_query(f'MATCH (m:Musician {{uuid:"{uuid}"}})<-[*]-(s:Song)-[*]->(a:Album) return DISTINCT a')
            albums = [Album.inflate(row[0]) for row in results]
            return [AlbumType(**a.to_dictionary()) for a in albums]
        except:
            return None

    @strawberry.field
    def get_song_of_musician(self, uuid: str) -> typing.Optional[typing.List[SongType]]:
        try:
            musician = Musician.nodes.get(uuid=uuid)
            songs = musician.song.all()
            return [SongType(**s.to_dictionary()) for s in songs]
        except:
            return None


schema = strawberry.Schema(query=Query)
