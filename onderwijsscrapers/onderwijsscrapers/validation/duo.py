from glob import glob
import json
from colander import (MappingSchema, SequenceSchema, SchemaNode, String, Int,
                      Length, Range, Date, url, Invalid)

import general_rules


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


class DuoVoSchool(MappingSchema):
    address = general_rules.Address()
    correspondence_address = general_rules.Address()
    board_id = general_rules.board_id
    denomination = general_rules.denomination
    corop_area = SchemaNode(String(), validator=Length(min=3, max=300))
    corop_area_code = SchemaNode(Int())
    dropouts = Dropouts(missing=True)
    dropouts_reference_date = SchemaNode(Date(), missing=True)
    education_area = SchemaNode(String(), validator=Length(min=5, max=100))
    education_area_code = SchemaNode(Int())
    education_structures = general_rules.EducationStructures()
    municipality = general_rules.municipality
    municipality_code = general_rules.municipality_code
    nodal_area = SchemaNode(String(), validator=Length(min=3, max=300))
    nodal_area_code = SchemaNode(Int())
    phone = general_rules.phone
    province = general_rules.province
    reference_year = SchemaNode(Int(), validator=Range(min=1990, max=2013))
    rmc_region = SchemaNode(String(), validator=Length(min=3, max=300))
    rmc_region_code = SchemaNode(Int())
    rpa_area = SchemaNode(String(), validator=Length(min=3, max=300))
    rpa_area_code = SchemaNode(Int())
    website = general_rules.url
    wgr_area = SchemaNode(String(), validator=Length(min=3, max=300))
    wgr_area_code = SchemaNode(Int())


if __name__ == '__main__':
    schema = DuoVoSchool()

    for path in glob('../export/duo_vo_schools/*.json'):
        print path
        data = json.load(open(path, 'r'))
        try:
            schema.deserialize(data)
        except Invalid, e:
            errors = e.asdict()
            print errors

