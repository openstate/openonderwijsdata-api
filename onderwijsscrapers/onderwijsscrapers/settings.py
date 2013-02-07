import os

BOT_NAME = 'onderwijsscrapers'
BOT_VERSION = '1.0'

SPIDER_MODULES = ['onderwijsscrapers.spiders']
ITEM_PIPELINES = ['onderwijsscrapers.pipelines.OnderwijsscrapersPipeline']
NEWSPIDER_MODULE = 'onderwijsscrapers.spiders'
USER_AGENT = '%s/%s' % (BOT_NAME, BOT_VERSION)

# Autothrottling settings
AUTOTHROTTLE_ENABLED = True
AUTOTHROTTLE_DEBUG = True

# Full filesystem path to the project
PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))

# Sentry exception logging config
SENTRY_DSN = 'http://8b3b10c7e19d4f9d82403f3ab4c40365:d1d53cce6e7c4981b3a6eb49be0f033b@sentry.dispectu.com/8'
import scrapy_sentry
scrapy_sentry.init(SENTRY_DSN)

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
        'url': '127.0.0.1:9200',
        'index': 'onderwijsinspectie',
        'doctype': 'vo_school'
    },
    'schoolvo.nl': {
        'url': '127.0.0.1:9200',
        'index': 'schoolvo',
        'doctype': 'school',
        'id_fields': ['brin', 'branch_id']
    },
    'duo_vo_branches': {
        'url': '127.0.0.1:9200',
        'index': 'duo',
        'doctype': 'vo_branch',
        'id_fields': ['publication_year', 'brin', 'branch_id']
    },
    'duo_vo_boards': {
        'url': '127.0.0.1:9200',
        'index': 'duo',
        'doctype': 'vo_board',
        'id_fields': ['board_id']
    },
    'duo_vo_schools': {
        'url': '127.0.0.1:9200',
        'index': 'duo',
        'doctype': 'vo_school',
        'id_fields': ['board_id']
    }
}
