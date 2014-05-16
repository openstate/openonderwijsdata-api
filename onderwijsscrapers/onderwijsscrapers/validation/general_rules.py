from colander import (MappingSchema, SequenceSchema, SchemaNode, String,
                      Length, Range, Int, url, Date, Invalid, Float)
from datetime import datetime, date


def date_today_or_earlier(node, value):
    today = date.today()

    if today < value:
        raise Invalid(node, '%s is a date in the future' % value)


board_id = SchemaNode(Int())
branch_id = SchemaNode(Int(), validator=Range(min=0, max=1000))
collaboration_id = SchemaNode(String(), validator=Length(min=1, max=20))
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
reference_url = url
year = SchemaNode(Int(), validator=Range(min=1990, max=datetime.now().year))
corop_area = SchemaNode(String(), validator=Length(min=3, max=300))
corop_area_code = SchemaNode(Int())
education_area = SchemaNode(String(), validator=Length(min=5, max=100))
education_area_code = SchemaNode(Int())
nodal_area = SchemaNode(String(), validator=Length(min=3, max=300))
nodal_area_code = SchemaNode(Int())
rmc_region = SchemaNode(String(), validator=Length(min=3, max=300))
rmc_region_code = SchemaNode(Int())
rpa_area = SchemaNode(String(), validator=Length(min=3, max=300))
rpa_area_code = SchemaNode(Int())
wgr_area = SchemaNode(String(), validator=Length(min=3, max=300))
wgr_area_code = SchemaNode(Int())
city = SchemaNode(String(), validator=Length(min=3, max=300))
publication_date = SchemaNode(Date(), validator=date_today_or_earlier)


class Coordinates(MappingSchema):
    lat = SchemaNode(Float(), validator=Range(min=-180.0, max=180.0))
    lon = SchemaNode(Float(), validator=Range(min=-180.0, max=180.0))


class Viewport(MappingSchema):
    northeast = Coordinates()
    southwest = Coordinates()


class AddressComponentTypes(SequenceSchema):
    address_type = SchemaNode(String(), validator=Length(min=4, max=100))


class AddressComponent(MappingSchema):
    long_name = SchemaNode(String(), validator=Length(min=4, max=300))
    short_name = SchemaNode(String(), validator=Length(min=4, max=300))
    types = AddressComponentTypes()


class AddressComponents(SequenceSchema):
    address_component = AddressComponent()


class Address(MappingSchema):
    street = SchemaNode(String(), validator=Length(min=4, max=300))
    city = city
    zip_code = SchemaNode(String(), validator=Length(min=6, max=6))
    geo_location = Coordinates()
    geo_viewport = Viewport()
    formatted_address = SchemaNode(String(), validator=Length(min=3, max=300))
    address_components = AddressComponents()


class EducationStructures(SequenceSchema):
    structure = SchemaNode(String())


#TODO:
#class FinancialKeyIndicatorsPerYear


#TODO:
#class AgesPerBranchByStudentWeight


#TODO:
#class WeightsPerSchool


#TODO:
#class EduTypes


#TODO:
#class PupilsByOrigins
