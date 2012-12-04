# Scrapy settings for onderwijsinspectie project
#
# For simplicity, this file contains only the most important settings by
# default. All the other settings are documented here:
#
#     http://doc.scrapy.org/topics/settings.html
#

BOT_NAME = 'onderwijsinspectie'
BOT_VERSION = '1.0'
ITEM_PIPELINES = ['onderwijsinspectie.pipelines.OnderwijsinspectiePipeline']
SPIDER_MODULES = ['onderwijsinspectie.spiders']
NEWSPIDER_MODULE = 'onderwijsinspectie.spiders'
USER_AGENT = '%s/%s' % (BOT_NAME, BOT_VERSION)

# File holding all zipcodes (4 digits!)
ZIPCODES = '/Users/bart/Documents/Dispectu/onderwijsdata/'\
           'onderwijsinspectie/zips.txt'
# The education sector ('onderwijssector') to retrieve. Possbile values
# are 'PO' ('primair onderwijs'), 'VO' ('voortgezet onderwijs')
# TODO: there are more possible values, describe them!
EDUCATION_SECTOR = 'VO'

EXPORT_DIRECTORY = '/Users/bart/Desktop/scholen'
