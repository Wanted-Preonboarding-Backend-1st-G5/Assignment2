import typing
import strawberry
from .types import AlbumType
from .models import Song


@strawberry.type
class Query:
    @strawberry.field
    def get_album_of_song(self, name: strawberry.ID) -> AlbumType:
        s = Song.nodes.get(name=name)
        a = s.album.get_or_none()
        return AlbumType(id=a.id, name=a.name)

schema = strawberry.Schema(query=Query)