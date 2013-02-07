import csv
import cStringIO
import time
import re

import requests
from scrapy.spider import BaseSpider
from scrapy.http import Request
from scrapy.selector import HtmlXPathSelector

from onderwijsscrapers.items import DUOSchoolItem


class DUOSpider(BaseSpider):
    name = 'data.duo.nl'

    def start_requests(self):
        return [
            # Request('http://data.duo.nl/organisatie/open_onderwijsdata/'\
            #     'databestanden/vo/adressen/Adressen/vestigingen.asp',
            #     self.parse_branches),
            # Request('http://data.duo.nl/organisatie/open_onderwijsdata/'\
            #     'databestanden/vo/leerlingen/Leerlingen/vo_leerlingen2.asp',
            #     self.parse_student_residences),
            # Request('http://data.duo.nl/organisatie/open_onderwijsdata/'\
            #     'databestanden/vo/leerlingen/Leerlingen/vo_leerlingen1.asp',
            #     self.parse_students_per_branch),
            Request('http://data.duo.nl/organisatie/open_onderwijsdata/'\
                'databestanden/vo/leerlingen/Leerlingen/vo_leerlingen6.asp',
                self.student_graduations)
        ]

    def parse_branches(self, response):
        """
        Parse "02. Adressen alle vestigingen"
        """
        hxs = HtmlXPathSelector(response)

        available_csvs = {}
        csvs = hxs.select('//tr[.//a[contains(@href, ".csv")]]')
        for csv_file in csvs:
            year = csv_file.select('./td[1]/span/text()').extract()
            year = re.search(r'\d+ \w+ (\d{4})', year[0]).groups()
            year = int(year[0])

            csv_url = csv_file.select('.//a/@href').re(r'(.*\.csv)')[0]

            available_csvs['http://duo.nl%s' % csv_url] = year

        for csv_url, publication_year in available_csvs.iteritems():
            csv_file = requests.get(csv_url)
            csv_file.encoding = 'cp1252'
            csv_file = csv.DictReader(cStringIO.StringIO(csv_file.content\
                .decode('cp1252').encode('utf8')), delimiter=';')

            for row in csv_file:
                school = DUOSchoolItem()

                school['publication_year'] = publication_year
                school['name'] = row['VESTIGINGSNAAM'].strip()
                school['address'] = '%s %s' % (row['STRAATNAAM'].strip(),
                    row['HUISNUMMER-TOEVOEGING'].strip())
                school['zip_code'] = row['POSTCODE'].strip()
                school['city'] = row['PLAATSNAAM'].strip()

                if row['INTERNETADRES'].strip():
                    school['website'] = row['INTERNETADRES'].strip()
                else:
                    school['website'] = None

                if row['DENOMINATIE'].strip():
                    school['denomination'] = row['DENOMINATIE'].strip()
                else:
                    school['denomination'] = None

                if row['ONDERWIJSSTRUCTUUR'].strip():
                    school['education_structures'] = row['ONDERWIJSSTRUCTUUR']\
                        .strip().split('/')
                else:
                    school['education_structures'] = None

                if row['PROVINCIE'].strip():
                    school['province'] = row['PROVINCIE'].strip()
                else:
                    school['province'] = None

                if row['BEVOEGD GEZAG NUMMER'].strip():
                    school['board_id'] = int(row['BEVOEGD GEZAG NUMMER'].strip())
                else:
                    school['board_id'] = None

                if row['BRIN NUMMER'].strip():
                    school['brin'] = row['BRIN NUMMER'].strip()

                if row['VESTIGINGSNUMMER'].strip():
                    school['branch_id'] = int(row['VESTIGINGSNUMMER'].strip()\
                        .replace(row['BRIN NUMMER'], ''))

                if row['GEMEENTENAAM'].strip():
                    school['municipality'] = row['GEMEENTENAAM'].strip()
                else:
                    school['municipality'] = None

                if row['GEMEENTENUMMER'].strip():
                    school['municipality_code'] = int(row['GEMEENTENUMMER'].strip())
                else:
                    school['municipality_code'] = None

                if row['TELEFOONNUMMER'].strip():
                    school['phone'] = row['TELEFOONNUMMER'].strip()
                else:
                    school['phone'] = None

                if row['STRAATNAAM CORRESPONDENTIEADRES'].strip():
                    school['correspondence_address'] = '%s %s'\
                        % (row['STRAATNAAM CORRESPONDENTIEADRES'].strip(),
                           row['HUISNUMMER-TOEVOEGING CORRESPONDENTIEADRES'].strip())
                else:
                    school['correspondence_address'] = None

                if row['POSTCODE CORRESPONDENTIEADRES'].strip():
                    school['correspondence_zip'] = row['POSTCODE '\
                        'CORRESPONDENTIEADRES'].strip()
                else:
                    school['correspondence_zip'] = None

                if row['NODAAL GEBIED NAAM'].strip():
                    school['nodal_area'] = row['NODAAL GEBIED NAAM'].strip()
                else:
                    school['nodal_area'] = None

                if row['NODAAL GEBIED CODE'].strip():
                    school['nodal_area_code'] = int(row['NODAAL GEBIED CODE']\
                        .strip())
                else:
                    school['nodal_area_code'] = None

                if row['RPA-GEBIED NAAM'].strip():
                    school['rpa_area'] = row['RPA-GEBIED NAAM'].strip()
                else:
                    school['rpa_area'] = None

                if row['RPA-GEBIED CODE'].strip():
                    school['rpa_area_code'] = int(row['RPA-GEBIED CODE'].strip())
                else:
                    school['rpa_area_code'] = None

                if row['WGR-GEBIED NAAM'].strip():
                    school['wgr_area'] = row['WGR-GEBIED NAAM'].strip()
                else:
                    school['wgr_area'] = None

                if row['WGR-GEBIED CODE'].strip():
                    school['wgr_area_code'] = int(row['WGR-GEBIED CODE'].strip())
                else:
                    school['wgr_area_code'] = None

                if row['COROPGEBIED NAAM'].strip():
                    school['corop_area'] = row['COROPGEBIED NAAM'].strip()
                else:
                    school['corop_area'] = None

                if row['COROPGEBIED CODE'].strip():
                    school['corop_area_code'] = int(row['COROPGEBIED CODE'].strip())
                else:
                    school['corop_area_code'] = None

                if row['ONDERWIJSGEBIED NAAM'].strip():
                    school['education_area'] = row['ONDERWIJSGEBIED NAAM'].strip()
                else:
                    school['education_area'] = None

                if row['ONDERWIJSGEBIED CODE'].strip():
                    school['education_area_code'] = int(row['ONDERWIJSGEBIED CODE']\
                        .strip())
                else:
                    school['education_area_code'] = None

                if row['RMC-REGIO NAAM'].strip():
                    school['rmc_region'] = row['RMC-REGIO NAAM'].strip()
                else:
                    school['rmc_region'] = None

                if row['RMC-REGIO CODE'].strip():
                    school['rmc_region_code'] = int(row['RMC-REGIO CODE'].strip())
                else:
                    school['rmc_region_code'] = None

                yield school

    def get_boards(self):
        pass

    def parse_students_per_branch(self, response):
        """
        Parse "01. Leerlingen per vestiging naar onderwijstype, lwoo
        indicatie, sector, afdeling, opleiding"
        """
        hxs = HtmlXPathSelector(response)

        available_csvs = {}
        csvs = hxs.select('//tr[.//a[contains(@href, ".csv")]]')
        for csv_file in csvs:
            print csv_file
            year = csv_file.select('./td[1]/span/text()').extract()
            year = re.search(r'\d+ \w+ (\d{4})', year[0]).groups()
            year = int(year[0])

            csv_url = csv_file.select('.//a/@href').re(r'(.*\.csv)')[0]

            available_csvs['http://duo.nl%s' % csv_url] = year

        for csv_url, publication_year in available_csvs.iteritems():
            csv_file = requests.get(csv_url)
            csv_file.encoding = 'cp1252'
            csv_file = csv.DictReader(cStringIO.StringIO(csv_file.content\
                .decode('cp1252').encode('utf8')), delimiter=';')

            student_educations = {}
            school_ids = {}

            for row in csv_file:
                school_id = '%s-%s' % (row['BRIN NUMMER'].strip(),
                    row['VESTIGINGSNUMMER'].strip().zfill(2))

                school_ids[school_id] = {
                    'brin': row['BRIN NUMMER'].strip(),
                    'branch_id': int(row['VESTIGINGSNUMMER'].strip()\
                        .replace(row['BRIN NUMMER'], ''))
                }

                if school_id not in student_educations:
                    student_educations[school_id] = []

                education_type = {}

                department = row['AFDELING'].strip()
                if department:
                    education_type['department'] = department
                    if education_type['department'].lower() == 'n.v.t.':
                        education_type['department'] = False
                else:
                    education_type['department'] = None

                if row['ELEMENTCODE'].strip():
                    education_type['elementcode'] = int(row['ELEMENTCODE']\
                        .strip())
                else:
                    education_type['elementcode'] = None

                lwoo = row['LWOO INDICATIE'].strip().lower()
                if lwoo:
                    if lwoo == 'j':
                        education_type['lwoo'] = True
                    elif lwoo == 'n':
                        education_type['lwoo'] = False
                    else:
                        education_type['lwoo'] = None
                else:
                    education_type['lwoo'] = None

                vmbo_sector = row['VMBO SECTOR'].strip()
                if vmbo_sector:
                    if vmbo_sector.lower() == 'n.v.t.':
                        education_type['vmbo_sector'] = False
                    else:
                        education_type['vmbo_sector'] = vmbo_sector
                else:
                    education_type['vmbo_sector'] = None

                naam = row['OPLEIDINGSNAAM'].strip()
                if naam:
                    education_type['education_name'] = naam
                else:
                    education_type['education_name'] = None

                otype = row['ONDERWIJSTYPE VO EN LEER- OF VERBLIJFSJAAR'].strip()
                if otype:
                    education_type['education_structure'] = otype
                else:
                    education_type['education_structure'] = None

                for available_year in range(1, 7):
                    male = int(row['LEER- OF VERBLIJFSJAAR %s - MAN'
                        % available_year])
                    female = int(row['LEER- OF VERBLIJFSJAAR %s - VROUW'
                        % available_year])

                    education_type['year_%s' % available_year] = {
                        'male': male,
                        'female': female,
                        'total': male + female
                    }

                student_educations[school_id].append(education_type)

            for school_id, s_by_structure in student_educations.iteritems():
                school = DUOSchoolItem(
                    brin=school_ids[school_id]['brin'],
                    branch_id=school_ids[school_id]['branch_id'],
                    publication_year=publication_year,
                    students_by_structure=s_by_structure
                )

                yield school

    def parse_student_residences(self, response):
        """
        Parse "02. Leerlingen per vestiging naar postcode leerling en
        leerjaar"
        """
        hxs = HtmlXPathSelector(response)

        available_csvs = {}
        csvs = hxs.select('//tr[.//a[contains(@href, ".csv")]]')
        for csv_file in csvs:
            print csv_file
            year = csv_file.select('./td[1]/span/text()').extract()
            year = re.search(r'\d+ \w+ (\d{4})', year[0]).groups()
            year = int(year[0])

            csv_url = csv_file.select('.//a/@href').re(r'(.*\.csv)')[0]

            available_csvs['http://duo.nl%s' % csv_url] = year

        for csv_url, publication_year in available_csvs.iteritems():
            csv_file = requests.get(csv_url)
            csv_file.encoding = 'cp1252'
            csv_file = csv.DictReader(cStringIO.StringIO(csv_file.content\
                .decode('cp1252').encode('utf8')), delimiter=';')

            student_residences = {}
            school_ids = {}
            for row in csv_file:
                school_id = '%s-%s' % (row['BRIN NUMMER'].strip(),
                    row['VESTIGINGSNUMMER'].strip().zfill(2))

                school_ids[school_id] = {
                    'brin': row['BRIN NUMMER'].strip(),
                    'branch_id': int(row['VESTIGINGSNUMMER'].strip()\
                        .replace(row['BRIN NUMMER'], ''))
                }

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
                school = DUOSchoolItem(
                    brin=school_ids[school_id]['brin'],
                    branch_id=school_ids[school_id]['branch_id'],
                    publication_year=publication_year,
                    student_residences=residence
                )

                yield school

    def student_graduations(self, response):
        """
        Parse "06. Examenkandidaten en geslaagden"
        """
        hxs = HtmlXPathSelector(response)

        available_csvs = {}
        csvs = hxs.select('//tr[.//a[contains(@href, ".csv")]]')
        for csv_file in csvs:
            year = csv_file.select('./td[1]/span/text()').extract()
            year = re.search(r'\d+ \w+ (\d{4})', year[0]).groups()
            year = int(year[0])

            csv_url = csv_file.select('.//a/@href').re(r'(.*\.csv)')[0]

            available_csvs['http://duo.nl%s' % csv_url] = year

        for csv_url, publication_year in available_csvs.iteritems():
            csv_file = requests.get(csv_url)
            csv_file.encoding = 'cp1252'
            csv_file = csv.DictReader(cStringIO.StringIO(csv_file.content\
                .decode('cp1252').encode('utf8')), delimiter=';')

            school_ids = {}
            graduations_school_year = {}
            for row in csv_file:
                # Remove newline chars and strip leading and trailing
                # whitespace.
                for key in row.keys():
                    row[key.replace('\n', '')] = row[key].strip()
                    del row[key]

                brin = row['BRIN NUMMER']
                branch_id = int(row['VESTIGINGSNUMMER'].replace(brin, ''))
                school_id = '%s-%s' % (brin, branch_id)

                school_ids[school_id] = {
                    'brin': brin,
                    'branch_id': branch_id
                }

                if school_id not in graduations_school_year:
                    graduations_school_year[school_id] = {}

                # The years present in the CVS file (keys) and the
                # normalized form we will use (values)
                years = {
                    'SCHOOLJAAR 2007-2008': '2007-2008',
                    'SCHOOLJAAR 2008-2009': '2008-2009',
                    'SCHOOLJAAR 2009-2010': '2009-2010',
                    'SCHOOLJAAR 2010-2011': '2010-2011',
                    'SCHOOLJAAR 2011-2012': '2011-2012',
                }

                # Available breakdowns and their normalized form
                breakdown = {
                    'MAN': 'male',
                    'VROUW': 'female',
                    'ONBEKEND': 'unknown'
                }

                for year, y_normal in years.iteritems():
                    if y_normal not in graduations_school_year[school_id]:
                        graduations_school_year[school_id][y_normal] = {
                            'year': y_normal,
                            'failed': 0,
                            'passed': 0,
                            'candidates': 0,
                            'per_department': []
                        }

                    try:
                        candidates = row['EXAMENKANDIDATEN %s TOTAAL' % year]
                        if candidates:
                            candidates = int(candidates)
                        else:
                            continue
                    except KeyError:
                        candidates = 0
                    graduations_school_year[school_id][y_normal]['candidates'] += candidates

                    try:
                        passed = int(row['GESLAAGDEN %s TOTAAL' % year])
                    except KeyError:
                        passed = 0
                    graduations_school_year[school_id][y_normal]['passed'] += passed

                    graduations_school_year[school_id][y_normal]['failed'] += (candidates - passed)

                    department = {
                        'education_structure': row['ONDERWIJSTYPE VO'],
                        'department': row['OPLEIDINGSNAAM'],
                        'inspectioncode': row['INSPECTIECODE'],
                        'passed': {},
                        'failed': {},
                        'candidates': {},
                    }

                    for gender, gender_normal in breakdown.iteritems():
                        try:
                            candidates = row['EXAMENKANDIDATEN %s %s' % (year,
                                gender)]
                        except KeyError:
                            continue

                        # Skip gender if no value
                        if not candidates:
                            continue

                        candidates = int(candidates)
                        department['candidates'][gender_normal] = candidates

                        try:
                            passed = int(row['GESLAAGDEN %s %s' % (year, gender)])
                        except KeyError:
                            continue
                        department['passed'][gender_normal] = passed

                        failed = candidates - passed
                        department['failed'][gender_normal] = failed

                    graduations_school_year[school_id][y_normal]['per_department'].append(department)

            for school_id, graduations in graduations_school_year.iteritems():
                school = DUOSchoolItem(
                    brin=school_ids[school_id]['brin'],
                    branch_id=school_ids[school_id]['branch_id'],
                    publication_year=publication_year,
                    graduations=[graduations[year] for year in graduations]
                )

                yield school
