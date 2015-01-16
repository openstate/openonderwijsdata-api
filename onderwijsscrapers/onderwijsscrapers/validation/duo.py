""".. _duodata:

DUO
---
DUO publishes many different datasets, each of these datasets has a different "release cycle". Some are published annually, just before the start of the new schoolyear, others are updated on a monthly basis. To group related data we introduce the notion of a "reference year". DUO datasets that are published within the same calendar year are grouped together into a single (vo_board, vo_school or vo_branch) document. For example: DUO published the :ref:`duostdstruct` on October 1, 2012 and :ref:`duostdres` on October 2, 2012, in this case both documents are combined into a single vo_branch document with ``reference_year`` 2012. For the sake of completeness, the exact reference date of the original item is also preserved, for example in the ``student_residences_reference_date`` and ``students_by_structure_reference_date`` attributes.

.. note::

   Currently DUO updates general information (addresses, names, phone numbers, etc.) of educational institutions on a monthly basis. Unfortunately, historical information is not provided. This means that for some reference years the API contains information such as the financial indicators and dropouts of a school, but does not include the address or name. A plausible explanation is that because of mergers or bankruptcies the school no longer exists in recent files.

.. _`COROP-gebied`: http://data.duo.nl/includes/navigatie/openbare_informatie/waargebruikt.asp?item=Coropgebied
.. _`Onderwijsgebied`: http://data.duo.nl/includes/navigatie/openbare_informatie/waargebruikt.asp?item=Onderwijsgebied
.. _`Nodaal gebied`: http://data.duo.nl/includes/navigatie/openbare_informatie/waargebruikt.asp?item=Nodaal%20gebied
.. _`Rmc-regio`: http://data.duo.nl/includes/navigatie/openbare_informatie/waargebruikt.asp?item=Rmc-gebied
.. _`Rpa-gebied`: http://data.duo.nl/includes/navigatie/openbare_informatie/waargebruikt.asp?item=Rpa-gebied
.. _`Wgr-gebied`: http://data.duo.nl/includes/navigatie/openbare_informatie/waargebruikt.asp?item=Wgr-gebied
.. _`Indicatie Special Basis Onderwijs`: http://data.duo.nl/includes/navigatie/openbare_informatie/waargebruikt.asp?item=Indicatie%20speciaal%20onderwijs
.. _`Cluster`: http://data.duo.nl/includes/navigatie/openbare_informatie/waargebruikt.asp?item=Cluster

"""
from colander import (MappingSchema, SequenceSchema, SchemaNode, String, Int,
    Length, Range, Date, Invalid, Float, Boolean, OneOf)
import colander
import general_rules
from onderwijsscrapers.codebooks import Codebook, load_codebook

class FinancialKeyIndicatorsPerYear(SequenceSchema):
    @colander.instantiate()
    class financial_key_indicator_per_year(MappingSchema):
        capitalization_ratio = SchemaNode(Float())
        capitalization_ratio.orig = "Kapitalisatiefactor"
        contract_activities_div_gov_funding = SchemaNode(Float())
        contract_activities_div_gov_funding.orig = "Contractactiviteiten/rijksbijdragen"
        contractactivities_div_total_profits = SchemaNode(Float())
        contractactivities_div_total_profits.orig = "Contractactiviteiten/totale baten"
        equity_div_total_profits = SchemaNode(Float())
        equity_div_total_profits.orig = "Eigen vermogen/totale baten"
        facilities_div_total_profits = SchemaNode(Float())
        facilities_div_total_profits.orig = "Voorzieningen/totale baten"
        general_reserve_div_total_income = SchemaNode(Float())
        general_reserve_div_total_income.orig = "Algemene reserve/totale baten"
        gov_funding_div_total_profits = SchemaNode(Float())
        gov_funding_div_total_profits.orig = "Rijksbijdragen/totale baten"
        group = SchemaNode(String())
        group.orig = "Groepering"
        housing_expenses_div_total_expenses = SchemaNode(Float())
        housing_expenses_div_total_expenses.orig = "Huisvestingslasten/totale lasten"
        housing_investment_div_total_profits = SchemaNode(Float())
        housing_investment_div_total_profits.orig = "Investering huisvesting/totale baten"
        investments_div_total_profits = SchemaNode(Float())
        investments_div_total_profits.orig = "Investeringen/totale baten"
        investments_relative_to_equity = SchemaNode(Float())
        investments_relative_to_equity.orig = "Beleggingen t.o.v. eigen vermogen"
        liquidity_current_ratio = SchemaNode(Float())
        liquidity_current_ratio.orig = "Liquiditeit (current ratio)"
        liquidity_quick_ratio = SchemaNode(Float())
        liquidity_quick_ratio.orig = "Liquiditeit (quick ratio)"
        operating_capital_div_total_profits = SchemaNode(Float())
        operating_capital_div_total_profits.orig = "Werkkapitaal/totale baten"
        operating_capital = SchemaNode(Float())
        operating_capital.orig = "Werkkapitaal"
        other_gov_funding_div_total_profits = SchemaNode(Float())
        other_gov_funding_div_total_profits.orig = "Overige overheidsbijdragen/totale baten"
        profitability = SchemaNode(Float())
        profitability.orig = "Rentabiliteit"
        solvency_1 = SchemaNode(Float())
        solvency_1.orig = "Solvabiliteit 1"
        solvency_2 = SchemaNode(Float())
        solvency_2.orig = "Solvabiliteit 2"
        staff_costs_div_gov_funding = SchemaNode(Float())
        staff_costs_div_gov_funding.orig = "Personeel/rijksbijdragen"
        staff_expenses_div_total_expenses = SchemaNode(Float())
        staff_expenses_div_total_expenses.orig = "Personele lasten/totale lasten"
        year = general_rules.year


class Dropouts(SequenceSchema):
    @colander.instantiate()
    class dropout(MappingSchema):
        """**Source:** `Voortijdig schoolverlaten - Voortijdig schoolverlaten - 02. Vsv in het voortgezet onderwijs per vo instelling <http://data.duo.nl/organisatie/open_onderwijsdata/databestanden/vschoolverlaten/vsvers/vsv_voortgezet.asp>`_"""
        year = general_rules.year( title="The year the dropout numbers apply to.")
        dropouts_with_mbo1_diploma = SchemaNode(Int(), validator=Range(min=0, max=5000),  title="Number of dropouts having a MBO 1 diploma (apprenticeship level) [#mbo1]_.")
        dropouts_with_mbo1_diploma.orig = "Aantal VSV-ers met MBO 1 diploma"
        dropouts_with_vmbo_diploma = SchemaNode(Int(), validator=Range(min=0, max=5000),  title="Number of dropouts having a VMBO diploma [#vmbo]_.")
        dropouts_with_vmbo_diploma.orig = "Aantal VSV-ers met VMBO diploma"
        dropouts_without_diploma = SchemaNode(Int(), validator=Range(min=0, max=5000),  title="Number of dropouts having no diploma.")
        dropouts_without_diploma.orig = "Aantal VSV-ers zonder diploma"
        education_structure = SchemaNode(String(), validator=Length(min=3, max=75),  title="Level of education [#edu_in_holland]_.")
        total_dropouts = SchemaNode(Int(), validator=Range(min=0, max=5000),  title="Total dropouts for the given year at this school.")
        total_students = SchemaNode(Int(), validator=Range(min=0, max=5000),  title="Total students for the given year at this school.")




class Graduations(SequenceSchema):
    @colander.instantiate()
    class graduation(MappingSchema):
        """**Source:** `Voortgezet onderwijs - Leerlingen - 06. Examenkandidaten en geslaagden <http://data.duo.nl/organisatie/open_onderwijsdata/databestanden/vo/leerlingen/Leerlingen/vo_leerlingen6.asp>`_"""
        candidates = SchemaNode(Int(), validator=Range(min=0),  title="The total number of exam candidates for this school year")
        failed = SchemaNode(Int(), validator=Range(min=0),  title="The number of candidates that did not graduate")
        passed = SchemaNode(Int(), validator=Range(min=0),  title="The number of candidates that graduated")
        @colander.instantiate()
        class per_department(SequenceSchema):
            @colander.instantiate()
            class department(MappingSchema):
                class GraudationDepartmentCandidates(MappingSchema):
                    male = SchemaNode(Int(), validator=Range(min=0))
                    female = SchemaNode(Int(), validator=Range(min=0))
                    unkown = SchemaNode(Int(), validator=Range(min=0))
                    department = SchemaNode(String(), validator=Length(min=3, max=300))
                    department.orig = "OPLEIDINGSNAAM"
                    education_structure = general_rules.education_structure()
                    education_structure.orig = "ONDERWIJSTYPE VO"

                candidates = GraudationDepartmentCandidates( title="The total number of exam candidates for this school year")
                failed = GraudationDepartmentCandidates( title="The number of candidates that did not graduate")
                passed = GraudationDepartmentCandidates( title="The number of candidates that graduated")
        year = SchemaNode(String(), title="The school year the graduations applay to")
        year.orig = "Schooljaar"


class StudentResidences(SequenceSchema):
    @colander.instantiate()
    class student_residence(MappingSchema):
        """
Number of pupils per age group (up to 25, as special education is included).

**Source:** `Primair onderwijs - Leerlingen - 11. Leerlingen primair onderwijs per gemeente naar postcode leerling en leeftijd <http://data.duo.nl/organisatie/open_onderwijsdata/databestanden/po/Leerlingen/Leerlingen/po_leerlingen11.asp>`_
        """
        municipality = general_rules.municipality()
        municipality_code = general_rules.municipality_code()
        city = general_rules.city()
        zip_code = SchemaNode(String(), validator=Length(min=4, max=4), title="The zip code where these pupils live.")
        year_1 = SchemaNode(Int(), validator=Range(min=0))
        year_2 = SchemaNode(Int(), validator=Range(min=0))
        year_3 = SchemaNode(Int(), validator=Range(min=0))
        year_4 = SchemaNode(Int(), validator=Range(min=0))
        year_5 = SchemaNode(Int(), validator=Range(min=0))
        year_6 = SchemaNode(Int(), validator=Range(min=0))


class StudentsEnrolledInStructure(MappingSchema):
    male = SchemaNode(Int(), validator=Range(min=0))
    female = SchemaNode(Int(), validator=Range(min=0))
    total = SchemaNode(Int(), validator=Range(min=0))

class StudentsByStructure(SequenceSchema):
    @colander.instantiate()
    class students_by_structure(MappingSchema):
        """**Source:** `Voortgezet onderwijs - Leerlingen - 01. Leerlingen per vestiging naar onderwijstype, lwoo indicatie, sector, afdeling, opleiding <http://data.duo.nl/organisatie/open_onderwijsdata/databestanden/vo/leerlingen/Leerlingen/vo_leerlingen1.asp>`_"""
        department = SchemaNode(String(), validator=Length(min=3, max=300),  title="Optional. Department of a vmbo track.")
        education_name = SchemaNode(String(), validator=Length(min=3, max=300),  title="Name of the education programme.")
        education_structure = general_rules.education_structure( title="Level of education [#edu_in_holland]_.")
        elementcode = SchemaNode(Int(), validator=Range(min=0))
        lwoo = SchemaNode(Boolean(),  title="Indicates whether this sector supports 'Leerwegondersteunend onderwijs', for students who need additional guidance [#lwoo]_.")
        vmbo_sector = SchemaNode(String(), validator=Length(min=3, max=300),  title="Vmbo sector [#sectors]_.")
        year_1 = StudentsEnrolledInStructure( title="Distribution of male and female students for year 1.")
        year_2 = StudentsEnrolledInStructure( title="Distribution of male and female students for year 2.")
        year_3 = StudentsEnrolledInStructure( title="Distribution of male and female students for year 3.")
        year_4 = StudentsEnrolledInStructure( title="Distribution of male and female students for year 4.")
        year_5 = StudentsEnrolledInStructure( title="Distribution of male and female students for year 5.")
        year_6 = StudentsEnrolledInStructure( title="Distribution of male and female students for year 6.")


class StudentsByAge(MappingSchema):
    # for n in '3 4 5 6 7 8 9 10 11 12 13 14 '.split():
    age_3 = SchemaNode(Int(), validator=Range(min=0),  title="Number of children at age 3 in the key's weight category at this branch.")
    age_4 = SchemaNode(Int(), validator=Range(min=0),  title="Number of children at age 4 in the key's weight category at this branch.")
    age_5 = SchemaNode(Int(), validator=Range(min=0),  title="Number of children at age 5 in the key's weight category at this branch.")
    age_6 = SchemaNode(Int(), validator=Range(min=0),  title="Number of children at age 6 in the key's weight category at this branch.")
    age_7 = SchemaNode(Int(), validator=Range(min=0),  title="Number of children at age 7 in the key's weight category at this branch.")
    age_8 = SchemaNode(Int(), validator=Range(min=0),  title="Number of children at age 8 in the key's weight category at this branch.")
    age_9 = SchemaNode(Int(), validator=Range(min=0),  title="Number of children at age 9 in the key's weight category at this branch.")
    age_10 = SchemaNode(Int(), validator=Range(min=0),  title="Number of children at age 10 in the key's weight category at this branch.")
    age_11 = SchemaNode(Int(), validator=Range(min=0),  title="Number of children at age 11 in the key's weight category at this branch.")
    age_12 = SchemaNode(Int(), validator=Range(min=0),  title="Number of children at age 12 in the key's weight category at this branch.")
    age_13 = SchemaNode(Int(), validator=Range(min=0),  title="Number of children at age 13 in the key's weight category at this branch.")
    age_14 = SchemaNode(Int(), validator=Range(min=0),  title="Number of children at age 14 in the key's weight category at this branch.")

class AgesByStudentWeight(MappingSchema):
    """
This dict has three keys *student_weight_0_0*, *student_weight_0_3* and *student_weight_1_2*, the weights are based on the pupil's parents level of education [#weight]_.

**Source:** `Primair onderwijs - Leerlingen - 03. Leerlingen basisonderwijs naar leerlinggewicht en leeftijd <http://data.duo.nl/organisatie/open_onderwijsdata/databestanden/po/Leerlingen/Leerlingen/po_leerlingen3.asp>`_
    """
    student_weight_0_0 = StudentsByAge()
    student_weight_0_3 = StudentsByAge()
    student_weight_1_2 = StudentsByAge()

class ExamGrades(MappingSchema):
    """**Source:** `Voortgezet onderwijs - Leerlingen - 07. Geslaagden, gezakten en gemiddelde examencijfers per instelling <http://data.duo.nl/organisatie/open_onderwijsdata/databestanden/vo/leerlingen/Leerlingen/vo_leerlingen7.asp>`_"""
    sector = SchemaNode(String(),  title="E.g. 'Cultuur en Maatschappij'")
    sector.orig = "Afdeling"
    education_structure = SchemaNode(String(),  title="E.g. 'HAVO'")
    education_structure.orig = "Onderwijstype VO"
    candidates = SchemaNode(Int(),  title="The total number of exam candidates for this school year")
    passed = SchemaNode(Int(),  title="The number of candidates that graduated")
    failed = SchemaNode(Int(),  title="The number of candidates that did not graduate")
    avg_grade_school_exam = SchemaNode(Float())
    avg_grade_school_exam.orig = "Gemiddeld cijfer schoolexamen"
    avg_grade_central_exam = SchemaNode(Float())
    avg_grade_central_exam.orig = "Gemiddeld cijfer centraal examen"
    avg_final_grade = SchemaNode(Float())
    avg_final_grade.orig = "Gemiddeld cijfer cijferlijst"


class GradesPerCourse(MappingSchema):
    """
**Source:** `08. Examenkandidaten vmbo en examencijfers per vak per instelling <http://data.duo.nl/organisatie/open_onderwijsdata/databestanden/vo/leerlingen/Leerlingen/vo_leerlingen8.asp>`_

**Source:** `09. Examenkandidaten havo en examencijfers per vak per instelling <http://data.duo.nl/organisatie/open_onderwijsdata/databestanden/vo/leerlingen/Leerlingen/vo_leerlingen9.asp>`_

**Source:** `10. Examenkandidaten vwo en examencijfers per vak per instelling <http://data.duo.nl/organisatie/open_onderwijsdata/databestanden/vo/leerlingen/Leerlingen/vo_leerlingen10.asp>`_
    """
    amount_of_central_exams = SchemaNode(Int(),  title="The amount of central exams [#centralexams]_ conducted for this branch")
    amount_of_central_exams_counting_for_diploma = SchemaNode(Int(),  title="The amount of central exams [#centralexams]_ conducted at this branch that count for a diploma")
    amount_of_school_exams_with_grades = SchemaNode(Int(),  title="The amount of school exams [#schoolexams]_ conducted at this branch that are graded")
    amount_of_school_exams_with_grades_counting_for_diploma = SchemaNode(Int(),  title="The amount of school exams [#schoolexams]_ conducted at this branch that are graded and count for a diploma")
    amount_of_school_exams_with_rating = SchemaNode(Int(),  title="Not all school exams are graded, but are rated as 'onvoldoende' (insufficient), 'voldoende' (sufficient) and 'goed' (good). This number denotes the amount of school exams that have rating, rather then a grade")
    amount_of_school_exams_with_rating_counting_for_diploma = SchemaNode(Int(),  title="The amount of school exams that are rated rather than graded that count for a diploma")
    average_grade_overall = SchemaNode(Float(),  title="The final average grade. This average is based on the grades on the final list of grades")
    avg_grade_central_exams = SchemaNode(Float(),  title="The average grade for central exams.")
    avg_grade_central_exams_counting_for_diploma = SchemaNode(Float(),  title="The average grade of central exams that count toward a diploma")
    avg_grade_school_exams = SchemaNode(Float(),  title="The average grade for school exams")
    avg_grade_school_exams_counting_for_diploma = SchemaNode(Float(),  title="The average grade of school exams that count toward a diploma")
    course_abbreviation = SchemaNode(String(),  title="Abbreviation used by DUO that denotes the course")
    course_identifier = SchemaNode(String(),  title="Identifier used by DUO for a course")
    course_name = SchemaNode(String(),  title="Verbose, human-readable name for the course")
    education_structure = SchemaNode(String(),  title="Level of education [#edu_in_holland]_")

class WeightsPerSchool(SequenceSchema):
    @colander.instantiate()
    class weights_per_school(MappingSchema):
        """**Source:** `Primair onderwijs - Leerlingen - 11. Leerlingen (speciaal) basisonderwijs per schoolvestiging naar leerjaar <http://data.duo.nl/organisatie/open_onderwijsdata/databestanden/po/Leerlingen/Leerlingen/leerjaar.asp>`_"""
        student_weight_0_0 = SchemaNode(Int() ,  title="Number of pupils who's parents don't fall into the weight 0.3 or 1.2 categories.")
        student_weight_0_3 = SchemaNode(Int() ,  title="Number of pupils who's both parents didn't get education beyond lbo/vbo, 'praktijkonderwijs' or vmbo 'basis- of kaderberoepsgerichte leerweg' [#weight]_.")
        student_weight_1_2 = SchemaNode(Int() ,  title="Number of pupils who's parents (one or both) didn't get education beyond 'basisonderwijs' or (v)so-zmlk [#weight]_.")
        school_weight = SchemaNode(Int() ,  title="Based on the student weights and results in extra money for the branch.")
        school_weight.orig = "Schoolgewicht"
        impulse_area = SchemaNode(Boolean(),  title="True if the branch is located in a so-called impulse area, which is an zipcode area with many families with low income or welfare. In if this is the case the branch gets extra money for each pupil.")
        impulse_area.orig = "Impulsgebied"


class StudentsByYear(SequenceSchema):
    @colander.instantiate()
    class students_by_year(MappingSchema):
        """**Source:** `Primair onderwijs - Leerlingen - 11. Leerlingen (speciaal) basisonderwijs per schoolvestiging naar leerjaar <http://data.duo.nl/organisatie/open_onderwijsdata/databestanden/po/Leerlingen/Leerlingen/leerjaar.asp>`_"""
        year_n = SchemaNode(Int(), title="Number of students for year *n* (including special education) .")


#TODO:
#class PupilsByOrigins


class StudentPrognosis(SequenceSchema):
    @colander.instantiate()
    class students_prognosis(MappingSchema):
        """**Source:** `Primair onderwijs - Leerlingen - 11. Prognose aantal leerlingen <http://data.duo.nl/organisatie/open_onderwijsdata/databestanden/vo/leerlingen/Leerlingen/vo_leerlingen11.asp>`_"""
        year = SchemaNode(Int(), title="Prognosis is for this year")
        structure = SchemaNode(String(), title="Level of education [#edu_in_holland]_.")
        students = SchemaNode(Int(), title="Number of students")




class FineGrainedStructureStudents(SequenceSchema):
    @colander.instantiate()
    class students_by_finegrained_structure(MappingSchema): # TODO consider: colander.TupleSchema
        type = SchemaNode(String()) # Actually a certain set of values
        count = SchemaNode(Int())

class VavoStudents(SequenceSchema):
    @colander.instantiate()
    class vavo_students(MappingSchema):
         """ Students who are registered in secondary education, but are in an adult education program, can still graduate with a secondary education degree (*Rutte - regeling*) """
         non_vavo = SchemaNode(Int(), title="Number of non-vavo students") # `AANTAL LEERLINGEN`
         vavo = SchemaNode(Int(), title="Number of students delegated to adult education") # `AANTAL VO LEERLINGEN UITBESTEED AAN VAVO`
         # (there's also a TOTAAL AANTAL LEERLINGEN sum column that we ignore)

class StudentsByAdvice(SequenceSchema):
    @colander.instantiate()
    class students_by_advice(MappingSchema):
        """
The level of education [#edu_in_holland]_ that the primary school recommended the student upon leaving primary education
**Source:** `Primair onderwijs - Leerlingen - 12. Leerlingen (speciaal) basisonderwijs per schoolvestiging naar schooladvies <http://data.duo.nl/organisatie/open_onderwijsdata/databestanden/po/Leerlingen/Leerlingen/Schooladvies.asp>`_
        """
        vso = SchemaNode(Int(),  title="Number of students with VSO advice")
        vso.orig = "VSO"
        pro = SchemaNode(Int(),  title="Number of students with PrO advice")
        pro.orig = "PrO"
        vmbo_bl = SchemaNode(Int(),  title="Number of students with VMBO BL advice")
        vmbo_bl.orig = "VMBO BL"
        vmbo_bl_kl = SchemaNode(Int(),  title="Number of students with VMBO BL-KL advice")
        vmbo_bl_kl.orig = "VMBO BL-KL"
        vmbo_kl = SchemaNode(Int(),  title="Number of students with VMBO KL advice")
        vmbo_kl.orig = "VMBO KL"
        vmbo_kl_gt = SchemaNode(Int(),  title="Number of students with VMBO KL-GT advice")
        vmbo_kl_gt.orig = "VMBO KL-GT"
        vmbo_gt = SchemaNode(Int(),  title="Number of students with VMBO GT advice")
        vmbo_gt.orig = "VMBO GT"
        vmbo_gt_havo = SchemaNode(Int(),  title="Number of students with VMBO GT-HAVO advice")
        vmbo_gt_havo.orig = "VMBO GT-HAVO"
        havo = SchemaNode(Int(),  title="Number of students with HAVO advice")
        havo.orig = "HAVO"
        havo_vwo = SchemaNode(Int(),  title="Number of students with HAVO-VWO advice")
        havo_vwo.orig = "HAVO-VWO"
        vwo = SchemaNode(Int(),  title="Number of students with VWO advice")
        vwo.orig = "VWO"
        unknown = SchemaNode(Int(),  title="Number of students with unknown advice")
        unknown.orig = "ONBEKEND"

class SPOStudentsByEduType(SequenceSchema):
    """**Source:** `Primair onderwijs - Leerlingen - 06. Leerlingen speciaal (basis)onderwijs naar onderwijssoort <http://data.duo.nl/organisatie/open_onderwijsdata/databestanden/po/Leerlingen/Leerlingen/po_leerlingen6.asp>`_"""
    @colander.instantiate()
    class spo_students_by_edu_type(MappingSchema):
        spo_indication = SchemaNode(String(),  title="Indication of type of special education")
        spo_indication.orig = "`Indicatie Special Basis Onderwijs`_ "
        sbao = SchemaNode(Int()) # `SBAO`
        so = SchemaNode(Int(),  title="Special education.")
        so.orig = "SO"
        vso = SchemaNode(Int(),  title="Special secondary education.")
        vso.orig = "SVO"
        v_so = SchemaNode(Int(),  title="Special education and special secondary education.")
        v_so.orig = "(V)SO"

class StudentsByEduType():
    """**Source:** `Primair onderwijs - Leerlingen - 07. Leerlingen primair onderwijs per bevoegd gezag naar denominatie en onderwijssoort <http://data.duo.nl/organisatie/open_onderwijsdata/databestanden/po/Leerlingen/Leerlingen/po_leerlingen7.asp>`_"""
    @colander.instantiate()
    class students_by_edu_type(MappingSchema):
        denomination = general_rules.denomination()
        students = SchemaNode(Int(), title="Number of students")
        edu_types = SchemaNode(String(), validator=colander.OneOf(['BAO', 'SBAO', 'SO', 'VSO', '(V)SO']), title="Edu type, in BAO, SBAO, SO, VSO, (V)SO")

# TODO
# class StudentsInBRON(MappingSchema):
#     ambulatory_guidance = SchemaNode(Int())
#     branch_active = SchemaNode(Int())
#     cumi = SchemaNode(Int())
#     enrollments = SchemaNode(Int())
#     financed = SchemaNode(Int())
#     guided_bo_bso = SchemaNode(Int())
#     guided_vo = SchemaNode(Int())
#     noat = SchemaNode(Int())
#     non-financed = SchemaNode(Int())
#     non_financed = SchemaNode(Int())
#     po_type = SchemaNode(Int())
#     reintroduced = SchemaNode(Int())
#     reintroduced_bo_sbo = SchemaNode(Int())
#     reintroduced_vo = SchemaNode(Int())
#     total = SchemaNode(Int())


class SPOStudentsPerCluster(SequenceSchema):
    """**Source:** `Primair onderwijs - Leerlingen - 04. Leerlingen speciaal onderwijs naar cluster <http://data.duo.nl/organisatie/open_onderwijsdata/databestanden/po/Leerlingen/Leerlingen/po_leerlingen4.asp>`_"""
    @colander.instantiate()
    class spo_students_per_cluster(MappingSchema):
        # http://duo.nl/includes/navigatie/openbare_informatie/waargebruikt.asp?item=Cluster
        cluster_1 = SchemaNode(Int(),  title="Number of pupils in schools for visually handicapped students")
        cluster_1.orig = "`Cluster`_"
        cluster_2 = SchemaNode(Int(),  title="Number of pupils in schools for auditory / communicatively disabled students: deaf, hard of hearing, severe speech difficulties.")
        cluster_2.orig = "`Cluster`_"
        cluster_3 = SchemaNode(Int(),  title="Number of pupils in schools for pupils with physical and / or intellectual disabilities: very difficult learning, protracted illness with physical disabilities.")
        cluster_3.orig = "`Cluster`_"
        cluster_4 = SchemaNode(Int(), title="Number of pupils in schools for pupils with psychiatric disorders and severe learning and / or behavioral problems, chronically ill students without disabilities and students associated with university-associated institutes that provide assistance to children with complex learning, behavioral or emotional problems (*Pedologisch Instituut*).")
        cluster_4.orig = "`Cluster`_"


class SPOStudentsByBirthyear(SequenceSchema):
    """**Source:** `Primair onderwijs - Leerlingen - 05. Leerlingen speciaal (basis)onderwijs naar geboortejaar <http://data.duo.nl/organisatie/open_onderwijsdata/databestanden/po/Leerlingen/Leerlingen/po_leerlingen5.asp>`_"""
    @colander.instantiate()
    class spo_students_by_birthyear(MappingSchema):
        birthyear = general_rules.year( title="Year of birth")
        students = SchemaNode(Int(), title="Number of students born in this year")






class DuoAreaSchema(MappingSchema):
    corop_area = general_rules.corop_area( title="A COROP area in the Netherlands is a region consisting of several municipalities, and is primarily used by research institutions to present statistical data." )
    corop_area.orig = "`COROP-gebied`_"
    corop_area_code = general_rules.corop_area_code( title="Identifier of the corop_area." )
    education_area = general_rules.education_area( title="Education areas are aggregations of nodal areas based on regional origins and destinations of students in secondary education." )
    education_area.orig = "`Onderwijsgebied`_"
    education_area_code = general_rules.education_area_code( title="Identifier of the education_area." )
    nodal_area = general_rules.nodal_area( title="Area defined for the planning of distribution of secondary schools." )
    nodal_area.orig = "`Nodaal gebied`_"
    nodal_area_code = general_rules.nodal_area_code( title="Identifier of the nodal_area." )
    rmc_region = general_rules.rmc_region( title="Area that is used for the coordination of school dropouts.")
    rmc_region.orig = "`Rmc-regio`_"
    rmc_region_code = general_rules.rmc_region_code( title="Identifier of the rmc_region.")
    rpa_area = general_rules.rpa_area( title="Area defined to cluster information on the labour market.")
    rpa_area.orig = "`Rpa-gebied`_"
    rpa_area_code = general_rules.rpa_area_code( title="Identifier of the rpa_area.")
    wgr_area = general_rules.wgr_area( title="Cluster of municipalities per collaborating region according to the 'Wet gemeenschappelijke regelingen' [#wgr_law]_.")
    wgr_area.orig = "`Wgr-gebied`_"
    wgr_area_code = general_rules.wgr_area_code( title="Identifier of the wgr_area.")


class DuoVoBranch(DuoAreaSchema, MappingSchema):
    """ **Source:** `Voortgezet onderwijs - Adressen - 02. Adressen alle vestigingen <http://data.duo.nl/organisatie/open_onderwijsdata/databestanden/vo/adressen/Adressen/vestigingen.asp>`_ """
    address = general_rules.Address( title="Address of this branch." )
    correspondence_address = general_rules.Address( title="Correspondence address of this branch." )
    name = general_rules.name( title="Name of the school." )
    branch_id = general_rules.branch_id( title="Identifier (assigned by :ref:`duodata`) of this branch." )
    board_id = general_rules.board_id( title="Identifier (assigned by :ref:`duodata`) of the board of this branch." )
    brin = general_rules.brin( title="'Basis Registratie Instellingen-nummer', identifier of the school this branch belongs to. Alphanumeric, four characters long." )
    denomination = general_rules.denomination( title="In the Netherlands, schools can be based on a (religious [#denomination]_) conviction, which is denoted here." )
    education_structures = general_rules.EducationStructures( title="An array of strings, where each string represents the level of education [#edu_in_holland]_ (education structure) that is offered at this school." )
    municipality = general_rules.municipality( title="The name of the municipality this branch is located in." )
    municipality_code = general_rules.municipality_code( title="Identifier (assigned by CBS [#cbs]_) to this municipality." )
    phone = general_rules.phone( title="Phone number of the school." )
    province = general_rules.province( title="The province [#provinces]_ this branch is situated in." )
    reference_year = general_rules.reference_year( title="Year the schools source file was published." )
    reference_year.orig = "Peiljaar"
    website = general_rules.url( title="Website of this school." )


    vavo_students_reference_url = general_rules.website()
    vavo_students_reference_date = SchemaNode(Date(), missing=True)
    vavo_students = VavoStudents()

    students_by_finegrained_structure_reference_url = general_rules.website()
    students_by_finegrained_structure_reference_date = SchemaNode(Date(), missing=True)
    students_by_finegrained_structure = FineGrainedStructureStudents()

    graduations = Graduations( title="Array of :ref:`graduation` where each item represents a school year. For each year information on the number of passed, failed and candidates is available. A futher breakdown in department and gender is also available." )
    graduations.orig = "Examenkandidaten en geslaagden"
    graduations_reference_date = SchemaNode(Date(),  title="Date the graduations source file was published at http://data.duo.nl" )
    graduations_reference_date.orig = "Peildatum"
    graduations_reference_url = general_rules.reference_url( title="URL to the dropouts source file at http://data.duo.nl/" )

    student_residences = StudentResidences( title="Array of :ref:`duostdres`, where each item contains the distribution of students from a given municipality over the years in this branch." )
    student_residences_reference_date = SchemaNode(Date(),  title="Date the student residences source file was published at http://data.duo.nl" )
    student_residences_reference_date.orig = "Peildatum"
    student_residences_reference_url = general_rules.reference_url( title="URL of the student residences source file." )

    students_by_structure = StudentsByStructure( title="Distribution of students by education structure and gender." )
    students_by_structure_reference_date = SchemaNode(Date(), missing=True)
    students_by_structure_url = general_rules.website()

    exam_grades = GradesPerCourse()
    exam_grades_reference_date = SchemaNode(Date(), missing=True)
    exam_grades_reference_url = general_rules.website()

    vmbo_exam_grades_per_course = GradesPerCourse()
    vmbo_exam_grades_reference_date = SchemaNode(Date(), missing=True)
    vmbo_exam_grades_reference_url = general_rules.website()

    havo_exam_grades_per_course = GradesPerCourse()
    havo_exam_grades_reference_date = SchemaNode(Date(), missing=True)
    havo_exam_grades_reference_url = general_rules.website()

    vwo_exam_grades_per_course = GradesPerCourse()
    vwo_exam_grades_reference_date = SchemaNode(Date(), missing=True)
    vwo_exam_grades_reference_url = general_rules.website()


class DuoVoBoard(MappingSchema):
    """**Source:** `Voortgezet onderwijs - Adressen - 03. Adressen hoofdbesturen <http://data.duo.nl/organisatie/open_onderwijsdata/databestanden/vo/adressen/Adressen/besturen.asp>`_"""
    address = general_rules.Address( title="Address of this board.")
    correspondence_address = general_rules.Address( title="Correspondence address of this board.")
    board_id = general_rules.board_id( title="Identifier (assigned by :ref:`duodata`) of the board of this branch.")
    name = general_rules.name( title="Name of the board.")
    phone = general_rules.phone( title="Phone number of the board.")
    municipality = general_rules.municipality( title="The name of the municipality this board is located in.")
    municipality_code = general_rules.municipality_code( title="Identifier (assigned by CBS [#cbs]_) to this municipality.")
    administrative_office_id = SchemaNode(Int(),  title="Identifier (assigned by :ref:`duodata`) for the accountancy firm that manages this board finances.")
    administrative_office_id.orig = "Administratiekantoor"
    denomination = general_rules.denomination( title="In the Netherlands, schools can be based on a (religious [#denomination]_) conviction, which is denoted here.")
    reference_year = general_rules.reference_year( title="Year the boards source file was published")
    reference_year.orig = "Peiljaar"
    website = general_rules.website( title="URL of the webpage of the board.")

    financial_key_indicators_per_year_reference_date = SchemaNode(Date(),  title="Date the financial key indicator source file was published at http://data.duo.nl", missing=True)
    financial_key_indicators_per_year_reference_date.orig = "Peiljaar"

    vavo_students_reference_url = general_rules.website()
    vavo_students_reference_date = SchemaNode(Date(), missing=True)
    # vavo_students = VavoStudents()
    vavo_students = Codebook([
        {'field':'board_id', 'keyed':'0', 'source':'BEVOEGD GEZAG NUMMER','type':'int', 'description':''},
        {'field':'vavo', 'keyed':'', 'source':'AANTAL LEERLINGEN','type':'int', 'description':''},
    ]).schema(description='Vavo students source bla bla')

    staff_reference_url = general_rules.website()
    staff_reference_date = SchemaNode(Date(), missing=True)
    staff = load_codebook('duo/vo_boards_staff').schema()


class DuoVoSchool(DuoAreaSchema, MappingSchema):
    """ **Source:** `Voortgezet onderwijs - Adressen - 01. Adressen hoofdvestigingen <http://data.duo.nl/organisatie/open_onderwijsdata/databestanden/vo/adressen/Adressen/hoofdvestigingen.asp>`_"""
    address = general_rules.Address( title="Address of this school.")
    correspondence_address = general_rules.Address( title="Correspondence address of this school.")
    board_id = general_rules.board_id( title="Identifier (assigned by :ref:`duodata`) of the board of this school.")
    brin = general_rules.brin( title="'Basis Registratie Instellingen-nummer', identifier of the school this branch belongs to. Alphanumeric, four characters long.")
    denomination = general_rules.denomination( title="In the Netherlands, schools can be based on a (religious [#denomination]_) conviction, which is denoted here.")
    education_structures = general_rules.EducationStructures( title="An array of strings, where each string represents the level of education [#edu_in_holland]_ (education structure) that is offered at this school.")
    municipality = general_rules.municipality( title="The name of the municipality this branch is located in.")
    municipality_code = general_rules.municipality_code( title="Identifier (assigned by CBS [#cbs]_) to this municipality.")
    phone = general_rules.phone( title="Phone number of the school.")
    province = general_rules.province( title="The province [#provinces]_ this branch is situated in.")
    reference_year = general_rules.reference_year( title="Year the schools source file was published.")
    reference_year.orig = "Peiljaar"
    website = general_rules.url( title="Website of this school.")

    students_prognosis = StudentPrognosis()
    students_prognosis_reference_date = SchemaNode(Date(), missing=True,  title="Date the source file was published at http://data.duo.nl")
    students_prognosis_reference_date.orig = "Peildatum"
    students_prognosis_url = general_rules.website()

    vo_lo_collaboration_reference_url = general_rules.website()
    vo_lo_collaboration_reference_date = SchemaNode(Date(), missing=True)
    vo_lo_collaboration = general_rules.collaboration_id()

    pao_collaboration_reference_url = general_rules.website()
    pao_collaboration_reference_date = SchemaNode(Date(), missing=True)
    pao_collaboration = general_rules.collaboration_id()

    dropouts = Dropouts(missing=True)
    dropouts_reference_date = SchemaNode(Date(), missing=True)
    dropouts_reference_url = general_rules.reference_url()


class DuoPoBoard(MappingSchema):
    """**Source:** `Primair onderwijs - Adressen - 05. Bevoegde gezagen basisonderwijs <http://data.duo.nl/organisatie/open_onderwijsdata/databestanden/po/adressen/Adressen/po_adressen05.asp>`_"""
    address = general_rules.Address( title="Address of this board.")
    correspondence_address = general_rules.Address( title="Correspondence address of this board.")
    board_id = general_rules.board_id( title="Identifier (assigned by :ref:`duodata`) of the board of this branch.")
    board_id.orig = "Bevoegd gezag nummer"
    name = general_rules.name( title="Name of the board.")
    name.orig = "Bevoegd gezag naam"
    phone = general_rules.phone( title="Phone number of the board.")
    phone.orig = "Telefoonnummer"
    municipality = general_rules.municipality( title="The name of the municipality this board is located in.")
    municipality.orig = "Gemeente"
    municipality_code = general_rules.municipality_code( title="Identifier (assigned by CBS [#cbs]_) to this municipality.")
    municipality_code.orig = "Gemeentenummer"
    administrative_office_id = SchemaNode(Int(),  title="Identifier (assigned by :ref:`duodata`) for the accountancy firm that manages this board finances.")
    administrative_office_id.orig = "Administratiekantoor"
    denomination = general_rules.denomination( title="In the Netherlands, schools can be based on a (religious [#denomination]_) conviction, which is denoted here.")
    denomination.orig = "Denominatie"
    reference_year = general_rules.reference_year( title="Year the boards source file was published")
    reference_year.orig = "Peiljaar"
    website = general_rules.website( title="URL of the webpage of the board.")

    # TODO:
    #financial_key_indicators_per_year = FinancialKeyIndicatorsPerYear()
    financial_key_indicators_per_year_reference_date = SchemaNode(Date(), missing=True,  title="Date the financial key indicator source file was published at http://data.duo.nl")
    financial_key_indicators_per_year_reference_date.orig = "Peiljaar"
    financial_key_indicators_per_year_url = general_rules.website()

    # edu_types = StudentsByEduType
    # edu_types_reference_date
    # edu_types_reference_url


class DuoPoSchool(DuoAreaSchema, MappingSchema):
    """**Source:** `Primair onderwijs - Adressen - 01. Hoofdvestigingen basisonderwijs <http://data.duo.nl/organisatie/open_onderwijsdata/databestanden/po/adressen/Adressen/hoofdvestigingen.asp>`_"""
    address = general_rules.Address( title="Address of this school.")
    correspondence_address = general_rules.Address( title="Correspondence address of this school.")
    board_id = general_rules.board_id( title="Identifier (assigned by :ref:`duodata`) of the board of this school.")
    board_id.orig = "Bevoegd gezag nummer"
    brin = general_rules.brin( title="'Basis Registratie Instellingen-nummer', identifier of the school this branch belongs to. Alphanumeric, four characters long.")
    denomination = general_rules.denomination( title="In the Netherlands, schools can be based on a (religious [#denomination]_) conviction, which is denoted here.")
    municipality = general_rules.municipality( title="The name of the municipality this branch is located in.")
    municipality_code = general_rules.municipality_code( title="Identifier (assigned by CBS [#cbs]_) to this municipality.")
    name = general_rules.name( title="Name of the school.")
    phone = general_rules.phone( title="Phone number of the school.")
    province = general_rules.province( title="The province [#provinces]_ this branch is situated in.")
    reference_year = general_rules.reference_year( title="Year the schools source file was published.")
    reference_year.orig = "Peiljaar"
    website = general_rules.website( title="Website of this school.")

    spo_students_per_cluster = SPOStudentsPerCluster( title="Number of pupils in special education, per special education cluster.")
    spo_students_per_cluster_reference_date = SchemaNode(Date(), missing=True,  title="Date the source file was published at http://data.duo.nl")
    spo_students_per_cluster_reference_url = general_rules.website( title="URL of the source file.")

    po_lo_collaboration_reference_url = general_rules.website()
    po_lo_collaboration_reference_date = SchemaNode(Date(), missing=True)
    po_lo_collaboration = general_rules.collaboration_id()

    pao_collaboration_reference_url = general_rules.website()
    pao_collaboration_reference_date = SchemaNode(Date(), missing=True)
    pao_collaboration = general_rules.collaboration_id()


class DuoPoBranch(DuoAreaSchema, MappingSchema):
    """**Source:** `Primair onderwijs - Adressen - 03. Alle vestigingen basisonderwijs <http://data.duo.nl/organisatie/open_onderwijsdata/databestanden/po/adressen/Adressen/vest_bo.asp>`_"""
    address = general_rules.Address( title="Address of this branch.")
    correspondence_address = general_rules.Address( title="Correspondence address of this branch.")
    name = general_rules.name( title="Name of the school.")
    branch_id = general_rules.branch_id( title="Identifier (assigned by :ref:`duodata`) of this branch.")
    board_id = general_rules.board_id( title="Identifier (assigned by :ref:`duodata`) of the board of this branch.")
    brin = general_rules.brin( title="'Basis Registratie Instellingen-nummer', identifier of the school this branch belongs to. Alphanumeric, four characters long.")
    denomination = general_rules.denomination( title="In the Netherlands, schools can be based on a (religious [#denomination]_) conviction, which is denoted here.")
    municipality = general_rules.municipality( title="The name of the municipality this branch is located in.")
    municipality_code = general_rules.municipality_code( title="Identifier (assigned by CBS [#cbs]_) to this municipality.")
    phone = general_rules.phone( title="Phone number of the school.")
    province = general_rules.province( title="The province [#provinces]_ this branch is situated in.")
    website = general_rules.url( title="Website of this school.")
    reference_year = general_rules.reference_year( title="Year the schools source file was published.")
    reference_year.orig = "Peiljaar"

    ages_per_branch_by_student_weight = AgesByStudentWeight()
    ages_per_branch_by_student_weight_reference_date = SchemaNode(Date(), missing=True,  title="Date the ages per branch by student weight source file was published at http://data.duo.nl")
    ages_per_branch_by_student_weight_reference_url = general_rules.website( title="URL of the ages per branch by student weight source file.")

    # TODO:
    #pupils_by_origins = PupilsByOrigins()
    pupils_by_origins_reference_date = SchemaNode(Date(), missing=True)
    pupils_by_origins_reference_url = general_rules.website()

    # TODO:
    #pupil_residences = PupilResidences()
    pupil_residences_reference_date = SchemaNode(Date(), missing=True)
    pupil_residences_reference_url = general_rules.website()


    weights_per_school = WeightsPerSchool()
    weights_per_school_reference_date = SchemaNode(Date(), missing=True)
    weights_per_school_reference_url = general_rules.website()

    # TODO:
    #student_year = StudentsByYear()
    student_year_reference_date = SchemaNode(Date(), missing=True)
    student_year_reference_url = general_rules.website()

    spo_law = SchemaNode(String(), validator=Length(min=2, max=4))
    spo_edu_type = SchemaNode(String()) # possibly multiple with slash
    spo_cluster = SchemaNode(Int(), validator=Range(min=0, max=4))

    spo_students_by_birthyear_reference_url = general_rules.website( title="URL of the source file.")
    spo_students_by_birthyear_reference_date = SchemaNode(Date(), missing=True,  title="Date the source file was published at http://data.duo.nl")
    spo_students_by_birthyear = SPOStudentsByBirthyear( title="Number of students per birth year")

    spo_students_by_edu_type_reference_url = general_rules.website( title="URL of the source file.")
    spo_students_by_edu_type_reference_date = SchemaNode(Date(), missing=True,  title="Date the source file was published at http://data.duo.nl")
    spo_students_by_edu_type = SPOStudentsByEduType( title="Number of students per special education type")

    students_by_advice_reference_url = general_rules.website( title="URL of the source file.")
    students_by_advice_reference_date = SchemaNode(Date(), missing=True,  title="Date the source file was published at http://data.duo.nl")
    students_by_advice = StudentsByAdvice( title="Number of students by secondary education level recommendation made upon leaving primary school")

    # TODO:
    # students_in_BRON = StudentsInBRON()
    students_in_BRON_reference_url = general_rules.website()
    students_in_BRON_reference_date = SchemaNode(Date(), missing=True)

    students_by_year = StudentsByYear()
    students_by_year_reference_url = general_rules.website()
    students_by_year_reference_date = SchemaNode(Date(), missing=True)


class DuoPaoCollaboration(MappingSchema):
    """**Source:** `Passend onderwijs - Adressen - 01. Adressen samenwerkingsverbanden lichte ondersteuning primair onderwijs <http://data.duo.nl/organisatie/open_onderwijsdata/databestanden/passendow/Adressen/Adressen/passend_po_1.asp>`_"""
    address = general_rules.Address( title="Address of this collaboration.")
    correspondence_address = general_rules.Address( title="Correspondence address of this collaboration.")
    collaboration_id = general_rules.collaboration_id( title="Identification number of collaboration")
    collaboration_id.orig = "Administratienummer"
    reference_year = general_rules.reference_year()


class DuoMboBoard(MappingSchema):
    """**Source:** `Middelbaar beroepsonderwijs - Adressen - 02. Adressen bevoegde gezagen <http://www.ib-groep.nl/organisatie/open_onderwijsdata/databestanden/mbo_/adressen/Adressen/bevoegde_gezagen.asp>`_"""
    address = general_rules.Address( title="Address of this board.")
    administrative_office_id = SchemaNode(Int(),  title="Identifier (assigned by :ref:`duodata`) for the accountancy firm that manages this board finances.")
    board_id  = general_rules.board_id( title="Identifier (assigned by :ref:`duodata`) of this board." )
    correspondence_address = general_rules.Address( title="Correspondence address of this board.")
    denomination = general_rules.denomination()
    municipality = general_rules.municipality()
    municipality_code = general_rules.municipality_code()
    name = general_rules.name( title="Name of the board." )
    phone = general_rules.phone( title="Phone number of the board." )
    website = general_rules.url( title="Website of this board." )

class DuoMboInstitution(DuoAreaSchema, MappingSchema):
    """**Source:** `Middelbaar beroepsonderwijs - Adressen - 01. Adressen instellingen <http://www.ib-groep.nl/organisatie/open_onderwijsdata/databestanden/mbo_/adressen/Adressen/instellingen.asp>`_"""
    brin = general_rules.brin( title="'Basis Registratie Instellingen-nummer', identifier of the institution. Alphanumeric, four characters long.")
    board_id  = general_rules.board_id( title="Identifier (assigned by :ref:`duodata`) of the board of this institution." )
    correspondence_address = general_rules.Address( title="Correspondence address of this institution.")
    denomination = general_rules.denomination()
    municipality = general_rules.municipality()
    municipality_code = general_rules.municipality_code()
    address = general_rules.Address( title="Address of this institution.")
    name = general_rules.name( title="Name of the institution." )
    phone = general_rules.phone( title="Phone number of the institution." )
    mbo_institution_kind = SchemaNode(String())
    mbo_institution_kind_code = SchemaNode(String())
    website = general_rules.website( title="Website of this institution.")

    # participants_per_grade_year_and_qualification = CodebookSchema('duo/mbo_participants_grade.csv')
    participants_per_grade_year_and_qualification_reference_url = general_rules.website()
    participants_per_grade_year_and_qualification_reference_date = SchemaNode(Date(), missing=True)

if __name__ == '__main__':
    import sys, inspect

    def print_schema(sch, n=0):
        if inspect.isclass(sch):
            sch = sch()
        print ' '*n, sch.name, '(%s)' % type(sch.typ).__name__
        for s in sch:
            if type(sch.typ).__name__ in ['Mapping', 'Sequence']:
                print_schema(s, n+1)

    for s in [DuoPoBoard, DuoPoSchool, DuoPoBranch, DuoVoBoard, DuoVoSchool, DuoVoBranch]:
        print s.__name__
        print_schema(s)