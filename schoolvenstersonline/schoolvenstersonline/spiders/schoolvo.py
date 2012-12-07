import re

import requests
from scrapy.conf import settings
from scrapy.spider import BaseSpider
from scrapy.http import Request
from scrapy.selector import HtmlXPathSelector

from schoolvenstersonline.items import SchoolItem


class SchoolVOSpider(BaseSpider):
    name = 'schoolvo.nl'

    def get_schools(self):
        """
        Schoolvo.nl provides a JSON 'endpoint' that will list all
        schools (with additional details) that are in their database.
        They use this endpoint to construct the map shown on the
        frontpage of the website. We will use the info to get to the
        detail pages of each school.
        """
        resp = requests.get('%sScholenOverzicht/data2.json'\
            % settings['SCHOOLVO_URL'])

        schools = []
        for school in resp.json['d']['SchoolSet']:
            school['schoolvo_detail_url'] = '%s?p_schoolcode=%s'\
                % (settings['SCHOOLVO_URL'], school['school_code'])

            schools.append(school)

        return schools

    def start_requests(self):
        requests = []

        for school in self.get_schools():
            # Construct an Item for each school and start with
            # requesting each school's overview pages.
            request = Request(school['schoolvo_detail_url'])
            request.meta['item'] = SchoolItem(
                schoolvo_id=school['school_id'],
                schoolvo_code=school['school_code'],
                name=school['naam'].strip(),
                address=school['adres'].strip(),
                zip_code=school['postcode'],
                city=school['woonplaats'],
                municipality=school['gemeente'],
                municipality_code=school['gemeente_code'],
                province=school['provincie'],
                longitude=school['longitude'],
                latitude=school['latitude'],
                phone=school['telefoon'],
                homepage=school['homepage'],
                email=school['e_mail'],
                schoolvo_status_id=school['venster_status_id'],
                schoolkompas_status_id=school['schoolkompas_status_id'],
                logo_img_url='%s%s' % (settings['SCHOOLVO_URL'],
                    school['pad_logo'][1:]),
                building_img_url='%s%s' % (settings['SCHOOLVO_URL'],
                    school['pad_gebouw'][1:]),
            )

            requests.append(request)

        return requests

    def parse(self, response):
        school = response.meta['item']

        # A mapping of the indicators that we currently extract, and the
        # function used to do the extraction for that indicator
        extract_indicators = {
            'ind00': self.extract_ind00,
            'ind02': self.extract_ind02
        }

        # Extract the 'indicatoren' that are available for this school
        indicators = set(re.findall(r'"(ind\d{2})_leesmeer"', response.body))

        # Include the extractable indicatiors in the school's item
        school['available_indicators'] = set(extract_indicators.keys())\
            & indicators

        # Request the indicators that are both available and parseable
        # for this schoool. Send the school Item along with each request.
        for indicator in school['available_indicators']:
            indicator_detail_url = '%(schoolvo_url)svensters/%(school_id)s'\
                '/publish/%(indicator_id)s_leesmeer/%(indicator_id)s_leesmeer_'\
                '%(school_id)s.html' % {
                    'schoolvo_url': settings['SCHOOLVO_URL'],
                    'indicator_id': indicator.lower(),
                    'school_id': response.meta['item']['schoolvo_code']
                }

            yield Request(indicator_detail_url, meta={'item': school},
                callback=extract_indicators[indicator])

    def extract_ind00(self, response):
        """
        Extraction of indicator 0: "Algemeen - Deze school"
        """
        school = response.meta['item']

        hxs = HtmlXPathSelector(response)

        structures = hxs.select('//tr[td/div/text() = "Onderwijsaanbod:"]/td[2]'\
            '/div/text()')
        if structures:
            school['education_structures'] = structures.extract()[0].split(' ')

        denomination = hxs.select('//tr[td/div/text() = "Denominatie:"]/td[2]'\
            '/div/text()')
        if denomination:
            school['denomination'] = denomination.extract()[0]

        board = hxs.select('//tr[td/div/text() = "Bestuur:"]/td[2]'\
            '/div/text()')
        if board:
            school['board'] = board.extract()[0]

        profile = hxs.select('string(//td[div/div/span/text() = "Profiel:"]'\
            '//div[position() > 1])')
        if profile:
            school['profile'] = profile.extract()[0].strip().replace(u'\xa0',
                u' ')

        school['available_indicators'].remove('ind00')
        if not school['available_indicators']:
            return school

    def extract_ind02(self, response):
        """
        Extraction of indicator 2: "Resultaten - Slaagpercentage"
        """
        school = response.meta['item']
        hxs = HtmlXPathSelector(response)

        graduations_year = hxs.select('//td[@class="a76l"]/text()')\
            .re(r'.* (\d{4}-\d{4})')
        if graduations_year:
            graduations = {
                'year': graduations_year[0]
            }

            current_sector = None
            for row in hxs.select('//table[@class="a141"]//tr'):
                sector = row.select('string(td[@class="a105cl"])').extract()

                if sector[0]:
                    current_sector = sector[0]
                    graduations[sector[0]] = {}
                    continue

                if current_sector:
                    cells = row.select('./td')
                    profile = cells[0].select('div/text()').extract()[0]
                    graduations[current_sector][profile] = {
                        'total': int(cells[1].select('div/text()').extract()[0]\
                            .replace('<', '')),
                        'successful': int(cells[2].select('div/text()')\
                            .extract()[0].replace('<', ''))
                    }

            school['graduations'] = graduations

        school['available_indicators'].remove('ind02')
        if not school['available_indicators']:
            return school
