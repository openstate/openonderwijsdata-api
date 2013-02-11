import glob
import json

from colander import (MappingSchema, SequenceSchema, SchemaNode, String, Int,
                      Float, Boolean, Length, Range, Date, Email, url, Invalid,
                      OneOf)

import general_rules


class Coordinates(MappingSchema):
    lat = SchemaNode(Float(), validator=Range(min=-180.0, max=180.0))
    lon = SchemaNode(Float(), validator=Range(min=-180.0, max=180.0))


# Extension of default address format with geo-coordinates
class SchoolVOAddress(general_rules.Address):
    geo_location = Coordinates()


####################################
# Average education hours per year #
####################################
class PlannedRealisedHours(MappingSchema):
    # Approximately 9000 hours in a year
    hours_planned = SchemaNode(Int(), validator=Range(min=0, max=9000))
    hours_realised = SchemaNode(Int(), validator=Range(min=0, max=9000))


class PlannedRealisedHoursPerStructure(PlannedRealisedHours):
    structure = SchemaNode(String(), validator=Length(min=1, max=75))


class AverageEducationHoursPerStructure(SequenceSchema):
    average_hour_per_structure = PlannedRealisedHoursPerStructure()


class PlannedRealisedHoursPerYear(PlannedRealisedHours):
    # Year can be a bunch of things ("Leerjaar 1", "alle jaren", ...)
    year = SchemaNode(String(), validator=Length(min=3, max=75))
    per_structure = AverageEducationHoursPerStructure()


class AverageEducationHours(SequenceSchema):
    average_hour = PlannedRealisedHoursPerYear()


####################################
#               Costs              #
####################################
class CostPerYear(MappingSchema):
    amount_euro = SchemaNode(Int(), validator=Range(min=0, max=1000))
    explanation = SchemaNode(String())
    link = SchemaNode(String())
    other_costs = SchemaNode(String(), validator=OneOf(['Ja', 'Nee']))
    # Year can be a bunch of things ("Leerjaar 1", "alle jaren", ...)
    year = SchemaNode(String(), validator=Length(min=3, max=75))


class CostsPerYear(SequenceSchema):
    cost_per_year = CostPerYear()


class Documents(SequenceSchema):
    document = SchemaNode(String(), validator=url)


class Costs(MappingSchema):
    explanation = SchemaNode(String(), validator=Length(min=3, max=5000))
    documents = Documents()
    signed_code_of_conduct = SchemaNode(Boolean())
    per_year = CostsPerYear()


####################################
#   Parent/student satisfactions   #
####################################
class Indicator(MappingSchema):
    grade = SchemaNode(Float(), validator=Range(min=0.0, max=10.0))
    indicator = SchemaNode(String(), validator=Length(min=10, max=200))


class Indicators(SequenceSchema):
    indicator = Indicator()


class Satisfaction(MappingSchema):
    average_grade = SchemaNode(Float(), validator=Range(min=0.0, max=10.0))
    national_grade = SchemaNode(Float(), validator=Range(min=0.0, max=10.0))
    education_structure = SchemaNode(String(), validator=Length(min=3,\
        max=15))
    indicators = Indicators()


class Satisfactions(SequenceSchema):
    satisfaction = Satisfaction()


class SchoolVOBranch(MappingSchema):
    address = SchoolVOAddress()
    avg_education_hours_per_student = AverageEducationHours()
    avg_education_hours_per_student_url = SchemaNode(String(), validator=url)
    board = SchemaNode(String(), validator=Length(min=3, max=100))
    board_id = general_rules.board_id
    branch_id = general_rules.branch_id
    brin = general_rules.brin
    building_img_url = SchemaNode(String(), validator=url)
    costs = Costs()
    costs_url = SchemaNode(String(), validator=url)
    denomination = general_rules.denomination
    education_structures = general_rules.EducationStructures()
    email = SchemaNode(String(), validator=Email)
    logo_img_url = SchemaNode(String(), validator=url)
    municipality = general_rules.municipality
    municipality_id = general_rules.municipality_code
    name = general_rules.name
    parent_satisfaction = Satisfactions()
    parent_satisfaction_url = SchemaNode(String(), validator=url)
    phone = general_rules.phone
    profile = SchemaNode(String(), validator=Length(min=3, max=500))
    province = general_rules.province
    schoolkompas_status_id = SchemaNode(Int(), validator=Range(min=0,\
        max=1000))
    schoolvo_code = SchemaNode(String(), validator=Length(min=14, max=14))
    student_satisfaction = Satisfactions()
    student_satisfaction_url = SchemaNode(String(), validator=url)
    website = general_rules.website


if __name__ == '__main__':
    schema = SchoolVOBranch()

    for path in glob.glob('../export/schoolvo.nl/*.json'):
        # print path
        data = json.load(open(path, 'r'))
        try:
            schema.deserialize(data)
        except Invalid, e:
            errors = e.asdict()
            print errors, path
