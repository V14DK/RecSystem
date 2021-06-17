from neomodel import (StructuredNode, StringProperty,
                        UniqueIdProperty, RelationshipTo, RelationshipFrom)

class Type(StructuredNode):
    type = StringProperty(unique_index=True, required=True)

class Category(StructuredNode):
    name = StringProperty(unique_index=True, required=True)

class Movie(StructuredNode):
    title = StringProperty(unique_index=True, required=True)
    m_type = RelationshipTo(Type, 'TYPED_AS')
    category = RelationshipTo(Category, 'IN_CATEGORY')

class Person(StructuredNode):
    name = StringProperty(unique_index=True, required=True)
    movie = RelationshipTo(Movie, 'ACTED_IN')