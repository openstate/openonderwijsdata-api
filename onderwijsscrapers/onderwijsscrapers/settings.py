import os

BOT_NAME = 'onderwijsscrapers'
BOT_VERSION = '1.0'

SPIDER_MODULES = ['onderwijsscrapers.spiders']
# ITEM_PIPELINES = ['onderwijsscrapers.pipelines.OnderwijsscrapersPipeline']
NEWSPIDER_MODULE = 'onderwijsscrapers.spiders'
USER_AGENT = '%s/%s' % (BOT_NAME, BOT_VERSION)

# Autothrottling settings
AUTOTHROTTLE_ENABLED = True
AUTOTHROTTLE_DEBUG = True

# Full filesystem path to the project
PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))

# Path to the file that holds all zipcodes (first 4 digits!). This file
# is used for searching in the toezichtkaart.owinsp.nl databse.
ZIPCODES = os.path.join(PROJECT_ROOT, 'zips.txt')

SCHOOLVO_URL = 'http://www.schoolvo.nl/'

# Mapping of SchoolVO.nl JSON attribute names to the SchoolVOItem fields
SCHOOLVO_FIELD_MAPPING = {
    'schoolvo_id': 'school_id',
    'schoolvo_code': 'school_code',
    'name': 'naam',
    'address': 'adres',
    'zip_code': 'postcode',
    'city': 'woonplaats',
    'municipality': 'gemeente',
    'municipality_code': 'gemeente_code',
    'province': 'provincie',
    'longitude': 'longitude',
    'latitude': 'latitude',
    'phone': 'telefoon',
    'website': 'homepage',
    'email': 'e_mail',
    'schoolvo_status_id': 'venster_status_id',
    'schoolkompas_status_id': 'schoolkompas_status_id'
}

# Available methods are 'elasticsearch' and 'file'
EXPORT_METHOD = 'file'

# Directory to which scrape results should be saved (in case the file
# exporter is used).
EXPORT_DIR = os.path.join(PROJECT_ROOT, 'export')

ELASTIC_SEARCH = {
    'po.owinsp.nl': {
        'url': '',
        'index': '',
        'doctype': '',
    },
    'vo.owinsp.nl': {
        'url': 'chimay.dispectu.com:9200',
        'index': 'onderwijsinspectie',
        'doctype': 'vo_school'
    },
    'schoolvo.nl': {
        'url': 'chimay.dispectu.com:9200',
        'index': 'schoolvo',
        'doctype': 'school',
    },
    'data.duo.nl': {
        'url': 'chimay.dispectu.com:9200',
        'index': 'duo',
        'doctype': 'school',
    }
}
