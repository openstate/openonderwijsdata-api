import csv
import cStringIO
import time

import requests
from scrapy.spider import BaseSpider
from scrapy.http import Request
from scrapy.selector import HtmlXPathSelector

from onderwijsscrapers.items import DUOSchoolItem


class DUOSpider(BaseSpider):
    name = 'data.duo.nl'
    available_parsers = set(['branches', 'student_residences'])
    schools = {}

    def start_requests(self):
        return [
            Request('http://duo.nl/organisatie/open_onderwijsdata/'\
                'Voortgezet_onderwijs/datasets/adressen/Adressen/'\
                '02allevestigingen.asp', self.parse_branches),
            Request('http://data.duo.nl/organisatie/open_onderwijsdata/'\
                'databestanden/Voortgezet_onderwijs/leerlingen/Leerlingen/'\
                'vo_leerlingen2.asp', self.parse_student_residences)
        ]

    def parse_branches(self, response):
        """
        Parse "02. Adressen alle vestigingen"
        """
        hxs = HtmlXPathSelector(response)
        csv_url = hxs.select('//tr[td/text() = "Definitief"]//a/@href')\
            .re(r'(.*\.csv)')
        csv_file = requests.get('http://duo.nl%s' % csv_url[0])
        csv_file = csv.DictReader(cStringIO.StringIO(csv_file.content.decode('cp1252').encode('utf8')),
            delimiter=';')

        for row in csv_file:
            school_id = '%s-%s' % (row['BRIN NUMMER'].strip(),
                row['VESTIGINGSNUMMER'].strip().replace(row['BRIN NUMMER'], ''))

            if school_id in self.schools:
                school = self.schools[school_id]
            else:
                school = DUOSchoolItem()
                self.schools[school_id] = school

            school['name'] = row['VESTIGINGSNAAM'].strip()
            school['address'] = '%s %s' % (row['STRAATNAAM'].strip(),
                row['HUISNUMMER-TOEVOEGING'].strip())
            school['zip_code'] = row['POSTCODE'].strip()
            school['city'] = row['PLAATSNAAM'].strip()

            if row['INTERNETADRES'].strip():
                school['website'] = row['INTERNETADRES'].strip()

            if row['DENOMINATIE'].strip():
                school['denomination'] = row['DENOMINATIE'].strip()

            if row['ONDERWIJSSTRUCTUUR'].strip():
                school['education_structure'] = row['ONDERWIJSSTRUCTUUR']\
                    .strip().split('/')

            if row['PROVINCIE'].strip():
                school['province'] = row['PROVINCIE'].strip()

            if row['BEVOEGD GEZAG NUMMER'].strip():
                school['board_id'] = int(row['BEVOEGD GEZAG NUMMER'].strip())

            if row['BRIN NUMMER'].strip():
                school['brin'] = row['BRIN NUMMER'].strip()

            if row['VESTIGINGSNUMMER'].strip():
                school['branch_id'] = int(row['VESTIGINGSNUMMER'].strip()\
                    .replace(row['BRIN NUMMER'], ''))

            if row['GEMEENTENAAM'].strip():
                school['municipality'] = row['GEMEENTENAAM'].strip()

            if row['GEMEENTENUMMER'].strip():
                school['municipality_code'] = int(row['GEMEENTENUMMER'].strip())

            if row['TELEFOONNUMMER'].strip():
                school['phone'] = row['TELEFOONNUMMER'].strip()

            if row['STRAATNAAM CORRESPONDENTIEADRES'].strip():
                school['correspondence_address'] = '%s %s'\
                    % (row['STRAATNAAM CORRESPONDENTIEADRES'].strip(),
                       row['HUISNUMMER-TOEVOEGING CORRESPONDENTIEADRES'].strip())

            if row['POSTCODE CORRESPONDENTIEADRES'].strip():
                school['correspondence_zip'] = row['POSTCODE '\
                    'CORRESPONDENTIEADRES'].strip()

            if row['NODAAL GEBIED NAAM'].strip():
                school['nodal_area'] = row['NODAAL GEBIED NAAM'].strip()

            if row['NODAAL GEBIED CODE'].strip():
                school['nodal_area_code'] = int(row['NODAAL GEBIED CODE']\
                    .strip())

            if row['RPA-GEBIED NAAM'].strip():
                school['rpa_area'] = row['RPA-GEBIED NAAM'].strip()

            if row['RPA-GEBIED CODE'].strip():
                school['rpa_area_code'] = int(row['RPA-GEBIED CODE'].strip())

            if row['WGR-GEBIED NAAM'].strip():
                school['wgr_area'] = row['WGR-GEBIED NAAM'].strip()

            if row['WGR-GEBIED CODE'].strip():
                school['wgr_area_code'] = int(row['WGR-GEBIED CODE'].strip())

            if row['COROPGEBIED NAAM'].strip():
                school['corop_area'] = row['COROPGEBIED NAAM'].strip()

            if row['COROPGEBIED CODE'].strip():
                school['corop_area_code'] = int(row['COROPGEBIED CODE'].strip())

            if row['ONDERWIJSGEBIED NAAM'].strip():
                school['education_area'] = row['ONDERWIJSGEBIED NAAM'].strip()

            if row['ONDERWIJSGEBIED CODE'].strip():
                school['education_area_code'] = int(row['ONDERWIJSGEBIED CODE']\
                    .strip())

            if row['RMC-REGIO NAAM'].strip():
                school['rmc_region'] = row['RMC-REGIO NAAM'].strip()

            if row['RMC-REGIO CODE'].strip():
                school['rmc_region_code'] = int(row['RMC-REGIO CODE'].strip())

        self.available_parsers.remove('branches')
        if not self.available_parsers:
            for school in self.schools:
                yield self.schools[school]

    def parse_student_residences(self, response):
        """
        Parse "02. Leerlingen per vestiging naar postcode leerling en leerjaar"
        """
        hxs = HtmlXPathSelector(response)
        csv_url = hxs.select('//tr[td/text() = "Definitief"]//a/@href')\
            .re(r'(.*\.csv)')
        csv_file = requests.get('http://duo.nl%s' % csv_url[0])
        print csv_file.encoding
        csv_file.encoding = 'cp1252'
        csv_file = csv.DictReader(cStringIO.StringIO(csv_file.content\
            .decode('cp1252').encode('utf8')), delimiter=';')

        student_residences = {}
        for row in csv_file:
            school_id = '%s-%s' % (row['BRIN NUMMER'].strip(),
                row['VESTIGINGSNUMMER'].strip().zfill(2))
            if school_id not in student_residences:
                student_residences[school_id] = []

            student_residences[school_id].append({
                'zip_code': row['POSTCODE LEERLING'].strip(),
                'city': row['PLAATSNAAM LEERLING'].strip().capitalize(),
                'municipality': row['GEMEENTENAAM LEERLING'].strip(),
                'municipality_id': int(row['GEMEENTENUMMER LEERLING'].strip()),
                'year_1': int(row['LEER- OF VERBLIJFSJAAR 1']),
                'year_2': int(row['LEER- OF VERBLIJFSJAAR 2']),
                'year_3': int(row['LEER- OF VERBLIJFSJAAR 3']),
                'year_4': int(row['LEER- OF VERBLIJFSJAAR 4']),
                'year_5': int(row['LEER- OF VERBLIJFSJAAR 5']),
                'year_6': int(row['LEER- OF VERBLIJFSJAAR 6'])
            })

        for school_id, residence in student_residences.iteritems():
            if school_id in self.schools:
                self.schools[school_id]['student_residences'] = residence
            else:
                self.schools[school_id] = DUOSchoolItem(
                    student_residences=residence)

        self.available_parsers.remove('student_residences')
        if not self.available_parsers:
            for school in self.schools:
                yield self.schools[school]
