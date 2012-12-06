BOT_NAME = 'schoolvenstersonline'

SPIDER_MODULES = ['schoolvenstersonline.spiders']
NEWSPIDER_MODULE = 'schoolvenstersonline.spiders'
ITEM_PIPELINES = ['schoolvenstersonline.pipeline.SchoolVOPipeline']

AUTOTHROTTLE_ENABLED = True
AUTOTHROTTLE_DEBUG = True

SCHOOLVO_URL = 'http://www.schoolvo.nl/'

# Available methods are 'elasticsearch' and 'file'
EXPORT_METHOD = 'elasticsearch'

ES_URL = 'chimay.dispectu.com:9200'
ES_INDEX = 'schoolvo'
ES_DOCTYPE = 'school'

FILE_PATH = '/Users/justin/Desktop/schooolvo/'
