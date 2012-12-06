from scrapy.item import Item, Field


class SchoolItem(Item):
    # Holds the indicators that are available for this school
    available_indicators = Field()

    schoolvo_id = Field()  # `school_id`
    schoolvo_code = Field()  # `school_code`
    name = Field()  # `naam`
    address = Field()  # `adres`
    zip_code = Field()  # `postcode`
    city = Field()  # `woonplaats`
    municipality = Field()  # `gemeente`
    municipality_code = Field()  # `gemeente_code`
    province = Field()  # `provincie`
    longitude = Field()  # `longitude`
    latitude = Field()  # `latitude`
    phone = Field()  # `telefoon`
    homepage = Field()  # `hompage`
    email = Field()  # `e_mail`
    schoolvo_status_id = Field()  # `venster_status_id`
    schoolkompas_status_id = Field()  # `schoolkompas_status_id`
    logo_img_url = Field()  # `pad_logo`
    building_img_url = Field()  # `pad_gebouw`
    education_structures = Field()  # `Onderwijsaanbod`
    denomination = Field()  # `denominatie`
    board = Field()  # `Bestuur`
    profile = Field()  # `Profiel`
    graduations = Field()  # `Slaagpercentage`
