from colander import MappingSchema, SequenceSchema, SchemaNode, String, Length, Range, Int, url
from datetime import datetime

board_id = SchemaNode(Int())
branch_id = SchemaNode(Int(), validator=Range(min=0, max=1000))
brin = SchemaNode(String(), validator=Length(min=4, max=4))
name = SchemaNode(String(), validator=Length(min=4, max=300))
phone = SchemaNode(String(), validator=Length(min=10, max=15))
denomination = SchemaNode(String(), validator=Length(min=5, max=150))
municipality = SchemaNode(String(), validator=Length(min=3, max=300))
municipality_code = SchemaNode(Int())
province = SchemaNode(String(), validator=Length(min=5, max=100))
website = SchemaNode(String(), validator=url)
education_structure = SchemaNode(String(), validator=Length(min=3, max=75))
reference_year = SchemaNode(Int(), validator=Range(min=1990,
    max=datetime.now().year))
year = SchemaNode(Int(), validator=Range(min=1990, max=datetime.now().year))


class Address(MappingSchema):
    street = SchemaNode(String(), validator=Length(min=4, max=300))
    city = SchemaNode(String(), validator=Length(min=3, max=300))
    zip_code = SchemaNode(String(), validator=Length(min=6, max=6))


class EducationStructures(SequenceSchema):
    structure = SchemaNode(String())
