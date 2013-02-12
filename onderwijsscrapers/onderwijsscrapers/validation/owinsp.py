from colander import (MappingSchema, SequenceSchema, SchemaNode, String, Length,
                      Range, Int)

import general_rules


class Report(MappingSchema):
    date = general_rules.publication_date
    education_structure = general_rules.education_structure
    title = SchemaNode(String(), validator=Length(min=30, max=150))
    url = general_rules.url


class Reports(SequenceSchema):
    report = Report()


class Rating(MappingSchema):
    date = general_rules.publication_date
    education_structure = general_rules.education_structure
    rating = SchemaNode(String(), validator=Length(min=4, max=20))


class RatingHistory(SequenceSchema):
    rating = Rating()


class CurrentRating(MappingSchema):
    education_structure = general_rules.date
    owinsp_id = SchemaNode(Int(), validator=Range(min=0))
    owinsp_url = general_rules.url
    rating = SchemaNode(String(), validator=Length(min=4, max=20))
    rating_excerpt = SchemaNode(String(), validator=Length(min=4, max=500))
    rating_valid_since = general_rules.publication_date


class CurrentRatings(SequenceSchema):
    current_rating = CurrentRating()


class OnderwijsInspectieVoBranch(MappingSchema):
    name = general_rules.name
    brin = general_rules.brin
    denomination = general_rules.denomination
    education_structures = general_rules.EducationStructures()
    branch_id = general_rules.branch_id
    board_id = general_rules.board_id
    address = general_rules.Address()
    website = general_rules.url
    result_card_url = general_rules.url
    reports = Reports()
    rating_history = RatingHistory()
    current_ratings = CurrentRatings()
    board = general_rules.name
