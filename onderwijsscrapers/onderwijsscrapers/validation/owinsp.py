""".. _owinspdata:

Onderwijsinspectie
------------------
The Inspectie voor het Onderwijs [#owinsp]_ is tasked with inspecting Dutch schools. Since 1997, they are required to publish reports on their findings when inspecting schools.
"""
from colander import (MappingSchema, SequenceSchema, SchemaNode, String, Length,
                      Range, Int)

import general_rules


class Report(MappingSchema):
    date = general_rules.publication_date( title="Date the report was published by the Onderwijsinspectie [#owinsp]_.")
    education_structure = general_rules.education_structure( title="The structure this rating applies to (*vbmo-t, havo, vwo, ...*)")
    title = SchemaNode(String(), validator=Length(min=30, max=150),  title="Title of the report.")
    url = general_rules.url( title="URL to the full report in PDF.")



class Reports(SequenceSchema):
    report = Report()


class Rating(MappingSchema):
    date = general_rules.publication_date( title="Date this rating was awarded.")
    education_structure = general_rules.education_structure( title="The structure this rating applies to (*vbmo-t, havo, vwo, ...*)")
    rating = SchemaNode(String(), validator=Length(min=4, max=20), title="Rating awarded by the Onderwijsinspectie [#owinsp]_.")



class RatingHistory(SequenceSchema):
    rating = Rating()


class CurrentRating(MappingSchema):
    # education_structure = None # TODO
    owinsp_id = SchemaNode(Int(), validator=Range(min=0))
    owinsp_url = general_rules.url()
    rating = SchemaNode(String(), validator=Length(min=4, max=20))
    rating_excerpt = SchemaNode(String(), validator=Length(min=4, max=500))
    rating_valid_since = general_rules.publication_date()


class CurrentRatings(SequenceSchema):
    current_rating = CurrentRating()


class OnderwijsInspectieVoBranch(MappingSchema):
    """

.. table::

    ======================================================= =================================== ========================================================================================================
    Field                                                   Type                                Description
    ======================================================= =================================== ========================================================================================================
    advice_structure_third_year                             array of :ref:`advice_struct_3`     An array of :ref:`advice_struct_3`, representing the distribution of the primary school advices students have in the third year of their education.
    board_id                                                integer                             Identifier (assigned by :ref:`duodata`) of the board of this branch.
    branch_id                                               integer                             Identifier (assigned by :ref:`duodata`) of this branch.
    brin                                                    string                              "Basis Registratie Instellingen-nummer", identifier of the school this branch belongs to. Alphanumeric, four characters long.
    composition_first_year                                  :ref:`first_year_comp`              Composition of the first year of this school, distinguishing between *combined* (students from different education structures partaking in the same courses) and *categorical* (percentage of students from the same education structures).
    exam_average_grades                                     array of :ref:`exam_avg_grades`     Array of :ref:`exam_avg_grades`, showing the average exam grade per course group.
    exam_participation_per_profile                          array of :ref:`exam_part_prof`      Array of :ref:`exam_part_prof`, containing the distribution of sectors (VMBO) and profiles (HAVO/VWO) in students participating in exams.
    first_years_performance                                 :ref:`first_year_perf`              Description of the performance of the school's "onderbouw" (first years).
    meta                                                    :ref:`owinspmeta`                   Metadata, such as date of scrape and whether this item passed validation.
    performance_assessments                                 array of :ref:`perf_ass`            Array of :ref:`perf_ass`, indicating the "Opbrengstenoordeel", a rating given by the Inspectie to each school, based on the performance in the first years ("onderbouw"), final years ("bovenbouw"), grades of the central examinations and the three year average of the difference between "schoolexamens" and central examinations grades.
    reports                                                 array of :ref:`owinspreport`        Array of :ref:`owinspreport`, where each item represents a report of the Onderwijsinspectie [#owinsp]_ in PDF.
    students_from_third_year_to_graduation_without_retaking array of :ref:`straight_grad`       Array of :ref:`straight_grad`, showing the percentage of students that go on to graduation from their third year without retaking a year, per education structure.
    students_in_third_year_without_retaking                 array of :ref:`3yearnoretakes`      Array of :ref:`3yearnoretakes`, showing the percentage of students that reach their third year without retaking a year.
    ======================================================= =================================== ========================================================================================================

    """
    address = general_rules.Address( title="Address of this branch")
    board = general_rules.name( title="The name of the board of this school.")
    board_id = general_rules.board_id( title="Identifier (assigned by :ref:`duodata`) of the board of this branch.")
    branch_id = general_rules.branch_id( title="Identifier (assigned by :ref:`duodata`) of this branch.")
    brin = general_rules.brin( title="'Basis Registratie Instellingen-nummer', identifier of the school this branch belongs to. Alphanumeric, four characters long.")
    current_ratings = CurrentRatings( title="Array of :ref:`owinspcurrat`, where each item represents the current rating of the Onderwijsinspectie [#owinsp]_.")
    denomination = general_rules.denomination( title="In the Netherlands, schools can be based on a (religious [#denomination]_) conviction, which is denoted here.")
    education_structures = general_rules.EducationStructures( title="An array of strings, where each string represents the level of education [#edu_in_holland]_ (education structure) that is offered at this school.")
    name = general_rules.name( title="Name of this branch.")
    rating_history = RatingHistory( title="Array of :ref:`owinsprathist`, where each item represents a rating the Onderwijsinspectie [#owinsp]_ awarded to this branch.")
    reports = Reports( title="Array of :ref:`owinspreport`, where each item represents a report of the Onderwijsinspectie [#owinsp]_ in PDF.")
    result_card_url = general_rules.url( title="URL to the result card ('opbrengstenkaart') of this branch.")
    website = general_rules.url( title="Website of this branch (optional).")


class OnderwijsInspectiePoBranch(MappingSchema):
    address = general_rules.Address( title="Address of this branch")
    board_id = general_rules.board_id()
    branch_id = general_rules.branch_id()
    brin = general_rules.brin( title="'Basis Registratie Instellingen-nummer', identifier of the school this branch belongs to. Alphanumeric, four characters long.")
    current_rating = CurrentRating()
    denomination = general_rules.denomination( title="In the Netherlands, schools can be based on a (religious [#denomination]_) conviction, which is denoted here.")
    name = general_rules.name( title="Name of this branch.")
    rating_history = RatingHistory( title="Array of :ref:`owinsprathist`, where each item represents a rating the Onderwijsinspectie [#owinsp]_ awarded to this branch.")
    reports = Reports( title="Array of :ref:`owinspreport`, where each item represents a report of the Onderwijsinspectie [#owinsp]_ in PDF.")
    website = general_rules.url( title="Website of this branch (optional).")


# .. _exam_avg_grades:

# AverageExamGrades
# ^^^^^^^^^^^^^^^^^
# .. table::

#     =================================== =================================== ==========================================================================
#     Field                               Type                                Description
#     =================================== =================================== ==========================================================================
#     grade                               float                               The average exam grade.
#     compared_performance                integer                             Value between 1 and 5 comparing how "good" this score is compared to the national average for this education structure (1 being worse, 2 being somewhat worse, 3 being average, 4 being somewhat better and 5 being better)
#     education_structure                 string                              Level of education [#edu_in_holland]_
#     name                                string                              The name of the course group this grade applies to.
#     =================================== =================================== ==========================================================================

# .. _owinspcurrat:

# CurrentRating
# ^^^^^^^^^^^^^
# .. table::

#     =================================== =================================== ==========================================================================
#     Field                               Type                                Description
#     =================================== =================================== ==========================================================================
#     education_structure                 string                              The structure this rating applies to (*vbmo-t, havo, vwo, ...*). **This value is optional**: as :ref:`owinspdatapobranch` do not have education structures, only :ref:`owinspdatavobranch` have this value.
#     owinsp_id                           integer                             Identifier (assigned by :ref:`owinspdata`). Use unknown.
#     owinsp_url                          string                              URL to the page of the branch where the rating for this education_structure was found.
#     rating                              string                              Rating awarded by the Onderwijsinspectie [#owinsp]_.
#     rating_excerpt                      string                              Excerpt of the rating report.
#     rating_valid_since                  date                                Date this rating went into effect.
#     =================================== =================================== ==========================================================================

# .. _exam_part_prof:

# ExamParticipationPerProfile
# ^^^^^^^^^^^^^^^^^^^^^^^^^^^
# .. table::

#     ========================================= =================================== ==========================================================================
#     Field                                     Type                                Description
#     ========================================= =================================== ==========================================================================
#     sector                                    string                              The sector or profile, depending on the education structure.
#     percentage                                float                               Percentage of students participating in an exam with this sector of profile.
#     education_structure                       string                              The education structure [#edu_in_holland]_ this sector or profile belongs to.
#     ========================================= =================================== ==========================================================================

# .. _first_year_comp:

# FirstYearComposition
# ^^^^^^^^^^^^^^^^^^^^
# .. table::

#     ========================================= =================================== ==========================================================================
#     Field                                     Type                                Description
#     ========================================= =================================== ==========================================================================
#     percentage_student_combined_education     float                               Percentage of students in combined education (following multiple kinds of education)
#     percentage_student_categorical_education  float                               Percentage of students in categorical education (following one kind of education)
#     combined_education_structures             array of strings                    Array containing strings representing education structures that have students following *combined* education.
#     categorical_education_structures          array of strings                    Array containing strings representing education structures that have students following *categorical* education.
#     ========================================= =================================== ==========================================================================

# .. _first_year_perf:

# FirstYearPerformance
# ^^^^^^^^^^^^^^^^^^^^
# .. table::

#     ========================================= =================================== ==========================================================================
#     Field                                     Type                                Description
#     ========================================= =================================== ==========================================================================
#     ratio                                     float                               Index describing the change of the first years performance. The starting date for this index is not known.
#     compared_performance                      integer                             Value between 1 and 5 comparing how "good" this score is compared to the national average for this education structure (1 being worse, 2 being somewhat worse, 3 being average, 4 being somewhat better and 5 being better)
#     compared_performance_category             string                              String describing to which education structure (group) this school's first years are compared.
#     ========================================= =================================== ==========================================================================

# PerformanceAssessments
# ^^^^^^^^^^^^^^^^^^^^^^

# .. table::

#     =================================== =================================== ==========================================================================
#     Field                               Type                                Description
#     =================================== =================================== ==========================================================================
#     education_structure                 string                              The structure this assessment applies to (*vbmo-t, havo, vwo, ...*)
#     performance_assessment              string                              String describing the assessment. Can have a value "voldoende" (adequate), "onvoldoende" (inadequate), "van 1 jaar gegevens" (data for only 1 year available) or "geen oordeel/onvoldoende gegevens" (no assessment/not enough data).
#     =================================== =================================== ==========================================================================

# .. _advice_struct_3:

# PrimarySchoolAdvices
# ^^^^^^^^^^^^^^^^^^^^

# .. table::

#     =================================== =================================== ==========================================================================
#     Field                               Type                                Description
#     =================================== =================================== ==========================================================================
#     primary_school_advices              Array of :ref:`advice_struct_comp`  Array of :ref:`advice_struct_comp`, containing the distribution of primary school advices of students in the third year of their education.
#     education_structure                 string                              String that represents the level of education [#edu_in_holland]_ the primary school advice distribution applies to.
#     =================================== =================================== ==========================================================================

# .. _advice_struct_comp:

# PrimarySchoolAdvice
# ^^^^^^^^^^^^^^^^^^^

# .. table::

#     =================================== =================================== ==========================================================================
#     Field                               Type                                Description
#     =================================== =================================== ==========================================================================
#     advice                              string                              String that represents the level of education [#edu_in_holland]_ the primary school recommended the student upon leaving primary education.
#     percentage_of_students              float                               Percentage of students with this advice in the third year of their education.
#     =================================== =================================== ==========================================================================

# StraightToGraduation
# ^^^^^^^^^^^^^^^^^^^^
# .. table::

#     =================================== =================================== ==========================================================================
#     Field                               Type                                Description
#     =================================== =================================== ==========================================================================
#     education_structure                 string                              Level of education [#edu_in_holland]_
#     percentage                          float                               Percentage of all students in this education structure that graduate without retaking any year between their third and their final year.
#     compared_performance                integer                             Value between 1 and 5 comparing how "good" this score is compared to the national average for this education structure (1 being worse, 2 being somewhat worse, 3 being average, 4 being somewhat better and 5 being better)
#     =================================== =================================== ==========================================================================

# .. _3yearnoretakes:

# StraightToThirdYear
# ^^^^^^^^^^^^^^^^^^^
# .. table::

#     =================================== =================================== ==========================================================================
#     Field                               Type                                Description
#     =================================== =================================== ==========================================================================
#     education_structure                 string                              Level of education [#edu_in_holland]_
#     percentage                          float                               Percentage of all students in this education structure that reach their third year without retaking any year between their first and their third year.
#     =================================== =================================== ==========================================================================
