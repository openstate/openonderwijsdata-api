from glob import glob
import json
from colander import (MappingSchema, SequenceSchema, SchemaNode, String, Int,
                      Length, Range, Date, Invalid, Float, Boolean)

import general_rules


class FinancialKeyIndicatorPerYear(MappingSchema):
    capitalization_ratio = SchemaNode(Float())
    contract_activities_div_gov_funding = SchemaNode(Float())
    contractactivities_div_total_profits = SchemaNode(Float())
    equity_div_total_profits = SchemaNode(Float())
    facilities_div_total_profits = SchemaNode(Float())
    general_reserve_div_total_income = SchemaNode(Float())
    gov_funding_div_total_profits = SchemaNode(Float())
    group = SchemaNode(String())
    housing_expenses_div_total_expenses = SchemaNode(Float())
    housing_investment_div_total_profits = SchemaNode(Float())
    investments_div_total_profits = SchemaNode(Float())
    investments_relative_to_equity = SchemaNode(Float())
    liquidity_current_ratio = SchemaNode(Float())
    liquidity_quick_ratio = SchemaNode(Float())
    operating_capital_div_total_profits = SchemaNode(Float())
    operating_capital = SchemaNode(Float())
    other_gov_funding_div_total_profits = SchemaNode(Float())
    profitability = SchemaNode(Float())
    solvency_1 = SchemaNode(Float())
    solvency_2 = SchemaNode(Float())
    staff_costs_div_gov_funding = SchemaNode(Float())
    staff_expenses_div_total_expenses = SchemaNode(Float())
    year = general_rules.year


class FinancialKeyIndicatorsPerYear(SequenceSchema):
    financial_key_indicator_per_year = FinancialKeyIndicatorPerYear()


class Dropout(MappingSchema):
    year = general_rules.year
    dropouts_with_mbo1_dimploma = SchemaNode(Int(), validator=Range(min=0,
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


class GraudationDepartmentCandidates(MappingSchema):
    male = SchemaNode(Int(), validator=Range(min=0))
    female = SchemaNode(Int(), validator=Range(min=0))
    unkown = SchemaNode(Int(), validator=Range(min=0))
    department = SchemaNode(String(), validator=Length(min=3, max=300))
    education_structure = general_rules.education_structure


class GraduationDepartment(MappingSchema):
    candidates = GraudationDepartmentCandidates()
    failed = GraudationDepartmentCandidates()
    passed = GraudationDepartmentCandidates()


class GraduationDepartments(SequenceSchema):
    department = GraduationDepartment()


class Graduation(MappingSchema):
    candidates = SchemaNode(Int(), validator=Range(min=0))
    failed = SchemaNode(Int(), validator=Range(min=0))
    passed = SchemaNode(Int(), validator=Range(min=0))
    per_department = GraduationDepartments()
    year = SchemaNode(String())


class Graduations(SequenceSchema):
    graduation = Graduation()


class StudentResidence(MappingSchema):
    municipality = general_rules.municipality
    municipality_code = general_rules.municipality_code
    city = general_rules.city
    zip_code = SchemaNode(String(), validator=Length(min=4, max=4))
    year_1 = SchemaNode(Int(), validator=Range(min=0))
    year_2 = SchemaNode(Int(), validator=Range(min=0))
    year_3 = SchemaNode(Int(), validator=Range(min=0))
    year_4 = SchemaNode(Int(), validator=Range(min=0))
    year_5 = SchemaNode(Int(), validator=Range(min=0))
    year_6 = SchemaNode(Int(), validator=Range(min=0))


class StudentResidences(SequenceSchema):
    student_residence = StudentResidence()


class StudentsEnrolledInStructure(MappingSchema):
    male = SchemaNode(Int(), validator=Range(min=0))
    female = SchemaNode(Int(), validator=Range(min=0))
    total = SchemaNode(Int(), validator=Range(min=0))


class StudentByStructure(MappingSchema):
    department = SchemaNode(String(), validator=Length(min=3, max=300))
    education_name = SchemaNode(String(), validator=Length(min=3, max=300))
    education_structure = general_rules.education_structure
    elementcode = SchemaNode(Int(), validator=Range(min=0))
    lwoo = SchemaNode(Boolean())
    vmbo_sector = SchemaNode(String(), validator=Length(min=3, max=300))
    year_1 = StudentsEnrolledInStructure()
    year_2 = StudentsEnrolledInStructure()
    year_3 = StudentsEnrolledInStructure()
    year_4 = StudentsEnrolledInStructure()
    year_5 = StudentsEnrolledInStructure()
    year_6 = StudentsEnrolledInStructure()


class StudentsByStructure(SequenceSchema):
    students_by_structure = StudentByStructure()

                                                                                                                                                              
#TODO:                                                                         
#class FinancialKeyIndicatorsPerYear                                           
                                                                                                                                                                                                                                             
                                                                                                                                                                                                                                                                                                                            
#TODO:                                                                         
#class AgesPerBranchByStudentWeight                                            
                                                                                                                                                                                                                                                                                                                                                                                                           
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                          
#TODO:                                                                         
#class WeightsPerSchool                                                        
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                       
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                      
#TODO:                                                                         
#class PupilsByOrigins             

class VavoStudents(MappingSchema):
     non_vavo = SchemaNode(Int()) # `AANTAL LEERLINGEN`
     vavo = SchemaNode(Int()) # `AANTAL VO LEERLINGEN UITBESTEED AAN VAVO`
     # (there's also a TOTAAL AANTAL LEERLINGEN sum column that we ignore)
class VavoStudents(SequenceSchema):
    vavo_students = VavoStudents()

class SPOStudentsByAdvice(MappingSchema):
    vso = SchemaNode(Int()) # `VSO`
    pro = SchemaNode(Int()) # `PrO`
    vmbo_bl = SchemaNode(Int()) # `VMBO BL`
    vmbo_bl_kl = SchemaNode(Int()) # `VMBO BL-KL`
    vmbo_kl = SchemaNode(Int()) # `VMBO KL`
    vmbo_kl_gt = SchemaNode(Int()) # `VMBO KL-GT`
    vmbo_gt = SchemaNode(Int()) # `VMBO GT`
    vmbo_gt_havo = SchemaNode(Int()) # `VMBO GT-HAVO`
    havo = SchemaNode(Int()) # `HAVO`
    havo_vwo = SchemaNode(Int()) # `HAVO-VWO`
    vwo = SchemaNode(Int()) # `VWO`
    unknown = SchemaNode(Int()) # `ONBEKEND`
class SPOStudentsByAdvice(SequenceSchema):
    spo_students_by_advice = SPOStudentsByAdvice()

class SPOStudentsByEduType(MappingSchema):
    spo_indication = SchemaNode(String()) # `INDICATIE SPECIAL BASIS ONDERWIJS`
    sbao = SchemaNode(Int()) # `SBAO`
    so = SchemaNode(Int()) # `SO`
    vso = SchemaNode(Int()) # `VSO`
class SPOStudentsByEduType(SequenceSchema):
    spo_students_by_edu_type = SPOStudentsByEduType()

class SPOStudentsPerCluster(MappingSchema):
    # http://duo.nl/includes/navigatie/openbare_informatie/waargebruikt.asp?item=Cluster
    cluster_1 = SchemaNode(Int())
    cluster_2 = SchemaNode(Int())
    cluster_3 = SchemaNode(Int())
    cluster_4 = SchemaNode(Int())
class SPOStudentsPerCluster(SequenceSchema):
    spo_students_per_cluster = SPOStudentsPerCluster()

class SPOStudentsByBirthyear(MappingSchema):
    birthyear = general_rules.year
    students = SchemaNode(Int())
class SPOStudentsByBirthyear(SequenceSchema):
    spo_students_by_birthyear = SPOStudentsByBirthyear()




class DuoVoBranch(MappingSchema):
    address = general_rules.Address()
    correspondence_address = general_rules.Address()
    name = general_rules.name
    branch_id = general_rules.branch_id
    board_id = general_rules.board_id
    brin = general_rules.brin
    corop_area = general_rules.corop_area
    corop_area_code = general_rules.corop_area_code
    denomination = general_rules.denomination
    education_area = general_rules.education_area
    education_area_code = general_rules.education_area_code
    education_structures = general_rules.EducationStructures()
    graduations = Graduations()
    graduations_reference_date = SchemaNode(Date())
    graduations_reference_url = general_rules.reference_url
    student_residences = StudentResidences()
    student_residences_reference_date = SchemaNode(Date())
    student_residences_reference_url = general_rules.reference_url
    students_by_structure = StudentsByStructure()
    municipality = general_rules.municipality
    municipality_code = general_rules.municipality_code
    nodal_area = general_rules.nodal_area
    nodal_area_code = general_rules.nodal_area_code
    phone = general_rules.phone
    province = general_rules.province
    reference_year = general_rules.reference_year
    rmc_region = general_rules.rmc_region
    rmc_region_code = general_rules.rmc_region_code
    rpa_area = general_rules.rpa_area
    rpa_area_code = general_rules.rpa_area_code
    website = general_rules.url
    wgr_area = general_rules.wgr_area
    wgr_area_code = general_rules.wgr_area_code


    vavo_students_reference_url = general_rules.website
    vavo_students_reference_date = SchemaNode(Date(), missing=True)
    vavo_students = VavoStudents()


class DuoVoBoard(MappingSchema):
    address = general_rules.Address()
    correspondence_address = general_rules.Address()
    board_id = general_rules.board_id
    name = general_rules.name
    phone = general_rules.phone
    municipality = general_rules.municipality
    municipality_code = general_rules.municipality_code
    administrative_office_id = SchemaNode(Int())
    denomination = general_rules.denomination
    financial_key_indicators_per_year_reference_date = SchemaNode(Date(),
        missing=True)
    reference_year = general_rules.reference_year
    website = general_rules.website

    vavo_students_reference_url = general_rules.website
    vavo_students_reference_date = SchemaNode(Date(), missing=True)
    vavo_students = VavoStudents()


class DuoVoSchool(MappingSchema):
    address = general_rules.Address()
    correspondence_address = general_rules.Address()
    board_id = general_rules.board_id
    brin = general_rules.brin
    denomination = general_rules.denomination
    corop_area = general_rules.corop_area
    corop_area_code = general_rules.corop_area
    dropouts = Dropouts(missing=True)
    dropouts_reference_date = SchemaNode(Date(), missing=True)
    dropouts_reference_url = general_rules.reference_url
    education_area = general_rules.education_area
    education_area_code = general_rules.education_area_code
    education_structures = general_rules.EducationStructures()
    municipality = general_rules.municipality
    municipality_code = general_rules.municipality_code
    nodal_area = general_rules.nodal_area
    nodal_area_code = general_rules.nodal_area_code
    phone = general_rules.phone
    province = general_rules.province
    reference_year = general_rules.reference_year
    rmc_region = general_rules.rmc_region
    rmc_region_code = general_rules.rmc_region_code
    rpa_area = general_rules.rpa_area
    rpa_area_code = general_rules.rpa_area_code
    website = general_rules.url
    wgr_area = general_rules.wgr_area
    wgr_area_code = general_rules.wgr_area_code

    # TODO:
    #students_prognosis = StudentPrognosis()
    students_prognosis_reference_date = SchemaNode(Date(), missing=True)
    students_prognosis_url = general_rules.website


class DuoPoBoard(MappingSchema):
    address = general_rules.Address()
    correspondence_address = general_rules.Address()
    board_id = general_rules.board_id

    name = general_rules.name
    phone = general_rules.phone
    municipality = general_rules.municipality
    municipality_code = general_rules.municipality_code
    administrative_office_id = SchemaNode(Int())
    denomination = general_rules.denomination
    # TODO:
    #financial_key_indicators_per_year = FinancialKeyIndicatorsPerYear()
    financial_key_indicators_per_year_reference_date = SchemaNode(Date(),
        missing=True)
    financial_key_indicators_per_year_url = general_rules.website
    reference_year = general_rules.reference_year
    website = general_rules.website


class DuoPoSchool(MappingSchema):
    address = general_rules.Address()
    correspondence_address = general_rules.Address()
    board_id = general_rules.board_id
    brin = general_rules.brin
    denomination = general_rules.denomination
    corop_area = general_rules.corop_area
    corop_area_code = general_rules.corop_area
    education_area = general_rules.education_area
    education_area_code = general_rules.education_area_code
    municipality = general_rules.municipality
    municipality_code = general_rules.municipality_code
    name = general_rules.name
    nodal_area = general_rules.nodal_area
    nodal_area_code = general_rules.nodal_area_code
    phone = general_rules.phone
    province = general_rules.province
    reference_year = general_rules.reference_year
    rmc_region = general_rules.rmc_region
    rmc_region_code = general_rules.rmc_region_code
    rpa_area = general_rules.rpa_area
    rpa_area_code = general_rules.rpa_area_code
    website = general_rules.website
    wgr_area = general_rules.wgr_area
    wgr_area_code = general_rules.wgr_area_code

    spo_students_per_cluster = SPOStudentsPerCluster()
    spo_students_per_cluster_reference_date = SchemaNode(Date(), missing=True)
    spo_students_per_cluster_reference_url = general_rules.website


class DuoPoBranch(MappingSchema):
    address = general_rules.Address()
    # TODO:
    #ages_per_branch_by_student_weight = AgesPerBranchByStudentWeight()
    ages_per_branch_by_student_weight_reference_date = SchemaNode(Date(),
        missing=True)
    ages_per_branch_by_student_weight_reference_url = general_rules.website
    correspondence_address = general_rules.Address()
    name = general_rules.name
    branch_id = general_rules.branch_id
    board_id = general_rules.board_id
    brin = general_rules.brin
    corop_area = general_rules.corop_area
    corop_area_code = general_rules.corop_area_code
    denomination = general_rules.denomination
    education_area = general_rules.education_area
    education_area_code = general_rules.education_area_code
    municipality = general_rules.municipality
    municipality_code = general_rules.municipality_code
    nodal_area = general_rules.nodal_area
    nodal_area_code = general_rules.nodal_area_code
    phone = general_rules.phone
    province = general_rules.province
    # TODO:
    #pupils_by_origins = PupilsByOrigins()
    pupils_by_origins_reference_date = SchemaNode(Date(), missing=True)
    pupils_by_origins_reference_url = general_rules.website
    # TODO:
    #pupil_residences = PupilResidences()
    pupil_residences_reference_date = SchemaNode(Date(), missing=True)
    pupil_residences_reference_url = general_rules.website
    reference_year = general_rules.reference_year
    rmc_region = general_rules.rmc_region
    rmc_region_code = general_rules.rmc_region_code
    rpa_area = general_rules.rpa_area
    rpa_area_code = general_rules.rpa_area_code
    website = general_rules.url

    # TODO:
    #weights_per_school = WeightsPerSchool()
    weights_per_school_reference_date = SchemaNode(Date(), missing=True)
    weights_per_school_reference_url = general_rules.website
    
    wgr_area = general_rules.wgr_area
    wgr_area_code = general_rules.wgr_area_code

    # TODO:
    #po_student_year = StudentsPerStructurePerYear()
    po_student_year_reference_date = SchemaNode(Date(), missing=True)
    po_student_year_reference_url = general_rules.website
    
    spo_law = SchemaNode(String(), validator=Length(min=2, max=4))
    spo_edu_type = SchemaNode(String()) # possibly multiple with slash
    spo_cluster = SchemaNode(Int(), validator=Range(min=0, max=4))
    
    spo_students_by_birthyear_reference_url = general_rules.website
    spo_students_by_birthyear_reference_date = SchemaNode(Date(), missing=True)
    spo_students_by_birthyear = SPOStudentsByBirthyear()

    
    spo_students_by_edu_type_reference_url = general_rules.website
    spo_students_by_edu_type_reference_date = SchemaNode(Date(), missing=True)
    spo_students_by_edu_type = SPOStudentsByEduType()

    spo_students_by_advice_reference_url = general_rules.website
    spo_students_by_advice_reference_date = SchemaNode(Date(), missing=True)
    spo_students_by_advice = SPOStudentsByAdvice()

class DuoPaoCollaboration(MappingSchema):
    address = general_rules.Address()
    correspondence_address = general_rules.Address()
    collaboration_id = general_rules.collaboration_id
    reference_year = general_rules.reference_year


errors = []
def validate():
    schema = DuoVoBranch()

    for path in glob('../export/duo_vo_branches/*.json'):
        print path
        data = json.load(open(path, 'r'))
        try:
            schema.deserialize(data)
        except Invalid, e:
            errors.append(e)
            print e.asdict()
