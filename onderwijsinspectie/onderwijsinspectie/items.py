from scrapy.item import Item, Field


class EducationalInstitution(Item):
    name = Field()
    address = Field()
    denomination = Field()
    website = Field()
    rating = Field()
    rating_date = Field()
    rating_excerpt = Field()
    rating_history = Field()
    reports = Field()
    education_sector = Field()
    education_structure = Field()
    owinsp_url = Field()
    owinsp_id = Field()


class VOSchool(EducationalInstitution):
    brin = Field()  # BRIN-nummer
    board_id = Field()  # Bevoegd gezagnummer
    board_name = Field()  # Bevoegd gezag
    branch_id = Field()  # Vestigingsnummer
    result_card = Field()  # Opbrengstenkaart URL


class POSchool(EducationalInstitution):
    pass
