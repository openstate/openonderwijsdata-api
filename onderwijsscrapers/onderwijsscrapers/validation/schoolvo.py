""".. _schoolvodata:

Vensters voor Verantwoording
----------------------------
`Vensters voor Verantwoording <http://schoolvo.nl/>`_ provides VO schools with a platform where they can share data on their performance with the public. The data described here is currently **not** available to the public through the `OpenOnderwijs API <http://api.openonderwijsdata.nl/>`_.
"""

import glob
import json

from colander import (MappingSchema, SequenceSchema, SchemaNode, String, Int,
                      Float, Boolean, Length, Range, Date, Email, url, Invalid,
                      OneOf)

import general_rules


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
    amount_euro = SchemaNode(Int(), validator=Range(min=0, max=1000),  title="Costs in &euro; (euro) for this year.")
    explanation = SchemaNode(String(),  title="Optional explanation of the details of the costs (*for a labcoat, for travel, ...*)")
    link = SchemaNode(String(),  title="Optional URL to a document detailing costs.")
    other_costs = SchemaNode(Boolean(),  title="Indication whether parents should expect additional costs, other than the costs mentioned here.")
    # Year can be a bunch of things ("Leerjaar 1", "alle jaren", ...)
    year = SchemaNode(String(), validator=Length(min=3, max=75),  title="String representation of the years these costs apply to.")


class CostsPerYear(SequenceSchema):
    cost_per_year = CostPerYear()


class Documents(SequenceSchema):
    document = SchemaNode(String(), validator=url)


class Costs(MappingSchema):
    explanation = SchemaNode(String(), validator=Length(min=3, max=5000),  title="Optional explanation provided by the school.")
    documents = Documents( title="Array containing URLs (string) to documents the school published regarding the costs for parents.")
    signed_code_of_conduct = SchemaNode(Boolean(),  title="*True* if the school signed the code of conduct of the VO-raad [#voraad]_ regarding school costs [#coc]_.")
    per_year = CostsPerYear(title="Many schools provide a detailed overview of the costs per year, which are described in this array.")



####################################
#   Parent/student satisfactions   #
####################################
class Indicator(MappingSchema):
    grade = SchemaNode(Float(), validator=Range(min=0.0, max=10.0),  title="The average grade student/parents awarded this indicator.")
    indicator = SchemaNode(String(), validator=Length(min=10, max=200),  title="The indicator.")


class Indicators(SequenceSchema):
    indicator = Indicator()


class Satisfaction(MappingSchema):
    average_grade = SchemaNode(Float(), validator=Range(min=0.0, max=10.0),  title="The average satisfaction grade of this structure (*0.0 <= average_grade <= 10.0*).")
    national_grade = SchemaNode(Float(), validator=Range(min=0.0, max=10.0),  title="The average grade for all these structures in the Netherlands (*0.0 <= average_grade <= 10.0*).")
    education_structure = SchemaNode(String(), validator=Length(min=3, max=15),  title="String representing the education structure [#edu_in_holland]_ this satisfaction surveys were collected for.")
    indicators = Indicators( title="Array of :ref:`indicator`, which indicate satisfaction scores for specific indicators [#tevr_stud]_ [#tevr_par]_.")



class Satisfactions(SequenceSchema):
    satisfaction = Satisfaction()


class SchoolVOBranch(MappingSchema):
    address = general_rules.Address( title="Address of the branch.")
    avg_education_hours_per_student = AverageEducationHours( title="Array of :ref:`eduhours`, representing how many hours of education were planned for a year, and how many are actually realised.")
    avg_education_hours_per_student_url = SchemaNode(String(), validator=url,  title="URL to the *Onderwijstijd* page.")
    board = SchemaNode(String(), validator=Length(min=3, max=100),  title="The name of the board of this school.")
    board_id = general_rules.board_id( title="Identifier (assigned by :ref:`duodata`) of the board of this branch.")
    branch_id = general_rules.branch_id( title="Identifier (assigned by :ref:`duodata`) of this branch.")
    brin = general_rules.brin( title="'Basis Registratie Instellingen-nummer', identifier of the school this branch belongs to. Alphanumeric, four characters long.")
    building_img_url = SchemaNode(String(), validator=url,  title="URL to a photo of the building of this branch.")
    costs = Costs( title="Object representing the costs a parent can expect for this branch.")
    costs_url = SchemaNode(String(), validator=url,  title="URL to the *Onderwijskosten* page.")
    denomination = general_rules.denomination( title="In the Netherlands, schools can be based on a (religious [#denomination]_) conviction, which is denoted here.")
    education_structures = general_rules.EducationStructures( title="An array of strings, where each string represents the level of education [#edu_in_holland]_ (education structure) that is offered at this school.")
    email = SchemaNode(String(), validator=Email(),  title="Email address of this branch.")
    logo_img_url = SchemaNode(String(), validator=url,  title="URL to a photo of the logo of the school of this branch.")
    municipality = general_rules.municipality( title="The name of the municipality this branch is located in.")
    municipality_id = general_rules.municipality_code()
    name = general_rules.name( title="Name of the branch of this school.")
    parent_satisfaction = Satisfactions( title="Satisfaction polls of parents.")
    parent_satisfaction_url = SchemaNode(String(), validator=url,  title="URL to the *Tevredenheid ouders* page.")
    phone = general_rules.phone( title="Unnormalised string representing the phone number of this branch.")
    profile = SchemaNode(String(), validator=Length(min=3, max=500),  title="Short description of the motto of this branch.")
    province = general_rules.province( title="The province [#provinces]_ this branch is situated in.")
    schoolkompas_status_id = SchemaNode(Int(), validator=Range(min=0, max=1000),  title="Identifier used at http://schoolkompas.nl. Use unknown.")
    schoolvo_code = SchemaNode(String(), validator=Length(min=14, max=14),  title="Identifier used at http://schoolvo.nl. Consists of the board_id, brin and branch_id, separated by dashes. A school page can be accessed at `http://schoolvo.nl/?p_schoolcode=`\ *<schoolvo_code>*.")
    student_satisfaction = Satisfactions( title="Satisfaction polls of students.")
    student_satisfaction_url = SchemaNode(String(), validator=url,  title="URL to the *Tevredenheid leerlingen* page.")
    website = general_rules.website( title="URL of the website of the school.")


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

# EduHoursPerStudent
# ^^^^^^^^^^^^^^^^^^

# .. table::

#     =================================== =================================== ======================================================================================================
#     Field                               Type                                Description
#     =================================== =================================== ======================================================================================================
#     hours_planned                       integer                             Hours of education planned by the school council [#medezeggenschapsraad]_ for the past year.
#     hours_realised                      integer                             Hours of education realised at the school [#medezeggenschapsraad]_ for the past year.
#     year                                string                              The school year the hours apply to. There are various ways in which these years are represented at `Vensters voor Verantwoording <http://schoolvo.nl>`_, but the most common is *Leerjaar <n>*.
#     per_structure                       array of :ref:`eduhoursstructure`   Array of :ref:`eduhoursstructure`, representing the planning and realisation of education hours per education structure.
#     =================================== =================================== ======================================================================================================

# .. _eduhoursstructure:

# EduHoursPerStructure
# ^^^^^^^^^^^^^^^^^^^^

# .. table::

#     =================================== =================================== ======================================================================================================
#     Field                               Type                                Description
#     =================================== =================================== ======================================================================================================
#     hours_planned                       integer                             Hours of education planned by the school council [#medezeggenschapsraad]_ for the past year.
#     hours_realised                      integer                             Hours of education realised at the school [#medezeggenschapsraad]_ for the past year.
#     structure                           string                              The structure these hours apply to (*vbmo-t, havo, vwo, ...*)
#     =================================== =================================== ======================================================================================================
