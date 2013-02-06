import re

import requests
from scrapy.conf import settings
from scrapy.spider import BaseSpider
from scrapy.http import Request
from scrapy.selector import HtmlXPathSelector

from onderwijsscrapers.items import SchoolVOItem

# Depending on whether there is an explanation present in indicators 11 and 12,
# the classes of elements differ. Also, XPaths for both indicators are the same,
# so we process them using the same function.
IND11_12_XPATHS = {
    'with_explanation': {
        'general_table': '//table[@class="a94"]//tr[@valign="top"]',
        'general': 'td[@class="a57c"]//span/text()',
        'school_grade': 'td[@class="a63c"]/div/text()',
        'national_grade': 'td[@class="a67c"]/div/text()',
        'general_indicator': 'td[@class="a77cl"]/div/text()',
        'general_ind_grade': 'td[@class="a82c"]/div/text()',
        'edu_struct_table': '//table[@class="a170"]//tr[@valign="top"]',
        'edu_struct': 'td[@class="a130c"]//span/text()',
        'edu_grade': 'td[@class="a139c"]/div/text()',
        'edu_nat_grade': 'td[@class="a143c"]/div/text()',
        'edu_source': 'td[@class="a135c"]/div/text()',
        'edu_indicator': 'td[@class="a153cl"]/div/text()',
        'edu_ind_grade': 'td[@class="a158c"]/div/text()'
    },
    'without_explanation': {
        'general_table': '//table[@class="a93"]//tr[@valign="top"]',
        'general': 'td[@class="a56c"]//span/text()',
        'school_grade': 'td[@class="a62c"]/div/text()',
        'national_grade': 'td[@class="a66c"]/div/text()',
        'general_indicator': 'td[@class="a76cl"]/div/text()',
        'general_ind_grade': 'td[@class="a81c"]/div/text()',
        'edu_struct_table': '//table[@class="a169"]//tr[@valign="top"]',
        'edu_struct': 'td[@class="a129c"]//span/text()',
        'edu_grade': 'td[@class="a138c"]/div/text()',
        'edu_nat_grade': 'td[@class="a142c"]/div/text()',
        'edu_source': 'td[@class="a134c"]/div/text()',
        'edu_indicator': 'td[@class="a152cl"]/div/text()',
        'edu_ind_grade': 'td[@class="a157c"]/div/text()'
    }
}

LABELS = {
    'ind11': 'student_satisfaction',
    'ind12': 'parent_satisfaction'
}


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

            item['board_id'], item['brin'], item['branch_id'] =\
                                item['schoolvo_code'].strip().split('-')
            request.meta['item'] = SchoolVOItem(item)

            if school['pad_logo'] and school['pad_logo'].startswith('/'):
                request.meta['item']['logo_img_url'] = '%s%s'\
                    % (settings['SCHOOLVO_URL'], school['pad_logo'][1:])

            if school['pad_gebouw'] and school['pad_gebouw'].startswith('/'):
                request.meta['item']['building_img_url'] = '%s%s'\
                    % (settings['SCHOOLVO_URL'], school['pad_gebouw'][1:])

            requests.append(request)

        return requests

    def parse(self, response):
        school = response.meta['item']

        # A mapping of the indicators that we currently extract, and the
        # function used to do the extraction for that indicator
        extract_indicators = {
            'ind00': self.extract_ind00,
            'ind02': self.extract_ind02,
            'ind11': self.extract_ind11_12,
            'ind12': self.extract_ind11_12
        }

        # Extract the 'indicatoren' that are available for this school
        indicators = set(re.findall(r'"(ind\d{2})_leesmeer"', response.body))

        # Include the extractable indicatiors in the school's item
        school['available_indicators'] = set(extract_indicators.keys())\
            & indicators

        # Request the indicators that are both available and parseable
        # for this school. Send the school Item along with each request.
        for indicator in school['available_indicators']:
            indicator_detail_url = '%(schoolvo_url)svensters/%(school_id)s'\
                '/publish/%(indicator_id)s_leesmeer/%(indicator_id)s_leesmeer_'\
                '%(school_id)s.html' % {
                    'schoolvo_url': settings['SCHOOLVO_URL'],
                    'indicator_id': indicator.lower(),
                    'school_id': response.meta['item']['schoolvo_code']
                }

            yield Request(indicator_detail_url, meta={'item': school,
                'indicator': indicator}, callback=extract_indicators[indicator])

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

    def extract_ind11_12(self, response):
        """
        Extraction of indicator 11: "Kwaliteit - Tevredenheid leerlingen"
        Extraction of indicator 12: "Kwaliteit - Tevredenheid ouders"
        """
        school = response.meta['item']
        hxs = HtmlXPathSelector(response)

        # Element classes are different if an explanation is present. Select
        # the appropriate XPath expressions to use here.
        # However, this is not true for ALL schools, so that's why this ugly,
        # enormous conditional is here.
        explanation = hxs.select('//span[@class="a13"]/text()')
        if explanation:
            xpaths = IND11_12_XPATHS.get('with_explanation')
            general_table = hxs.select(xpaths['general_table'])
            if not general_table:
                xpaths = IND11_12_XPATHS.get('without_explanation')
        else:
            xpaths = IND11_12_XPATHS.get('without_explanation')
            general_table = hxs.select(xpaths['general_table'])
            if not general_table:
                xpaths = IND11_12_XPATHS.get('with_explanation')

        struct = None
        satisfaction = None
        satisfactions = []

        for row in hxs.select(xpaths['general_table']):
            general = row.select(xpaths['general'])

            if general:
                if satisfaction:
                    satisfactions.append(satisfaction)

                struct = u'school'
                school_grade = float(row.select(xpaths['school_grade'])\
                                        .extract()[0].replace(',', '.'))
                national_grade = row.select(xpaths['national_grade']).extract()

                if national_grade:
                    national_grade = float(national_grade[0].replace(',', '.'))
                else:
                    national_grade = None

                satisfaction = {
                        'education_structure': struct,
                        'grade': school_grade,
                        'national_grade': national_grade,
                        'indicators': []
                    }

                continue

            if struct:
                indicator = {
                    'indicator': row.select(xpaths['general_indicator'])\
                                    .extract()[0].strip(),
                    'grade': float(row.select(xpaths['general_ind_grade'])\
                                    .extract()[0].replace(',', '.'))
                }
                satisfaction['indicators'].append(indicator)

        # education structures
        struct = None
        for row in hxs.select(xpaths['edu_struct_table']):
            structure = row.select(xpaths['edu_struct'])

            if structure:
                if satisfaction:
                    satisfactions.append(satisfaction)

                struct = structure[0].extract().strip()
                grade = float(row.select(xpaths['edu_grade'])[0].extract()\
                                .replace(',', '.'))
                national_grade = row.select(xpaths['edu_nat_grade']).extract()
                source = row.select(xpaths['edu_source'])[0].extract()\
                            .replace('Bron: ', '')

                if national_grade:
                    national_grade = float(national_grade[0].replace(',', '.'))
                else:
                    national_grade = None

                satisfaction = {
                    'education_structure': struct,
                    'grade': grade,
                    'national_grade': national_grade,
                    'source': source,
                    'indicators': []
                }

                continue

            if struct:
                indicator = {
                    'indicator': row.select(xpaths['edu_indicator'])[0]\
                                    .extract().strip(),
                    'grade': float(row.select(xpaths['edu_ind_grade'])\
                                    .extract()[0].replace(',', '.'))
                }
                satisfaction['indicators'].append(indicator)

        # Append last satisfaction, if satisfacion exists
        if satisfaction:
            satisfactions.append(satisfaction)

        indicator = response.meta['indicator']

        school[LABELS[indicator]] = satisfactions

        school['available_indicators'].remove(indicator)
        if not school['available_indicators']:
            return school
