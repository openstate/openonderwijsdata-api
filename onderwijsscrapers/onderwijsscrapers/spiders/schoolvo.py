import re

import requests
from scrapy.conf import settings
from scrapy.spider import BaseSpider
from scrapy.http import Request
from scrapy.selector import HtmlXPathSelector

from onderwijsscrapers.items import SchoolVOItem


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
        for school in resp.json()['d']['SchoolSet']:
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

            item = {}
            for field, value in settings.get('SCHOOLVO_FIELD_MAPPING')\
                                    .iteritems():
                schoolvo_value = school.get(value, None)

                # If there is a string value in de SchoolVO data, it is
                # probably entered by a human, so strip trailing/leading
                # whitespaces
                if schoolvo_value and type(schoolvo_value) == unicode:
                    schoolvo_value = schoolvo_value.strip()
                item[field] = schoolvo_value

            request.meta['item'] = SchoolVOItem(item)

            if school['pad_logo'] and school['pad_logo'].startswith('/'):
                request.meta['item']['logo_img_url'] = '%s%s'\
                    % (settings['SCHOOLVO_URL'], school['pad_logo'][1:])

            if school['pad_gebouw'] and school['pad_gebouw'].startswith('/'):
                request.meta['item']['building_img_url'] = '%s%s'\
                    % (settings['SCHOOLVO_URL'], school['pad_gebouw'][1:]),

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
            school['education_structure'] = structures.extract()[0].split(' ')

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
        graduations = []

        graduations_year = hxs.select('//td[@class="a76l"]/text()')\
            .re(r'.* (\d{4}-\d{4})')
        if graduations_year:
            # graduations = {
            #     'year': graduations_year[0]
            # }

            # explanation = hxs.select('//div[div/span/text() = "Toelichting:"]'\
            #     '/div[2]/span/text()').extract()
            # if explanation and len(explanation[0]) > 0:
            #     graduations['explanation'] = explanation[0].strip()

            current_sector = None
            graduation = None

            for row in hxs.select('//table[@class="a141"]//tr[@valign="top"]'):
                sector = row.select('string(td[@class="a105cl"])').extract()

                if sector[0]:
                    if graduation:
                        graduations.append(graduation)
                    current_sector = sector[0].strip()

                    total = int(row.select('.//td[@class="a109c"]/div/text()')[0].extract().replace('<', ''))
                    passed = int(row.select('.//td[@class="a113c"]/div/text()')[0].extract().replace('<', ''))

                    graduation = {
                        'education_structure': current_sector,
                        'total': total,
                        'passed': passed,
                        'failed': total - passed,
                        'profiles': []
                    }

                    # Go to next iteration of loop
                    continue

                if current_sector:
                    cells = row.select('./td')

                    profile = cells[0].select('div/text()').extract()[0].strip()

                    profile_total = int(cells[1].select('div/text()').extract()[0]\
                        .replace('<', ''))
                    profile_passed = int(cells[2].select('div/text()')\
                        .extract()[0].replace('<', ''))

                    graduation['profiles'].append({
                        'profile': profile,
                        'total': profile_total,
                        'passed': profile_passed,
                        'failed': profile_total - profile_passed
                    })

            # Append last graduation dict
            graduations.append(graduation)

        school['graduations'] = graduations

        school['available_indicators'].remove('ind02')
        if not school['available_indicators']:
            return school
