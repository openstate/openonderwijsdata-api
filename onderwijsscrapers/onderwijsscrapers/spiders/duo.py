import csv
import cStringIO

from scrapy.conf import settings
from scrapy.spider import BaseSpider
from scrapy.http import Request
from scrapy.selector import HtmlXPathSelector


class DUOSpider(BaseSpider):
    name = 'data.duo.nl'
    schools = {}

    def start_requests(self):
        return [Request('http://duo.nl/organisatie/open_onderwijsdata/'\
            'Voortgezet_onderwijs/datasets/adressen/Adressen/'\
            '02allevestigingen.asp')]

    def parse(self, response):
        hxs = HtmlXPathSelector(response)
        csv = hxs.select('//tr[td/text() = "Definitief"]//a/@href')\
            .re(r'(.*\.csv)')

        if csv:
            return Request('http://duo.nl%s' % csv[0], self.parse_branches)

    def parse_branches(self, response):
        """
        Parse "02. Adressen alle vestigingen"
        """
        csv_body = cStringIO.StringIO()
        print response.body
        csv_body.write(response.body)
        csv_file = csv.DictReader(csv_body)

        print csv_file.fieldnames
