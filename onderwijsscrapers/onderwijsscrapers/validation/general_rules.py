from colander import (MappingSchema, SequenceSchema, SchemaNode, String,
                      Length, Range, Int, Date, Invalid, Float)
from datetime import datetime, date
import colander


def date_today_or_earlier(node, value):
    today = date.today()

    if today < value:
        raise Invalid(node, '%s is a date in the future' % value)


board_id = lambda **kwargs: SchemaNode(Int(), **kwargs)
branch_id = lambda **kwargs: SchemaNode(Int(), validator=Range(min=0, max=1000), **kwargs)
collaboration_id = lambda **kwargs: SchemaNode(String(), validator=Length(min=1, max=20), **kwargs)
brin = lambda **kwargs: SchemaNode(String(), validator=Length(min=4, max=4), **kwargs)
name = lambda **kwargs: SchemaNode(String(), validator=Length(min=4, max=300), **kwargs)
phone = lambda **kwargs: SchemaNode(String(), validator=Length(min=10, max=15), **kwargs)
denomination = lambda **kwargs: SchemaNode(String(), validator=Length(min=5, max=150), **kwargs)
municipality = lambda **kwargs: SchemaNode(String(), validator=Length(min=3, max=300), **kwargs)
municipality_code = lambda **kwargs: SchemaNode(Int(), **kwargs)
province = lambda **kwargs: SchemaNode(String(), validator=Length(min=5, max=100), **kwargs)
website = lambda **kwargs: SchemaNode(String(), validator=colander.url, **kwargs)
education_structure = lambda **kwargs: SchemaNode(String(), validator=Length(min=3, max=75), **kwargs)
reference_year = lambda **kwargs: SchemaNode(Int(), validator=Range(min=1990, max=datetime.now().year), **kwargs)
reference_url = lambda **kwargs : lambda **kwargs: SchemaNode(String(), validator=colander.url , **kwargs)
year = lambda **kwargs: SchemaNode(Int(), validator=Range(min=1990, max=datetime.now().year), **kwargs)
corop_area = lambda **kwargs: SchemaNode(String(), validator=Length(min=3, max=300), **kwargs)
corop_area_code = lambda **kwargs: SchemaNode(Int(), **kwargs)
education_area = lambda **kwargs: SchemaNode(String(), validator=Length(min=5, max=100), **kwargs)
education_area_code = lambda **kwargs: SchemaNode(Int(), **kwargs)
nodal_area = lambda **kwargs: SchemaNode(String(), validator=Length(min=3, max=300), **kwargs)
nodal_area_code = lambda **kwargs: SchemaNode(Int(), **kwargs)
rmc_region = lambda **kwargs: SchemaNode(String(), validator=Length(min=3, max=300), **kwargs)
rmc_region_code = lambda **kwargs: SchemaNode(Int(), **kwargs)
rpa_area = lambda **kwargs: SchemaNode(String(), validator=Length(min=3, max=300), **kwargs)
rpa_area_code = lambda **kwargs: SchemaNode(Int(), **kwargs)
wgr_area = lambda **kwargs: SchemaNode(String(), validator=Length(min=3, max=300), **kwargs)
wgr_area_code = lambda **kwargs: SchemaNode(Int(), **kwargs)
city = lambda **kwargs: SchemaNode(String(), validator=Length(min=3, max=300), **kwargs)
publication_date = lambda **kwargs: SchemaNode(Date(), validator=date_today_or_earlier, **kwargs)
url = lambda **kwargs: SchemaNode(String(), validator=colander.url , **kwargs)

class Coordinates(MappingSchema):
    lat = SchemaNode(Float(), validator=Range(min=-180.0, max=180.0))
    lon = SchemaNode(Float(), validator=Range(min=-180.0, max=180.0))


class Viewport(MappingSchema):
    northeast = Coordinates()
    southwest = Coordinates()

class Address(MappingSchema):
    street = SchemaNode(String(), validator=Length(min=4, max=300))
    city = city
    zip_code = SchemaNode(String(), validator=Length(min=6, max=6))
    geo_location = Coordinates()
    geo_viewport = Viewport()
    formatted_address = SchemaNode(String(), validator=Length(min=3, max=300))

    @colander.instantiate()
    class address_components(SequenceSchema):
        @colander.instantiate()
        class address_component(MappingSchema):
            long_name = SchemaNode(String(), validator=Length(min=4, max=300))
            short_name = SchemaNode(String(), validator=Length(min=4, max=300))
            
            @colander.instantiate()
            class types(SequenceSchema):
                address_type = SchemaNode(String(), validator=Length(min=4, max=100))


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
