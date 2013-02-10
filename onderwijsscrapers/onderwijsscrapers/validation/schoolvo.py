from colander import (MappingSchema, SequenceSchema, SchemaNode, String, Int,
                      Float, Length, Range, Date, url, Invalid)

from general_rules import Address


class Coordinates(MappingSchema):
    lat = SchemaNode(Float(), validator=Range(min=-180.0, max=180.0))
    lon = SchemaNode(Float(), validator=Range(min=-180.0, max=180.0))


# Extension of default address format with geo-coordinates
class SchoolVOAddress(Address):
    geo_location = Coordinates()


####################################
# Average education hours per year #
####################################
class PlannedRealisedHours(MappingSchema):
    # Approximately 9000 hours in a year
    hours_planned = SchemaNode(Int(), validator=Range(min=0, max=9000))
    hours_realised = SchemaNode(Int(), validator=Range(min=0, max=9000))


class PlannedRealisedHoursPerStructure(PlannedRealisedHours):
    structure = SchemaNode(String(), validator=Length(min=3, max=75))


class AverageEducationHoursPerStructure(SequenceSchema):
    average_hour_per_structure = PlannedRealisedHoursPerStructure()


class PlannedRealisedHoursPerYear(PlannedRealisedHours):
    # Year can be a bunch of things ("Leerjaar 1", "alle jaren", ...)
    year = SchemaNode(String(), validator=Length(min=3, max=75))
    per_structure = AverageEducationHoursPerStructure()


class AverageEducationHours(SequenceSchema):
    average_hour = PlannedRealisedHoursPerYear()
