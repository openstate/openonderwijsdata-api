from scrapy.item import Item, Field


class SchoolItem(Item):
    name = Field()  # `naam`
    address = Field()  # `adres`
    denomination = Field()  # `denominatie`
    zip_code = Field()  # `postcode`
    city = Field()  # `woonplaats`
    website = Field()  # `website` or `homepage`
    board = Field()  # `Bestuur` or `Bevoegd gezag`
    education_structure = Field()  # `Onderwijsaanbod`


class SchoolVOItem(SchoolItem):
    # Holds the indicators that are available for this school
    available_indicators = Field()

    schoolvo_id = Field()  # `school_id`
    schoolvo_code = Field()  # `school_code`
    municipality = Field()  # `gemeente`
    municipality_code = Field()  # `gemeente_code`
    province = Field()  # `provincie`
    longitude = Field()  # `longitude`
    latitude = Field()  # `latitude`
    phone = Field()  # `telefoon`
    email = Field()  # `e_mail`
    schoolvo_status_id = Field()  # `venster_status_id`
    schoolkompas_status_id = Field()  # `schoolkompas_status_id`
    logo_img_url = Field()  # `pad_logo`
    building_img_url = Field()  # `pad_gebouw`
    profile = Field()  # `Profiel`
    graduations = Field()  # `Slaagpercentage`


class OnderwijsInspectieItem(SchoolItem):
    rating = Field()
    rating_date = Field()
    rating_excerpt = Field()
    rating_history = Field()
    reports = Field()
    education_sector = Field()
    owinsp_url = Field()
    owinsp_id = Field()


class VOSchool(OnderwijsInspectieItem):
    brin = Field()  # BRIN-nummer
    board_id = Field()  # Bevoegd gezagnummer
    branch_id = Field()  # Vestigingsnummer
    result_card = Field()  # Opbrengstenkaart URL


class POSchool(OnderwijsInspectieItem):
    pass
