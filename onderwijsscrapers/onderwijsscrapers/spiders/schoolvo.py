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

                if schoolvo_value and field == 'city':
                    schoolvo_value = schoolvo_value.capitalize()

                # If there is a string value in de SchoolVO data, it is
                # probably entered by a human, so strip trailing/leading
                # whitespaces
                if schoolvo_value and type(schoolvo_value) == unicode:
                    schoolvo_value = schoolvo_value.strip()
                    try:
                        schoolvo_value = int(schoolvo_value)
                    except:
                        pass
                item[field] = schoolvo_value

            identifiers = item['schoolvo_code'].strip().split('-')
            item['board_id'] = int(identifiers[0])
            item['brin'] = identifiers[1]
            item['branch_id'] = int(identifiers[2])

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
            # 'ind02': self.extract_ind02,
            'ind11': self.extract_ind11_12,
            'ind12': self.extract_ind11_12,
            'ind17': self.extract_ind17,
            'ind19b': self.extract_ind19b
        }

        # Extract the 'indicatoren' that are available for this school
        indicators = set(re.findall(r'"(ind\d{2}\w?)_leesmeer"', response.body))

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
            school.pop('available_indicators')
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
        # Check whether data is present for this indicator
        if graduations_year:
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
            school.pop('available_indicators')
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
                        'average_grade': school_grade,
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
                    'average_grade': grade,
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
        school['%s_url' % (LABELS[indicator])] = response.url

        school['available_indicators'].remove(indicator)
        if not school['available_indicators']:
            school.pop('available_indicators')
            return school

    def extract_ind17(self, response):
        """
        Extraction of indicator 17: "Onderwijsbeleid - Onderwijstijd"
        """
        school = response.meta['item']
        hxs = HtmlXPathSelector(response)

        per_year = []

        edutime_year = hxs.select('//td[@class="a16l" or @class="a17l"]')
        # Check whether data is present for this indicator
        if edutime_year:
            year = None
            table = hxs.select('//table[@class="a83" or @class="a84"]')
            for row in table.select('.//tr[@valign="top"]'):
                edu_year = row.select('./td[@class="a47c" or @class="a48c"]')
                if edu_year:
                    if year:
                        per_year.append(year)

                    planned = int(row.select('./td[@class="a51c" or @class="a52c"]//text()')\
                                        .extract()[0].strip().replace('.', ''))
                    realised = int(row.select('./td[@class="a55c" or @class="a56c"]//text()')\
                                        .extract()[0].strip().replace('.', ''))

                    year = {
                        'year': edu_year.select('.//text()').extract()[0].strip(),
                        'planned': planned,
                        'realised': realised,
                        'per_structure': []
                    }

                    continue

                if year:
                    planned = int(row.select('./td[@class="a68c" or @class="a69c"]//text()')\
                                        .extract()[0].strip().replace('.', ''))
                    realised = int(row.select('./td[@class="a72c" or @class="a73c"]//text()')\
                                        .extract()[0].strip().replace('.', ''))
                    struct = {
                        'structure': row.select('./td[@class="a64cl" or @class="a65cl"]//text()')\
                                        .extract()[0].strip(),
                        'planned': planned,
                        'realised': realised
                    }
                    year['per_structure'].append(struct)

            # Append last year
            per_year.append(year)

        school['avg_education_hours_per_student'] = per_year
        school['avg_education_hours_per_student_url'] = response.url

        school['available_indicators'].remove(response.meta['indicator'])
        if not school['available_indicators']:
            school.pop('available_indicators')
            return school

    def extract_ind19b(self, response):
        """
        Extraction of indicator 19b: "Bedrijfsvoering - Schoolkosten"
        """
        school = response.meta['item']
        hxs = HtmlXPathSelector(response)

        costs_year = hxs.select('//td[@class="a15l" or @class="a16l"]/text()')

        per_year = []
        explanation = None
        signed_code_of_conduct = False
        documents = []

        # Check whether data is present for this indicator
        if costs_year:
            table = hxs.select('//table[@class="a65" or @class="a66" or\
                                @class="a73"]')
            if table:
                for row in table.select('.//tr[@valign="top"]'):
                    cells = row.select('.//td')
                    year = cells[0].select('.//text()').extract()[0]
                    if year and year != u'\xa0':
                        amount = cells[1].select('.//text()').extract()[0]
                        try:
                            amount = float(amount.replace(u'\u20ac', u'')\
                                                .replace(',', '.').strip())
                        except:
                            # If something weird happens, just use the value as
                            # found on SchoolVO
                            amount = amount.strip()

                        other_costs = cells[2].select('.//text()').extract()[0]
                        cost_per_year = {
                            'year': year.strip(),
                            'amount': amount,
                            'other_costs': other_costs.strip(),
                            'explanation': '',
                            'link': ''
                        }

                        expl = cells[3].select('.//text()').extract()[0]
                        if expl:
                            cost_per_year['explanation'] = expl.strip()

                        if len(cells) > 4:
                            link = cells[4].select('.//text()').extract()[0]
                            if link:
                                cost_per_year['link'] = link.strip()

                        per_year.append(cost_per_year)

            signed = hxs.select('//td[@class="a80c" or @class="a79c" or @class="a87c"]')

            if signed:
                signed_code_of_conduct = True

            explanation = hxs.select('//div[@class="a10" or @class="a9"]/span/text()')
            if explanation:
                explanation = u' '.join([unicode(exp.encode('utf8')
                                        .replace('\xc2\xa0', '').strip(), 'utf8')
                                        for exp in explanation.extract() if exp])

            docs = hxs.select('//a[contains(@href, ".pdf")]')
            if docs:
                root_url = 'http://%s' % '/'.join(response.url.split('/')[2:-1])
                for doc in docs:
                    doc = doc.select('./@href').re(r'window\.open\(\''\
                                                        '(.*?)\',\'')[0]
                    doc_url = '%s/%s' % (root_url, doc)
                    documents.append(doc_url)

        school['costs'] = {
            'url': response.url,
            'explanation': explanation,
            'per_year': per_year,
            'documents': documents,
            'signed_code_of_conduct': signed_code_of_conduct
        }

        school['available_indicators'].remove(response.meta['indicator'])
        if not school['available_indicators']:
            school.pop('available_indicators')
            return school
