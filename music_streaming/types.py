import strawberry


@strawberry.type
class SongType:
    id : int
    name: str


@strawberry.type
class AlbumType:
    id : int
    name: str


@strawberry.type
class MusicianType:
    id : int
    name: str