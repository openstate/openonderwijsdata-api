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

# Path to the file that holds all zipcodes (firs 4 digits!). This file
# is used for searching in the toezichtkaart.owinsp.nl databse.
ZIPCODES = os.path.join(PROJECT_ROOT, 'zips.txt')

SCHOOLVO_URL = 'http://www.schoolvo.nl/'

# Available methods are 'elasticsearch' and 'file'
EXPORT_METHOD = 'file'

# Directory to which scrape results should be saved (in case the file
# exporter is used).
EXPORT_DIR = os.path.join(PROJECT_ROOT, 'export')

ELESTIC_SEARCH = {
    'po.owinsp.nl': {
        'url': '',
        'index': '',
        'doctype': '',
    },
    'vo.owinsp.nl': {
        'url': '',
        'index': '',
        'doctype': ''
    },
    'schoolvo.nl': {
        'url': 'chimay.dispectu.com:9200',
        'index': 'schoolvo',
        'doctype': 'school',
    }
}
