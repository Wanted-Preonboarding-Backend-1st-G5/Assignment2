import json

from neomodel import (
                StructuredNode, StringProperty, RelationshipTo,
                 One, RelationshipFrom, OneOrMore, UniqueIdProperty
                )


class Song(StructuredNode):
    uuid     = UniqueIdProperty()
    name     = StringProperty()
    album    = RelationshipTo('Album', 'belongsto', cardinality=One)
    musician = RelationshipTo('Musician', 'writtenby', cardinality=OneOrMore)

    def to_dictionary(self):
        return json.loads(json.dumps(self.__properties__, ensure_ascii=False))


class Album(StructuredNode):
    uuid = UniqueIdProperty()
    name = StringProperty()
    song = RelationshipFrom('Song', 'belongsto', cardinality=OneOrMore)

    def to_dictionary(self): 
        return json.loads(json.dumps(self.__properties__, ensure_ascii=False))


class Musician(StructuredNode):
    uuid = UniqueIdProperty()
    name = StringProperty()
    song = RelationshipFrom('Song', 'writtenby', cardinality=OneOrMore)

    def to_dictionary(self): 
        return json.loads(json.dumps(self.__properties__, ensure_ascii=False))
