from neomodel import (
                StructuredNode, StringProperty, RelationshipTo,
                 One, RelationshipFrom, OneOrMore
                )


class Song(StructuredNode):
    name     = StringProperty(unique_index=True)
    album    = RelationshipTo('Album', 'belongsto', cardinality=One)
    musician = RelationshipTo('Musician', 'writtenby', cardinality=OneOrMore)


class Album(StructuredNode):
    name = StringProperty(unique_index=True)
    song = RelationshipFrom('Song', 'belongsto', cardinality=OneOrMore)


class Musician(StructuredNode):
    name = StringProperty(unique_index=True)
    song = RelationshipFrom('Song', 'writtenby', cardinality=OneOrMore)