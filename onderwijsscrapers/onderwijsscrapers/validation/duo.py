from glob import glob
import json
from colander import (MappingSchema, SequenceSchema, SchemaNode, String, Int,
                      Length, Range, Date, url, Invalid)

from general_rules import Address


class Dropout(MappingSchema):
    year = SchemaNode(Int(), validator=Range(min=1990, max=2013))
    dropouts_with_vmbo1_dimploma = SchemaNode(Int(), validator=Range(min=0,
        max=5000))
    dropouts_with_vmbo_diploma = SchemaNode(Int(), validator=Range(min=0,
        max=5000))
    dropouts_without_diploma = SchemaNode(Int(), validator=Range(min=0,
        max=5000))
    education_structure = SchemaNode(String(), validator=Length(min=3, max=75))
    total_dropouts = SchemaNode(Int(), validator=Range(min=0, max=5000))
    total_students = SchemaNode(Int(), validator=Range(min=0, max=5000))


class Dropouts(SequenceSchema):
    dropout = Dropout()


class EducationStructures():
    structure = SchemaNode(String())


class DuoVoSchool(MappingSchema):
    name = SchemaNode(String(), validator=Length(min=4, max=300))
    brin = SchemaNode(String(), validator=Length(min=4, max=4))
    board_id = SchemaNode(Int())
    address = Address()
    correspondence = Address()
    corop_area = SchemaNode(String(), validator=Length(min=3, max=300))
    corop_area_code = SchemaNode(Int())
    denomination = SchemaNode(String(), validator=Length(min=5, max=150))
    dropouts = Dropouts(missing=True)
    dropouts_reference_date = SchemaNode(Date(), missing=True)
    education_area = SchemaNode(String(), validator=Length(min=5, max=100))
    education_area_code = SchemaNode(Int())
    education_structures = EducationStructures()
    municipality = SchemaNode(String(), validator=Length(min=3, max=300))
    municipality_code = SchemaNode(Int())
    nodal_area = SchemaNode(String(), validator=Length(min=3, max=300))
    nodal_area_code = SchemaNode(Int())
    phone = SchemaNode(String(), validator=Length(min=10, max=15))
    province = SchemaNode(String(), validator=Length(min=5, max=100))
    reference_year = SchemaNode(Int(), validator=Range(min=1990, max=2013))
    rmc_region = SchemaNode(String(), validator=Length(min=3, max=300))
    rmc_region_code = SchemaNode(Int())
    rpa_area = SchemaNode(String(), validator=Length(min=3, max=300))
    rpa_area_code = SchemaNode(Int())
    website = SchemaNode(String(), validator=url)
    wgr_area = SchemaNode(String(), validator=Length(min=3, max=300))
    wgr_area_code = SchemaNode(Int())


if __name__ == '__main__':
    schema = DuoVoSchool()

    for path in glob('../onderwijsscrapers/onderwijsscrapers/export/duo_vo_schools/*.json'):
        print path
        data = json.load(open(path, 'r'))
        try:
            schema.deserialize(data)
        except Invalid, e:
            errors = e.asdict()
            print errors

