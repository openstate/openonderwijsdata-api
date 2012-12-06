import json
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
            request = Request(school['schoolvo_detail_url'])
            request.meta['item'] = SchoolItem(
                schoolvo_id=school['school_id'],
                schoolvo_code=school['school_code'],
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
                    school['pad_logo']),
                building_img_url='%s%s' % (settings['SCHOOLVO_URL'],
                    school['pad_gebouw']),
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

        for indicator in school['available_indicators']:
            indicator_detail_url = '%(schoolvo_url)svensters/%(school_id)s'\
                '/publish/%(indicator_id)s_leesmeer/%(indicator_id)s_leesmeer_'\
                '%(school_id)s.html' % {
                    'schoolvo_url': settings['SCHOOLVO_URL'],
                    'indicator_id': indicator.lower(),
                    'school_id': response.meta['item']['schoolvo_code']
                }

            return Request(indicator_detail_url, meta={'item': school},
                callback=extract_indicators[indicator])

    def extract_ind00(self, response):
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
        school = response.meta['item']
        hxs = HtmlXPathSelector(response)

        graduations_year = hxs.select('//td[@class="a76l"]/text()')\
            .re(r'.* (\d{4}-\d{4})')
        if graduations_year:
            graduatins = {
                'year': graduations_year
            }

            current_sector = None
            for sector in hxs.select('//table[@class="a141"]//tr'):
                cells = sector.select('.//td')

                if cells[0].select('@class = "a105cl"'):
                    print cells[0].extract()

        school['available_indicators'].remove('ind02')
        if not school['available_indicators']:
            return school
