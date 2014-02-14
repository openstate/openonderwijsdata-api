from scrapy.item import Item, Field


class SchoolItem(Item):
    name = Field()  # `naam`
    brin = Field()  # `BRIN-nummer`
    branch_id = Field()  # Vestigingsnummer
    address = Field()  # `adres`
    website = Field()  # `website` or `homepage`
    denomination = Field()  # `denominatie`


class SchoolVOItem(SchoolItem):
    education_structures = Field()  # `Onderwijsaanbod`
    # Holds the indicators that are available for this school
    available_indicators = Field()

    board_id = Field()  # Bevoegd gezagnummer
    schoolvo_id = Field()  # `school_id`
    schoolvo_code = Field()  # `school_code`
    municipality = Field()  # `gemeente`
    municipality_code = Field()  # `gemeente_code`
    province = Field()  # `provincie`
    longitude = Field()  # `longitude`
    latitude = Field()  # `latitude`
    phone = Field()  # `telefoon`
    email = Field()  # `e_mail`
    board = Field()  # `Bestuur` or `Bevoegd gezag`
    schoolvo_status_id = Field()  # `venster_status_id`
    schoolkompas_status_id = Field()  # `schoolkompas_status_id`
    logo_img_url = Field()  # `pad_logo`
    building_img_url = Field()  # `pad_gebouw`
    profile = Field()  # `Profiel`
    # graduations = Field()  # `Slaagpercentage`

    student_satisfaction = Field()  # `Tevredenheid leerlingen`
    student_satisfaction_url = Field()  # `Tevredenheid leerlingen` url

    parent_satisfaction = Field()  # `Tevredenheid ouders`
    parent_satisfaction_url = Field()  # `Tevredenheid ouders` url

    costs = Field()  # `Schoolkosten`
    costs_url = Field()  # `Schoolkosten` url

    avg_education_hours_per_student = Field()  # `Onderwijstijd`
    avg_education_hours_per_student_url = Field()  # `Onderwijstijd` url


class OnderwijsInspectieItem(SchoolItem):
    board_id = Field()  # Bevoegd gezagnummer
    rating_date = Field()
    rating_excerpt = Field()
    rating_history = Field()
    reports = Field()


class OwinspVOSchool(OnderwijsInspectieItem):
    board = Field()  # `Bestuur` or `Bevoegd gezag`
    education_structures = Field()  # `Onderwijsaanbod`
    result_card_url = Field()  # Opbrengstenkaart URL

    current_ratings = Field()

    # Field used to merge all sectors of a single school into one item.
    # This field is not stored.
    education_structures_to_scrape = Field()


class OwinspPOSchool(OnderwijsInspectieItem):
    owinsp_id = Field()
    current_rating = Field()  # A PO school has only one rating


class DuoVoBranch(SchoolItem):
    education_structures = Field()  # `Onderwijsaanbod`
    ignore_id_fields = Field()
    reference_year = Field()  # peiljaar
    province = Field()  # `provincie`
    board_id = Field()  # Bevoegd gezagnummer
    municipality = Field()  # `Gemeente naam`
    municipality_code = Field()  # `Gemeente nummer`
    phone = Field()  # `telefoonnummer`
    correspondence_address = Field()
    nodal_area = Field()  # `NODAAL GEBIED NAAM`
    nodal_area_code = Field()  # `NODAAL GEBIED CODE`
    rpa_area = Field()  # `RPA GEBIED NAAM`
    rpa_area_code = Field()  # `RPA GEBIED CODE`
    wgr_area = Field()  # `WGR GEBIED NAAM`
    wgr_area_code = Field()  # `WGR GEBIED CODE`
    corop_area = Field()  # `COROP GEBIED NAAM`
    corop_area_code = Field()  # `COROP GEBIED CODE`
    education_area = Field()  # `ONDERWIJS GEBIED NAAM`
    education_area_code = Field()  # `ONDERWIJS GEBIED CODE`
    rmc_region = Field()  # `RMC REGIO NAAM`
    rmc_region_code = Field()  # `RMC REGIO CODE`

    # Contents of "02. Leerlingen per vestiging naar postcode leerling
    # en leerjaar"
    student_residences_url = Field()
    student_residences_reference_date = Field()
    student_residences = Field()

    # Contents of "01. Leerlingen per vestiging naar onderwijstype, lwoo
    # indicatie, sector, afdeling, opleiding"
    students_by_structure_url = Field()
    students_by_structure_reference_date = Field()
    students_by_structure = Field()

    # Contents of "06. Examenkandidaten en geslaagden"
    graduations_reference_url = Field()
    graduations_reference_date = Field()
    graduations = Field()

    # Contents of "07. Geslaagden, gezakten en gemiddelde examencijfers
    # per instelling"
    exam_grades_reference_url = Field()
    exam_grades_reference_date = Field()
    exam_grades = Field()

    # Contents of "08. Examenkandidaten vmbo en examencijfers per vak
    # per instelling"
    vmbo_exam_grades_reference_url = Field()
    vmbo_exam_grades_reference_date = Field()
    vmbo_exam_grades_per_course = Field()

    # Contents of "09. Examenkandidaten havo en examencijfers per vak
    # per instelling"
    havo_exam_grades_reference_url = Field()
    havo_exam_grades_reference_date = Field()
    havo_exam_grades_per_course = Field()

    # Contents of "10. Examenkandidaten vwo en examencijfers per vak
    # per instelling"
    vwo_exam_grades_reference_url = Field()
    vwo_exam_grades_reference_date = Field()
    vwo_exam_grades_per_course = Field()


class DuoVoSchool(SchoolItem):
    education_structures = Field()  # `Onderwijsaanbod`
    ignore_id_fields = Field()
    reference_year = Field()  # peiljaar
    province = Field()  # `provincie`
    board_id = Field()  # Bevoegd gezagnummer
    municipality = Field()  # `Gemeente naam`
    municipality_code = Field()  # `Gemeente nummer`
    phone = Field()  # `telefoonnummer`
    correspondence_address = Field()
    nodal_area = Field()  # `NODAAL GEBIED NAAM`
    nodal_area_code = Field()  # `NODAAL GEBIED CODE`
    rpa_area = Field()  # `RPA GEBIED NAAM`
    rpa_area_code = Field()  # `RPA GEBIED CODE`
    wgr_area = Field()  # `WGR GEBIED NAAM`
    wgr_area_code = Field()  # `WGR GEBIED CODE`
    corop_area = Field()  # `COROP GEBIED NAAM`
    corop_area_code = Field()  # `COROP GEBIED CODE`
    education_area = Field()  # `ONDERWIJS GEBIED NAAM`
    education_area_code = Field()  # `ONDERWIJS GEBIED CODE`
    rmc_region = Field()  # `RMC REGIO NAAM`
    rmc_region_code = Field()  # `RMC REGIO CODE`

    # Contents of "02. Vsv in het voortgezet onderwijs per vo instelling"
    dropouts_per_year_url = Field()
    dropouts_per_year_reference_date = Field()
    dropouts_per_year = Field()


class DuoVoBoard(Item):
    ignore_id_fields = Field()
    reference_year = Field()  # peiljaar
    board_id = Field()  # `Bevoegd gezagnummer`
    name = Field()  # `BEVOEGD GEZAG NAAM`
    address = Field()  # `adres`
    zip_code = Field()  # `postcode`
    city = Field()  # `woonplaats`
    correspondence_address = Field()
    municipality = Field()  # `Gemeente naam`
    municipality_code = Field()  # `Gemeente nummer`
    phone = Field()  # `telefoonnummer`
    website = Field()  # `website` or `homepage`
    denomination = Field()  # `denominatie`
    administrative_office_id = Field()  # `ADMINISTRATIEKANTOORNUMMER`

    # Contents of "15. Kengetallen"
    financial_key_indicators_per_year_url = Field()
    financial_key_indicators_per_year_reference_date = Field()
    financial_key_indicators_per_year = Field()


class DuoPoBoard(Item):
    ignore_id_fields = Field()
    reference_year = Field()  # peiljaar
    board_id = Field()  # `Bevoegd gezagnummer`
    name = Field()  # `BEVOEGD GEZAG NAAM`
    address = Field()  # `adres`
    correspondence_address = Field()
    municipality = Field()  # `Gemeente naam`
    municipality_code = Field()  # `Gemeente nummer`
    phone = Field()  # `telefoonnummer`
    website = Field()  # `website` or `homepage`
    denomination = Field()  # `denominatie`
    administrative_office_id = Field()  # `ADMINISTRATIEKANTOORNUMMER`

    # Contents of "15. Kengetallen"
    financial_key_indicators_per_year_url = Field()
    financial_key_indicators_per_year_reference_date = Field()
    financial_key_indicators_per_year = Field()

    # Contents of "07. Leerlingen primair onderwijs per bevoegd gezag naar denominatie en onderwijssoort"
    students_per_edu_type_reference_url = Field()
    students_per_edu_type_reference_date = Field()
    students_per_edu_type = Field()


class DuoPoSchool(SchoolItem):
    ignore_id_fields = Field()
    reference_year = Field()  # peiljaar
    province = Field()  # `provincie`
    board_id = Field()  # Bevoegd gezagnummer
    municipality = Field()  # `Gemeente naam`
    municipality_code = Field()  # `Gemeente nummer`
    phone = Field()  # `telefoonnummer`
    correspondence_address = Field()
    nodal_area = Field()  # `NODAAL GEBIED NAAM`
    nodal_area_code = Field()  # `NODAAL GEBIED CODE`
    rpa_area = Field()  # `RPA GEBIED NAAM`
    rpa_area_code = Field()  # `RPA GEBIED CODE`
    wgr_area = Field()  # `WGR GEBIED NAAM`
    wgr_area_code = Field()  # `WGR GEBIED CODE`
    corop_area = Field()  # `COROP GEBIED NAAM`
    corop_area_code = Field()  # `COROP GEBIED CODE`
    education_area = Field()  # `ONDERWIJS GEBIED NAAM`
    education_area_code = Field()  # `ONDERWIJS GEBIED CODE`
    rmc_region = Field()  # `RMC REGIO NAAM`
    rmc_region_code = Field()  # `RMC REGIO CODE`


class DuoPoBranch(SchoolItem):
    ignore_id_fields = Field()
    reference_year = Field()  # peiljaar
    province = Field()  # `provincie`
    board_id = Field()  # Bevoegd gezagnummer
    municipality = Field()  # `Gemeente naam`
    municipality_code = Field()  # `Gemeente nummer`
    phone = Field()  # `telefoonnummer`
    correspondence_address = Field()
    nodal_area = Field()  # `NODAAL GEBIED NAAM`
    nodal_area_code = Field()  # `NODAAL GEBIED CODE`
    rpa_area = Field()  # `RPA GEBIED NAAM`
    rpa_area_code = Field()  # `RPA GEBIED CODE`
    wgr_area = Field()  # `WGR GEBIED NAAM`
    wgr_area_code = Field()  # `WGR GEBIED CODE`
    corop_area = Field()  # `COROP GEBIED NAAM`
    corop_area_code = Field()  # `COROP GEBIED CODE`
    education_area = Field()  # `ONDERWIJS GEBIED NAAM`
    education_area_code = Field()  # `ONDERWIJS GEBIED CODE`
    rmc_region = Field()  # `RMC REGIO NAAM`
    rmc_region_code = Field()  # `RMC REGIO CODE`

    # Contents of "01. Leerlingen basisonderwijs naar leerlinggewicht en per
    # vestiging het schoolgewicht en impulsgebied"
    weights_per_school_reference_url = Field()
    weights_per_school_reference_date = Field()
    weights_per_school = Field()  # Dict of `GEWICHT 0`, `GEWICHT 0.3`,
                                  # `GEWICHT 1.2`, `SCHOOLGEWICHT` and
                                  # `IMPULSGEBIED`.

    # Contents of "02. Leerlingen basisonderwijs naar leeftijd"
    ages_per_branch_by_student_weight_reference_url = Field()
    ages_per_branch_by_student_weight_reference_date = Field()
    ages_per_branch_by_student_weight = Field()  # Dict of childrens ages
                                                  # (age (3/4)-14) by student weight.

    # Contents of "09. Leerlingen basisonderwijs met een niet-Nederlandse achtergrond naar geboorteland"
    students_by_origin_reference_url = Field()
    students_by_origin_reference_date = Field()
    students_by_origin = Field()

    # Contents of "11. Leerlingen primair onderwijs per gemeente naar postcode leerling en leeftijd"
    student_residences_reference_url = Field()
    student_residences_reference_date = Field()
    student_residences = Field()

class DuoPaoCollaboration(Item):
    reference_year = Field()
    ignore_id_fields = Field()
    collaboration = Field()  #ADMINISTRATIENUMMER
    collaboration_id = Field()  #SAMENWERKINGSVERBAND
    address = Field() #ADRES, POSTCODE, PLAATSNAAM
    correspondence_address = Field() #CORRESPONDENTIEADRES, 
                                     #POSTCODE CORRESPONDENTIEADRES
                                     #PLAATS CORRESPONDENTIEADRES
    
