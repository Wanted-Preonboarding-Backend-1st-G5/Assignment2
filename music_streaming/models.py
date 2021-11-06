import json
from neomodel import (
                StructuredNode, StringProperty, RelationshipTo,
                 ZeroOrOne,ZeroOrMore, RelationshipFrom, UniqueIdProperty
                )


class Song(StructuredNode):
    uuid     = UniqueIdProperty()
    name     = StringProperty()
    album    = RelationshipTo('Album', 'belongsto', cardinality=ZeroOrOne)
    musician = RelationshipTo('Musician', 'writtenby', cardinality=ZeroOrMore)

    def to_dictionary(self): 
        data = json.loads(json.dumps(self.__properties__, ensure_ascii=False))
        if 'id' in data :
            data.pop('id')
        return data


class Album(StructuredNode):
    uuid = UniqueIdProperty()
    name = StringProperty()
    song = RelationshipFrom('Song', 'belongsto', cardinality=ZeroOrMore)

    def to_dictionary(self): 
        data = json.loads(json.dumps(self.__properties__, ensure_ascii=False))
        if 'id' in data :
            data.pop('id')
        return data


class Musician(StructuredNode):
    uuid = UniqueIdProperty()
    name = StringProperty()
    song = RelationshipFrom('Song', 'writtenby', cardinality=ZeroOrMore)

    def to_dictionary(self): 
        data = json.loads(json.dumps(self.__properties__, ensure_ascii=False))
        if 'id' in data :
            data.pop('id')
        return data