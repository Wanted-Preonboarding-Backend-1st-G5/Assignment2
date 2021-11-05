import json

from neomodel import (
                StructuredNode, StringProperty, RelationshipTo,
                 One, RelationshipFrom, OneOrMore
                )


class Song(StructuredNode):
    name     = StringProperty(unique_index=True)
    album    = RelationshipTo('Album', 'belongsto', cardinality=One)
    musician = RelationshipTo('Musician', 'writtenby', cardinality=OneOrMore)

    def to_dictionary(self):
        return json.loads(json.dumps(self.__properties__, ensure_ascii=False))


class Album(StructuredNode):
    name = StringProperty(unique_index=True)
    song = RelationshipFrom('Song', 'belongsto', cardinality=OneOrMore)

    def to_dictionary(self):
        return json.loads(json.dumps(self.__properties__, ensure_ascii=False))


class Musician(StructuredNode):
    name = StringProperty(unique_index=True)
    song = RelationshipFrom('Song', 'writtenby', cardinality=OneOrMore)

    def to_dictionary(self):
        return json.loads(json.dumps(self.__properties__, ensure_ascii=False))
