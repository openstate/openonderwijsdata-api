# Scrapy settings for schoolvenstersonline project
#
# For simplicity, this file contains only the most important settings by
# default. All the other settings are documented here:
#
#     http://doc.scrapy.org/topics/settings.html
#

BOT_NAME = 'schoolvenstersonline'

SPIDER_MODULES = ['schoolvenstersonline.spiders']
NEWSPIDER_MODULE = 'schoolvenstersonline.spiders'

# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'schoolvenstersonline (+http://www.yourdomain.com)'

SCHOOLVO_URL = 'http://www.schoolvo.nl/'
