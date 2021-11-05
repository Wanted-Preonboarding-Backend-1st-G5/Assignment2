from enum import unique
import strawberry


@strawberry.type
class SongType:
    uuid : str
    name : str


@strawberry.type
class AlbumType:
    uuid : str
    name : str


@strawberry.type
class MusicianType:
    uuid : str
    name : str