from scrapy.item import Item, Field
from collections import defaultdict

class FlexibleItem(dict, Item):
    # perhaps add Field defaultdict here
    pass

SchoolItem = FlexibleItem
SchoolVOItem = FlexibleItem

OwinspVOSchool = FlexibleItem
OwinspPOSchool = FlexibleItem

DuoVoBranch = FlexibleItem
DuoVoSchool = FlexibleItem
DuoVoBoard = FlexibleItem
DuoPoBoard = FlexibleItem
DuoPoSchool = FlexibleItem
DuoPoBranch = FlexibleItem
DuoPaoCollaboration = FlexibleItem
DuoMboBoard = FlexibleItem
DuoMboInstitution = FlexibleItem
DuoHoBoard = FlexibleItem
DuoHoInstitution = FlexibleItem

OCWPoBranch = FlexibleItem
DANSVoBranch = FlexibleItem
ROASurvey = FlexibleItem
