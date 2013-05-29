import os
import exporters

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

# Directory to which scrape results should be saved (in case the file
# exporter is used).
EXPORT_DIR = os.path.join(PROJECT_ROOT, 'export')

# Available methods are 'elasticsearch' and 'file'
EXPORT_METHODS = {
    'file': {
        'exporter': exporters.FileExporter,
        'options': {
            'export_dir': EXPORT_DIR,
            'create_tar': True,
            'remove_json': False
        }
    },
    'elasticsearch': {
        'exporter': exporters.ElasticSearchExporter,
        'options': {
            'url': '127.0.0.1:9200'
        }
    }
}

from validation.duo import DuoVoSchool, DuoVoBoard, DuoVoBranch
from validation.schoolvo import SchoolVOBranch
from validation.owinsp import OnderwijsInspectieVoBranch

EXPORT_SETTINGS = {
    'po.owinsp.nl': {
        'url': '',
        'index': '',
        'doctype': '',
    },
    'vo.owinsp.nl': {
        'validate': True,
        'schema': OnderwijsInspectieVoBranch,
        'validation_index': 'onderwijsdata_validation',
        'geocode': True,
        'geocode_fields': ['address'],
        'index': 'onderwijsinspectie',
        'doctype': 'vo_branch',
        'id_fields': ['brin', 'branch_id']
    },
    'schoolvo.nl': {
        'validate': True,
        'schema': SchoolVOBranch,
        'validation_index': 'onderwijsdata_validation',
        'geocode': True,
        'geocode_fields': ['address'],
        'index': 'schoolvo',
        'doctype': 'vo_branch',
        'id_fields': ['brin', 'branch_id']
    },
    'duo_vo_branches': {
        'validate': True,
        'schema': DuoVoBranch,
        'validation_index': 'onderwijsdata_validation',
        'geocode': True,
        'geocode_fields': ['address'],
        'index': 'duo',
        'doctype': 'vo_branch',
        'id_fields': ['reference_year', 'brin', 'branch_id']
    },
    'duo_vo_boards': {
        'validate': True,
        'schema': DuoVoBoard,
        'validation_index': 'onderwijsdata_validation',
        'geocode': True,
        'geocode_fields': ['address', 'correspondence_address'],
        'index': 'duo',
        'doctype': 'vo_board',
        'id_fields': ['reference_year', 'board_id']
    },
    'duo_vo_schools': {
        'validate': True,
        'schema': DuoVoSchool,
        'validation_index': 'onderwijsdata_validation',
        'geocode': True,
        'geocode_fields': ['address', 'correspondence_address'],
        'index': 'duo',
        'doctype': 'vo_school',
        'id_fields': ['reference_year', 'brin']
    }
}
