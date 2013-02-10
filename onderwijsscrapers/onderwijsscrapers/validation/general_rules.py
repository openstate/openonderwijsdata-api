from colander import MappingSchema, SchemaNode, String, Length


class Address(MappingSchema):
    street = SchemaNode(String(), validator=Length(min=4, max=300))
    city = SchemaNode(String(), validator=Length(min=3, max=300))
    zip_code = SchemaNode(String(), validator=Length(min=6, max=6))
