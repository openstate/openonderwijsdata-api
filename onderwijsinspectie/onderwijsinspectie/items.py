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
