import csv
import cStringIO
import locale
import xlrd
from datetime import datetime
from os import devnull
from zipfile import ZipFile

import requests
from scrapy.conf import settings
from scrapy.spider import BaseSpider
from scrapy.http import Request
from scrapy.selector import HtmlXPathSelector

from onderwijsscrapers.items import (DuoVoBoard, DuoVoSchool, DuoVoBranch,
                                     DuoPoBoard, DuoPoSchool, DuoPoBranch,
                                     DuoPaoCollaboration)

locale.setlocale(locale.LC_ALL, 'nl_NL.UTF-8')


def find_available_csvs(response):
    """ Get all URLS of CSV files on the DUO page """
    hxs = HtmlXPathSelector(response)
    available_csvs = {}
    csvs = hxs.select('//tr[.//a[contains(@href, ".csv")]]')
    for csv_file in csvs:
        ref_date = csv_file.select('./td[1]/span/text()').extract()
        ref_date = datetime.strptime(ref_date[0], '%d %B %Y').date()

        csv_url = csv_file.select('.//a/@href').re(r'(.*\.csv)')[0]

        available_csvs['http://duo.nl%s' % csv_url] = ref_date
    return available_csvs

def find_available_csvs(response):
    """ Get all URLS of ZIP files on the DUO page """
    hxs = HtmlXPathSelector(response)
    available_csvs = {}
    csvs = hxs.select('//tr[.//a[contains(@href, ".csv")]]')
    for csv_file in csvs:
        ref_date = csv_file.select('./td[1]/span/text()').extract()
        ref_date = datetime.strptime(ref_date[0], '%d %B %Y').date()

        csv_url = csv_file.select('.//a/@href').re(r'(.*\.csv)')[0]

        available_csvs['http://duo.nl%s' % csv_url] = ref_date
    return available_csvs

def parse_csv_file(csv_url):
    """ Download and parse CSV file """
    csv_file = requests.get(csv_url)
    csv_file.encoding = 'cp1252'
    csv_file = csv.DictReader(cStringIO.StringIO(csv_file.content
                  .decode('cp1252').encode('utf8')), delimiter=';')
    # todo: is this a dict or an iterator? can we do (whitespace) preprocessing here?
    return csv_file

def int_or_none(value):
    """
        Try to make `value` an int. If the string is not a number, 
        or empty, return None.
    """
    try: 
        return int(value)
    except ValueError:
        return None

class DuoVoBoards(BaseSpider):
    name = 'duo_vo_boards'

    def start_requests(self):
        return [
            Request('http://data.duo.nl/organisatie/open_onderwijsdata/'
                    'databestanden/vo/adressen/Adressen/besturen.asp',
                    self.parse_boards),
            Request('http://data.duo.nl/organisatie/open_onderwijsdata/'
                    'databestanden/vo/Financien/Financien/Kengetallen.asp',
                    self.parse_financial_key_indicators),
            Request('http://data.duo.nl/organisatie/open_onderwijsdata/'
                    'databestanden/vo/leerlingen/Leerlingen/vo_leerlingen4.asp',
                    self.parse_vavo_students),
        ]

    def parse_boards(self, response):
        """
        Parse "03. Adressen bevoegde gezagen"
        """

        for csv_url, reference_date in find_available_csvs(response).iteritems():
            reference_year = reference_date.year
            reference_date = str(reference_date)
            for row in parse_csv_file(csv_url):
                # strip leading and trailing whitespace.
                for key in row.keys():
                    row[key] = row[key].strip()

                board = DuoVoBoard()
                board['board_id'] = int(row['BEVOEGD GEZAG NUMMER'])
                board['name'] = row['BEVOEGD GEZAG NAAM']
                board['address'] = {
                    'street': '%s %s' % (row['STRAATNAAM'],
                                         row['HUISNUMMER-TOEVOEGING']),
                    'zip_code': row['POSTCODE'].replace(' ', ''),
                    'city': row['PLAATSNAAM']
                }

                board['correspondence_address'] = {}
                if row['STRAATNAAM CORRESPONDENTIEADRES']:
                    board['correspondence_address']['street'] = '%s %s'\
                        % (row['STRAATNAAM CORRESPONDENTIEADRES'],
                           row['HUISNUMMER-TOEVOEGING CORRESPONDENTIEADRES'])
                else:
                    board['correspondence_address']['street'] = None

                if row['POSTCODE CORRESPONDENTIEADRES']:
                    board['correspondence_address']['zip_code'] = row[
                        'POSTCODE CORRESPONDENTIEADRES'].replace(' ', '')
                else:
                    board['correspondence_address']['zip_code'] = None

                board['correspondence_address']['city'] = row[
                        'PLAATSNAAM CORRESPONDENTIEADRES'] or None

                board['municipality'] = row['GEMEENTENAAM'] or None

                board['municipality_code'] = int_or_none(row['GEMEENTENUMMER'])

                board['phone'] = row['TELEFOONNUMMER'] or None

                board['website'] = row['INTERNETADRES'] or None

                board['denomination'] = row['DENOMINATIE'] or None

                if row['ADMINISTRATIEKANTOORNUMMER']:
                    board['administrative_office_id'] = \
                        int(row['ADMINISTRATIEKANTOORNUMMER'])
                else:
                    board['administrative_office_id'] = None

                board['reference_year'] = reference_year
                board['ignore_id_fields'] = ['reference_year']
                yield board

    def parse_financial_key_indicators(self, response):
        """
        Parse "15. Kengetallen"
        """

        indicators_mapping = {
            'LIQUIDITEIT (CURRENT RATIO)': 'liquidity_current_ratio',
            'RENTABILITEIT': 'profitability',
            'SOLVABILITEIT 1': 'solvency_1',
            'SOLVABILITEIT 2': 'solvency_2',
            'ALGEMENE RESERVE / TOTALE BATEN': 'general_reserve_div_total_income',
            'BELEGGINGEN (T.O.V. EV)': 'investments_relative_to_equity',
            'CONTRACTACTIVITEITEN / RIJKSBIJDRAGE': 'contract_activities_div_gov_funding',
            'CONTRACTACTIVITEITEN / TOTALE BATEN': 'contractactivities_div_total_profits',
            'EIGEN VERMOGEN / TOTALE BATEN': 'equity_div_total_profits',
            'INVESTERING HUISVESTING / TOTALE BATEN': 'housing_investment_div_total_profits',
            'INVESTERINGEN (INVENT.+APP.) / TOTALE BATEN': 'investments_div_total_profits',
            'KAPITALISATIEFACTOR': 'capitalization_ratio',
            'LIQUIDITEIT (QUICK RATIO)': 'liquidity_quick_ratio',
            'OV. OVERHEIDSBIJDRAGEN / TOT. BATEN': 'other_gov_funding_div_total_profits',
            'PERSONEEL / RIJKSBIJDRAGEN': 'staff_costs_div_gov_funding',
            'PERSONELE LASTEN / TOTALE LASTEN': 'staff_expenses_div_total_expenses',
            'RIJKSBIJDRAGEN / TOTALE BATEN': 'gov_funding_div_total_profits',
            'VOORZIENINGEN /TOTALE BATEN': 'facilities_div_total_profits',
            #'WEERSTANDSVERMOGEN (-/- MVA)': '',
            #'WEERSTANDSVERMOGEN VO TOTALE BN.': '',
            'WERKKAPITAAL / TOTALE BATEN': 'operating_capital_div_total_profits',
            'HUISVESTINGSLASTEN / TOTALE LASTEN': 'housing_expenses_div_total_expenses',
            'WERKKAPITAAL': 'operating_capital',
        }

        for csv_url, reference_date in find_available_csvs(response).iteritems():
            reference_year = reference_date.year
            reference_date = str(reference_date)
            indicators_per_board = {}
            for row in parse_csv_file(csv_url):
                # strip leading and trailing whitespace.
                for key in row.keys():
                    row[key] = row[key].strip()

                board_id = int(row['BEVOEGD GEZAG NUMMER'])
                if board_id not in indicators_per_board:
                    indicators_per_board[board_id] = []

                indicators = {}
                indicators['year'] = int(row['JAAR'])
                indicators['group'] = row['GROEPERING']

                for ind, ind_norm in indicators_mapping.iteritems():
                    indicators[ind_norm] = float(row[ind].replace('.', '')
                                                         .replace(',', '.'))

                indicators_per_board[board_id].append(indicators)

            for board_id, indicators in indicators_per_board.iteritems():
                board = DuoVoBoard(
                    board_id=board_id,
                    reference_year=reference_year,
                    financial_key_indicators_per_year_url=csv_url,
                    financial_key_indicators_per_year_reference_date=reference_date,
                    financial_key_indicators_per_year=indicators
                )

                yield board

    def parse_vavo_students(self, response):
        """
        Primair onderwijs > Leerlingen
        Parse "04 Leerlingen per bestuur en denominatie (vavo apart)"
        """

        for csv_url, reference_date in find_available_csvs(response).iteritems():
            reference_year = reference_date.year
            reference_date = str(reference_date)
            vavo_students_per_school = {}

            for row in parse_csv_file(csv_url):

                board_id = int(row['BEVOEGD GEZAG NUMMER'].strip())

                vavo_students = {
                    'non_vavo' : int(row['AANTAL LEERLINGEN'] or 0),
                    'vavo' : int(row['AANTAL VO LEERLINGEN UITBESTEED AAN VAVO'] or 0),
                }

                if board_id not in vavo_students_per_school:
                    vavo_students_per_school[board_id] = []
                vavo_students_per_school[board_id].append(vavo_students)

            for board_id, per_school in vavo_students_per_school.iteritems():
                school = DuoVoBranch(
                    board_id=board_id,
                    reference_year=reference_year,
                    vavo_students_reference_url=csv_url,
                    vavo_students_reference_date=reference_date,
                    vavo_students=per_school,
                )
                yield school

class DuoVoSchools(BaseSpider):
    name = 'duo_vo_schools'

    def start_requests(self):
        return [
            # Request('http://data.duo.nl/organisatie/open_onderwijsdata/'
            #         'databestanden/vo/adressen/Adressen/hoofdvestigingen.asp',
            #         self.parse_schools),
            # Request('http://data.duo.nl/organisatie/open_onderwijsdata/'
            #         'databestanden/vschoolverlaten/vsv_voortgezet.asp',
            #         self.parse_dropouts),
            # Request('http://data.duo.nl/organisatie/open_onderwijsdata/'
            #         'databestanden/vo/leerlingen/Leerlingen/vo_leerlingen11.asp',
            #         self.parse_students_prognosis),
            Request('http://data.duo.nl/organisatie/open_onderwijsdata/'
                    'databestanden/passendow/Adressen/Adressen/passend_vo_6.asp',
                    self.parse_vo_lo_collaboration),
            Request('http://data.duo.nl/organisatie/open_onderwijsdata/'
                    'databestanden/passendow/Adressen/Adressen/passend_vo_8.asp',
                    self.parse_pao_collaboration),
        ]

    def parse_schools(self, response):
        """
        Parse: "01. Adressen hoofdvestigingen"
        """

        # Fields that do not need additonal processing
        school_fields = {
            'BRIN NUMMER': 'brin',
            'PROVINCIE': 'province',
            'INSTELLINGSNAAM': 'name',
            'GEMEENTENAAM': 'municipality',
            'DENOMINATIE': 'denomination',
            'INTERNETADRES': 'website',
            'TELEFOONNUMMER': 'phone',
            'ONDERWIJSGEBIED NAAM': 'education_area',
            'NODAAL GEBIED NAAM': 'nodal_area',
            'RPA-GEBIED NAAM': 'rpa_area',
            'WGR-GEBIED NAAM': 'wgr_area',
            'COROPGEBIED NAAM': 'corop_area',
            'RMC-REGIO NAAM': 'rmc_region'
        }

        for csv_url, reference_date in find_available_csvs(response).iteritems():
            reference_year = reference_date.year
            reference_date = str(reference_date)
            for row in parse_csv_file(csv_url):
                # strip leading and trailing whitespace.
                for key in row.keys():
                    value = row[key].strip()
                    row[key] = value or None

                school = DuoVoSchool()
                school['board_id'] = int(row['BEVOEGD GEZAG NUMMER'])
                school['address'] = {
                    'street': '%s %s' % (row['STRAATNAAM'],
                                         row['HUISNUMMER-TOEVOEGING']),
                    'city': row['PLAATSNAAM'],
                    'zip_code': row['POSTCODE'].replace(' ', '')
                }

                school['correspondence_address'] = {
                    'street': '%s %s' % (row['STRAATNAAM CORRESPONDENTIEADRES'],
                                         row['HUISNUMMER-TOEVOEGING '
                                             'CORRESPONDENTIEADRES']),
                    'city': row['PLAATSNAAM CORRESPONDENTIEADRES'],
                    'zip_code': row['POSTCODE CORRESPONDENTIEADRES']
                }

                school['municipality_code'] = int_or_none(row['GEMEENTENUMMER'])
                school['education_structures'] = row['ONDERWIJSSTRUCTUUR']
                if school['education_structures']:
                    school['education_structures'] = school['education_structures'].split('/')

                if row['COROPGEBIED CODE']:
                    school['corop_area_code'] = int(row['COROPGEBIED CODE'])

                school['nodal_area_code'] = int_or_none(row['NODAAL GEBIED CODE'])

                school['rpa_area_code'] = int_or_none(row['RPA-GEBIED CODE'])

                school['wgr_area_code'] = int_or_none(row['WGR-GEBIED CODE'])

                school['education_area_code'] = int_or_none(row['ONDERWIJSGEBIED CODE'])

                school['rmc_region_code'] = int_or_none(row['RMC-REGIO CODE'])

                for field, field_norm in school_fields.iteritems():
                    school[field_norm] = row[field]

                school['reference_year'] = reference_year
                school['ignore_id_fields'] = ['reference_year']

                yield school

    def parse_dropouts(self, response):
        """
        Parse: "02. Vsv in het voortgezet onderwijs per vo instelling"
        """

        for csv_url, reference_date in find_available_csvs(response).iteritems():
            reference_year = reference_date.year
            reference_date = str(reference_date)
            dropouts_per_school = {}
            for row in parse_csv_file(csv_url):
                # strip leading and trailing whitespace and remove
                # thousands separator ('.')
                for key in row.keys():
                    row[key] = row[key].strip().replace('.', '')

                brin = row['BRIN NUMMER']

                if brin not in dropouts_per_school:
                    dropouts_per_school[brin] = []

                dropouts = {
                    'year': int(row['JAAR']),
                    'education_structure': row['ONDERWIJSSTRUCTUUR EN LEERJAAR'],
                    'total_students': int(row['AANTAL DEELNEMERS']),
                    'total_dropouts': int(row['AANTAL VSV ERS']),
                    'dropouts_with_vmbo_diploma': int(row['AANTAL VSV ERS MET VMBO DIPLOMA']),
                    'dropouts_with_mbo1_dimploma': int(row['AANTAL VSV ERS MET MBO1 DIPLOMA']),
                    'dropouts_without_diploma': int(row['AANTAL VSV ERS ZONDER DIPLOMA'])
                }

                if row['PROFIEL'] == 'NVT':
                    dropouts['sector'] = None
                else:
                    dropouts['sector'] = row['PROFIEL']

                dropouts_per_school[brin].append(dropouts)

            for brin, dropouts in dropouts_per_school.iteritems():
                school = DuoVoSchool(
                    brin=brin,
                    dropouts_per_year_url=csv_url,
                    dropouts_per_year=dropouts,
                    dropouts_per_year_reference_date=reference_date,
                    reference_year=reference_year,
                )

                yield school

    def parse_students_prognosis(self, response):
        """
        Parse: "11. Prognose aantal leerlingen"
        """

        for csv_url, reference_date in find_available_csvs(response).iteritems():
            reference_year = reference_date.year
            reference_date = str(reference_date)
            students_prognosis_per_school = {}
            for row in parse_csv_file(csv_url):
                # strip leading and trailing whitespace and remove
                # thousands separator ('.')
                for key in row.keys():
                    row[key] = row[key].strip().replace('.', '')

                brin = row['BRIN NUMMER']

                if brin not in students_prognosis_per_school:
                    students_prognosis_per_school[brin] = []

                # ignoring actual data for now, only adding prognosis
                students_prognosis = []
                for k, v in row.iteritems():
                    row_words = k.split()
                    # k is of the form 'PROGNOSE LWOO PRO 2024'
                    if row_words[0] == 'PROGNOSE' or row_words[0]=='POGNOSE': # don't ask
                        if row_words[-1].isdigit():
                            students_prognosis.append({
                                'year' : int(row_words[-1]),
                                'structure' : '_'.join(row_words[1:-1]).lower(),
                                'students' : int(v),
                            })

                students_prognosis_per_school[brin].append(students_prognosis)

            for brin, students_prognosis in students_prognosis_per_school.iteritems():
                school = DuoVoSchool(
                    brin=brin,
                    students_prognosis_url=csv_url,
                    students_prognosis=students_prognosis,
                    students_prognosis_reference_date=reference_date,
                    reference_year=reference_year,
                )

                yield school

    def parse_vo_lo_collaboration(self, response):
        """
        Passend onderwijs > Adressen
        Parse "06. Adressen instellingen per samenwerkingsverband lichte ondersteuning, voortgezet onderwijs"
        """

        for csv_url, reference_date in find_available_csvs(response).iteritems():
            reference_year = reference_date.year
            reference_date = str(reference_date)
            vo_lo_collaboration_per_school = {}

            for row in parse_csv_file(csv_url):
                # strip leading and trailing whitespace.
                for key in row.keys():
                    value = (row[key] or '').strip()
                    row[key] = value or None
                    row[key.strip()] = value or None

                if row.has_key('BRINNUMMER'):
                    row['BRIN NUMMER'] = row['BRINNUMMER']

                brin = row['BRIN NUMMER']
                cid = row['ADMINISTRATIENUMMER'].strip()
                if '-' in cid:
                    int_parts = map(int_or_none, cid.split('-'))
                    if any([i == None for i in int_parts]):
                        cid = '-'.join(map(str, int_parts))
                collaboration = cid

                if brin not in vo_lo_collaboration_per_school:
                    vo_lo_collaboration_per_school[brin] = []

                vo_lo_collaboration_per_school[brin].append(collaboration)

            for brin, per_school in vo_lo_collaboration_per_school.iteritems():
                school = DuoVoSchool(
                    brin=brin,
                    reference_year=reference_year,
                    vo_lo_collaboration_reference_url=csv_url,
                    vo_lo_collaboration_reference_date=reference_date,
                    vo_lo_collaboration=per_school
                )
                yield school

    def parse_pao_collaboration(self, response):
        """
        Passend onderwijs > Adressen
        Parse "08. Adressen instellingen per samenwerkingsverband passend onderwijs, voortgezet onderwijs"
        """

        for csv_url, reference_date in find_available_csvs(response).iteritems():
            reference_year = reference_date.year
            reference_date = str(reference_date)
            pao_collaboration_per_school = {}

            for row in parse_csv_file(csv_url):
                # strip leading and trailing whitespace.
                for key in row.keys():
                    value = (row[key] or '').strip()
                    row[key] = value or None
                    row[key.strip()] = value or None

                if row.has_key('BRINNUMMER'):
                    row['BRIN NUMMER'] = row['BRINNUMMER']

                brin = row['BRIN NUMMER']
                collaboration = row['ADMINISTRATIENUMMER']

                if brin not in pao_collaboration_per_school:
                    pao_collaboration_per_school[brin] = []

                pao_collaboration_per_school[brin].append(collaboration)

            for brin, per_school in pao_collaboration_per_school.iteritems():
                school = DuoVoSchool(
                    brin=brin,
                    reference_year=reference_year,
                    pao_collaboration_reference_url=csv_url,
                    pao_collaboration_reference_date=reference_date,
                    pao_collaboration=per_school
                )
                yield school


class DuoVoBranchesSpider(BaseSpider):
    name = 'duo_vo_branches'

    def start_requests(self):
        return [
            Request('http://data.duo.nl/organisatie/open_onderwijsdata/'
                    'databestanden/vo/adressen/Adressen/vestigingen.asp',
                    self.parse_branches),
            Request('http://data.duo.nl/organisatie/open_onderwijsdata/'
                    'databestanden/vo/leerlingen/Leerlingen/vo_leerlingen2.asp',
                    self.parse_student_residences),
            Request('http://data.duo.nl/organisatie/open_onderwijsdata/'
                    'databestanden/vo/leerlingen/Leerlingen/vo_leerlingen1.asp',
                     self.parse_students_per_branch),
            Request('http://data.duo.nl/organisatie/open_onderwijsdata/'
                    'databestanden/vo/leerlingen/Leerlingen/vo_leerlingen6.asp',
                    self.student_graduations),
            Request('http://data.duo.nl/organisatie/open_onderwijsdata/'
                    'databestanden/vo/leerlingen/Leerlingen/vo_leerlingen7.asp',
                    self.student_exam_grades),
            Request('http://data.duo.nl/organisatie/open_onderwijsdata/'
                    'databestanden/vo/leerlingen/Leerlingen/vo_leerlingen8.asp',
                    self.vmbo_exam_grades_per_course),
            Request('http://data.duo.nl/organisatie/open_onderwijsdata/'
                    'databestanden/vo/leerlingen/Leerlingen/vo_leerlingen9.asp',
                    self.havo_exam_grades_per_course),
            Request('http://data.duo.nl/organisatie/open_onderwijsdata/'
                    'databestanden/vo/leerlingen/Leerlingen/vo_leerlingen10.asp',
                    self.vwo_exam_grades_per_course),
            Request('http://data.duo.nl/organisatie/open_onderwijsdata/'
                    'databestanden/vo/leerlingen/Leerlingen/vo_leerlingen3.asp',
                    self.parse_vavo_students),
            Request('http://data.duo.nl/organisatie/open_onderwijsdata/'
                    'databestanden/vo/leerlingen/Leerlingen/vo_leerlingen5.asp',
                    self.parse_students_by_finegrained_structure),
        ]

    def parse_branches(self, response):
        """
        Parse "02. Adressen alle vestigingen"
        """

        for csv_url, reference_date in find_available_csvs(response).iteritems():
            reference_year = reference_date.year
            reference_date = str(reference_date)
            for row in parse_csv_file(csv_url):
                school = DuoVoBranch()

                school['reference_year'] = reference_year
                school['ignore_id_fields'] = ['reference_year']
                school['name'] = row['VESTIGINGSNAAM'].strip()
                school['address'] = {
                    'street': '%s %s' % (row['STRAATNAAM'].strip(),
                                         row['HUISNUMMER-TOEVOEGING'].strip()),
                    'city': row['PLAATSNAAM'].strip(),
                    'zip_code': row['POSTCODE'].strip().replace(' ', '')
                }

                school['website'] = row['INTERNETADRES'].strip() or None

                school['denomination'] = row['DENOMINATIE'].strip() or None

                if row['ONDERWIJSSTRUCTUUR'].strip():
                    school['education_structures'] = row['ONDERWIJSSTRUCTUUR']\
                        .strip().split('/')
                else:
                    school['education_structures'] = None

                school['province'] = row['PROVINCIE'].strip() or None

                school['board_id'] = int_or_none(row['BEVOEGD GEZAG NUMMER'].strip())

                if row['BRIN NUMMER'].strip():
                    school['brin'] = row['BRIN NUMMER'].strip()

                if row['VESTIGINGSNUMMER'].strip():
                    school['branch_id'] = int(row['VESTIGINGSNUMMER']
                                              .strip()
                                              .replace(row['BRIN NUMMER'], ''))

                school['municipality'] = row['GEMEENTENAAM'].strip() or None

                school['municipality_code'] = int_or_none(row['GEMEENTENUMMER'].strip())

                school['phone'] = row['TELEFOONNUMMER'].strip() or None

                school['correspondence_address'] = {}
                if row['STRAATNAAM CORRESPONDENTIEADRES'].strip():
                    school['correspondence_address']['street'] = '%s %s'\
                        % (row['STRAATNAAM CORRESPONDENTIEADRES'].strip(),
                           row['HUISNUMMER-TOEVOEGING CORRESPONDENTIEADRES'].strip())
                else:
                    school['correspondence_address']['street'] = None

                if row['POSTCODE CORRESPONDENTIEADRES'].strip():
                    school['correspondence_address']['zip_code'] = row[
                        'POSTCODE CORRESPONDENTIEADRES'].strip().replace(' ', '')
                else:
                    school['correspondence_address']['zip_code'] = None

                school['correspondence_address']['city'] = row[
                        'PLAATSNAAM CORRESPONDENTIEADRES'].strip() or None

                school['nodal_area'] = row['NODAAL GEBIED NAAM'].strip() or None

                school['nodal_area_code'] = int_or_none(row['NODAAL GEBIED CODE']
                                                    .strip())

                school['rpa_area'] = row['RPA-GEBIED NAAM'].strip() or None

                school['rpa_area_code'] = int_or_none(row['RPA-GEBIED CODE'].strip())

                school['wgr_area'] = row['WGR-GEBIED NAAM'].strip() or None

                school['wgr_area_code'] = int_or_none(row['WGR-GEBIED CODE'].strip())

                school['corop_area'] = row['COROPGEBIED NAAM'].strip() or None

                school['corop_area_code'] = int_or_none(row['COROPGEBIED CODE'].strip())

                school['education_area'] = row['ONDERWIJSGEBIED NAAM'].strip() or None

                if row['ONDERWIJSGEBIED CODE'].strip():
                    school['education_area_code'] = int(row['ONDERWIJSGEBIED '
                                                            'CODE'].strip())
                else:
                    school['education_area_code'] = None

                school['rmc_region'] = row['RMC-REGIO NAAM'].strip() or None

                school['rmc_region_code'] = int_or_none(row['RMC-REGIO CODE'].strip())

                yield school

    def parse_students_per_branch(self, response):
        """
        Parse "01. Leerlingen per vestiging naar onderwijstype, lwoo
        indicatie, sector, afdeling, opleiding"
        """

        for csv_url, reference_date in find_available_csvs(response).iteritems():
            reference_year = reference_date.year
            reference_date = str(reference_date)
            student_educations = {}
            school_ids = {}

            for row in parse_csv_file(csv_url):
                school_id = '%s-%s' % (row['BRIN NUMMER'].strip(),
                                       row['VESTIGINGSNUMMER'].strip().zfill(2))

                school_ids[school_id] = {
                    'brin': row['BRIN NUMMER'].strip(),
                    'branch_id': int(row['VESTIGINGSNUMMER']
                                     .strip().replace(row['BRIN NUMMER'], ''))
                }

                if school_id not in student_educations:
                    student_educations[school_id] = []

                education_type = {}

                department = row['AFDELING'].strip()
                if department:
                    education_type['department'] = department
                    if education_type['department'].lower() == 'n.v.t.':
                        education_type['department'] = None
                else:
                    education_type['department'] = None

                if row['ELEMENTCODE'].strip():
                    education_type['elementcode'] = int(row['ELEMENTCODE']
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
                        education_type['vmbo_sector'] = None
                    else:
                        education_type['vmbo_sector'] = vmbo_sector
                else:
                    education_type['vmbo_sector'] = None

                naam = row['OPLEIDINGSNAAM'].strip()
                education_type['education_name'] = naam or None

                otype = row['ONDERWIJSTYPE VO EN LEER- OF VERBLIJFSJAAR'].strip()
                education_type['education_structure'] = otype or None

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
                school = DuoVoBranch(
                    brin=school_ids[school_id]['brin'],
                    branch_id=school_ids[school_id]['branch_id'],
                    reference_year=reference_year,
                    students_by_structure_url=csv_url,
                    students_by_structure_reference_date=reference_date,
                    students_by_structure=s_by_structure
                )

                yield school

    def parse_student_residences(self, response):
        """
        Parse "02. Leerlingen per vestiging naar postcode leerling en
        leerjaar"
        """

        for csv_url, reference_date in find_available_csvs(response).iteritems():
            reference_year = reference_date.year
            reference_date = str(reference_date)
            student_residences = {}
            school_ids = {}
            for row in parse_csv_file(csv_url):
                school_id = '%s-%s' % (row['BRIN NUMMER'].strip(),
                                       row['VESTIGINGSNUMMER'].strip().zfill(2))

                school_ids[school_id] = {
                    'brin': row['BRIN NUMMER'].strip(),
                    'branch_id': int(row['VESTIGINGSNUMMER'].strip()
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
                school = DuoVoBranch(
                    brin=school_ids[school_id]['brin'],
                    branch_id=school_ids[school_id]['branch_id'],
                    reference_year=reference_year,
                    student_residences_url=csv_url,
                    student_residences_reference_date=reference_date,
                    student_residences=residence
                )

                yield school

    def student_graduations(self, response):
        """
        Parse "06. Examenkandidaten en geslaagden"
        """

        for csv_url, reference_date in find_available_csvs(response).iteritems():
            reference_year = reference_date.year
            reference_date = str(reference_date)
            school_ids = {}
            graduations_school_year = {}
            for row in parse_csv_file(csv_url):
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
                        # Graduation info of a single school year
                        graduations_school_year[school_id][y_normal] = {
                            'year': y_normal,
                            'failed': 0,
                            'passed': 0,
                            'candidates': 0,
                            'per_department': []
                        }

                    # Total number of candidates (not always present for
                    # every year)
                    try:
                        candidates = row['EXAMENKANDIDATEN %s TOTAAL' % year]
                        if candidates:
                            candidates = int(candidates)
                        else:
                            continue
                    except KeyError:
                        candidates = 0
                    graduations_school_year[school_id][y_normal]['candidates'] += candidates

                    # Total number of successful graduations
                    try:
                        passed = int(row['GESLAAGDEN %s TOTAAL' % year])
                    except KeyError:
                        passed = 0
                    graduations_school_year[school_id][y_normal]['passed'] += passed

                    graduations_school_year[school_id][y_normal]['failed'] += (candidates - passed)

                    # Graduations for a singel department, by gender
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
                school = DuoVoBranch(
                    brin=school_ids[school_id]['brin'],
                    branch_id=school_ids[school_id]['branch_id'],
                    reference_year=reference_year,
                    graduations_reference_url=csv_url,
                    graduations_reference_date=reference_date,
                    graduations=[graduations[year] for year in graduations]
                )

                yield school

    def student_exam_grades(self, response):
        """
        Parse "07. Geslaagden, gezakten en gemiddelde examencijfers per instelling"
        """

        for csv_url, reference_date in find_available_csvs(response).iteritems():
            reference_year = reference_date.year
            reference_date = str(reference_date)
            school_ids = {}
            grades_per_school = {}
            for row in parse_csv_file(csv_url):
                # Remove newline chars and strip leading and trailing
                # whitespace.
                for key in row.keys():
                    c_key = key.replace('\n', '')
                    row[c_key] = row[key].strip()

                    if not row[c_key]:
                        del row[c_key]

                brin = row['BRIN NUMMER']
                branch_id = int(row['VESTIGINGSNUMMER'].replace(brin, ''))
                school_id = '%s-%s' % (brin, branch_id)

                school_ids[school_id] = {
                    'brin': brin,
                    'branch_id': branch_id
                }

                grades = {
                    'education_structure': row['ONDERWIJSTYPE VO']
                }

                if 'LEERWEG VMBO' in row:
                    grades['education_structure'] += '-%s' % row['LEERWEG VMBO']

                if 'VMBO SECTOR' in row:
                    grades['vmbo_sector'] = row['VMBO SECTOR']

                if 'AFDELING' in row:
                    grades['sector'] = row['AFDELING']

                if 'EXAMENKANDIDATEN' in row:
                    grades['candidates'] = int(row['EXAMENKANDIDATEN'])

                if 'GESLAAGDEN' in row:
                    grades['passed'] = int(row['GESLAAGDEN'])

                if 'GEZAKTEN' in row:
                    grades['failed'] = int(row['GEZAKTEN'])

                if 'GEMIDDELD CIJFER SCHOOLEXAMEN' in row:
                    grades['avg_grade_school_exam'] = float(row[
                        'GEMIDDELD CIJFER SCHOOLEXAMEN'].replace(',', '.'))

                if 'GEMIDDELD CIJFER CENTRAAL EXAMEN' in row:
                    grades['avg_grade_central_exam'] = float(row[
                        'GEMIDDELD CIJFER CENTRAAL EXAMEN'].replace(',', '.'))

                if 'GEMIDDELD CIJFER CIJFERLIJST' in row:
                    grades['avg_final_grade'] = float(row[
                        'GEMIDDELD CIJFER CIJFERLIJST'].replace(',', '.'))

                if school_id not in grades_per_school:
                    grades_per_school[school_id] = []

                grades_per_school[school_id].append(grades)

            for school_id, grades in grades_per_school.iteritems():
                school = DuoVoBranch(
                    brin=school_ids[school_id]['brin'],
                    branch_id=school_ids[school_id]['branch_id'],
                    reference_year=reference_year,
                    exam_grades_reference_url=csv_url,
                    exam_grades_reference_date=reference_date,
                    exam_grades=grades
                )

                yield school

    def vmbo_exam_grades_per_course(self, response):
        """
        Parse "08. Examenkandidaten vmbo en examencijfers per vak per instelling"
        """

        for csv_url, reference_date in find_available_csvs(response).iteritems():
            reference_year = reference_date.year
            reference_date = str(reference_date)
            school_ids = {}
            courses_per_school = {}
            for row in parse_csv_file(csv_url):
                # Remove newline chars and strip leading and trailing
                # whitespace.
                for key in row.keys():
                    c_key = key.replace('\n', '')
                    row[c_key] = row[key].strip()

                    if not row[c_key]:
                        del row[c_key]

                brin = row['BRIN NUMMER']
                branch_id = int(row['VESTIGINGSNUMMER'])
                school_id = '%s-%s' % (brin, branch_id)

                school_ids[school_id] = {
                    'brin': brin,
                    'branch_id': branch_id
                }

                grades = {
                    'education_structure': '%s-%s' % (row['ONDERWIJSTYPE VO'],
                                                      row['LEERWEG']),
                    'course_identifier': row['VAKCODE'],
                    'course_abbreviation': row['AFKORTING VAKNAAM'],
                    'course_name': row['VAKNAAM']

                }

                if 'SCHOOLEXAMEN BEOORDELING' in row:
                    grades['school_exam_rating'] = row['SCHOOLEXAMEN BEOORDELING']

                if 'TOTAAL AANTAL SCHOOLEXAMENS MET BEOORDELING' in row:
                    grades['amount_of_school_exams_with_rating'] = int(row[
                        'TOTAAL AANTAL SCHOOLEXAMENS MET BEOORDELING'])

                if 'AANTAL SCHOOLEXAMENS MET BEOORDELING MEETELLEND VOOR DIPLOMA' in row:
                    grades['amount_of_school_exams_with_rating_counting_'
                           'for_diploma'] = int(row['AANTAL SCHOOLEXAMENS MET '
                                                    'BEOORDELING MEETELLEND VOOR '
                                                    'DIPLOMA'])

                if 'TOTAAL AANTAL SCHOOLEXAMENS MET CIJFER' in row:
                    grades['amount_of_school_exams_with_grades'] = int(row[
                        'TOTAAL AANTAL SCHOOLEXAMENS MET CIJFER'])

                if 'GEM. CIJFER TOTAAL AANTAL SCHOOLEXAMENS' in row:
                    grades['avg_grade_school_exams'] = float(row[
                        'GEM. CIJFER TOTAAL AANTAL SCHOOLEXAMENS']
                        .replace(',', '.'))

                if 'AANTAL SCHOOLEXAMENS MET CIJFER MEETELLEND VOOR DIPLOMA' in row:
                    grades['amount_of_school_exams_with_grades_counting_'
                           'for_diploma'] = int(row['AANTAL SCHOOLEXAMENS MET '
                                                    'CIJFER MEETELLEND VOOR DIPLOMA'])

                if 'GEM. CIJFER SCHOOLEXAMENS MET CIJFER MEETELLEND VOOR DIPLOMA' in row:
                    grades['avg_grade_school_exams_counting_for_diploma'] = \
                        float(row['GEM. CIJFER SCHOOLEXAMENS MET CIJFER '
                                  'MEETELLEND VOOR DIPLOMA'].replace(',', '.'))

                if 'TOTAAL AANTAL CENTRALE EXAMENS' in row:
                    grades['amount_of_central_exams'] = int(row['TOTAAL AANTAL'
                                                                ' CENTRALE EXAMENS'])

                if 'GEM. CIJFER TOTAAL AANTAL CENTRALE EXAMENS' in row:
                    grades['avg_grade_central_exams'] = float(row[
                        'GEM. CIJFER TOTAAL AANTAL CENTRALE EXAMENS']
                        .replace(',', '.'))

                if 'AANTAL CENTRALE EXAMENS MEETELLEND VOOR DIPLOMA' in row:
                    grades['amount_of_central_exams_counting_for_diploma'] = \
                        int(row['AANTAL CENTRALE EXAMENS MEETELLEND VOOR DIPLOMA'])

                if 'GEM. CIJFER CENTRALE EXAMENS MET CIJFER MEETELLEND VOOR DIPLOMA' in row:
                    grades['avg_grade_central_exams_counting_for_diploma'] = \
                        float(row['GEM. CIJFER CENTRALE EXAMENS MET CIJFER '
                                  'MEETELLEND VOOR DIPLOMA'].replace(',', '.'))

                if 'GEM. CIJFER CIJFERLIJST' in row:
                    grades['average_grade_overall'] = float(row[
                        'GEM. CIJFER CIJFERLIJST'].replace(',', '.'))

                if school_id not in courses_per_school:
                    courses_per_school[school_id] = []

                courses_per_school[school_id].append(grades)

            for school_id, grades in courses_per_school.iteritems():
                school = DuoVoBranch(
                    brin=school_ids[school_id]['brin'],
                    branch_id=school_ids[school_id]['branch_id'],
                    reference_year=reference_year,
                    vmbo_exam_grades_reference_url=csv_url,
                    vmbo_exam_grades_reference_date=reference_date,
                    vmbo_exam_grades_per_course=grades
                )

                yield school

    def havo_exam_grades_per_course(self, response):
        """
        Parse "09. Examenkandidaten havo en examencijfers per vak per instelling"
        """

        for csv_url, reference_date in find_available_csvs(response).iteritems():
            reference_year = reference_date.year
            reference_date = str(reference_date)
            school_ids = {}
            courses_per_school = {}
            for row in parse_csv_file(csv_url):
                # Remove newline chars and strip leading and trailing
                # whitespace.
                for key in row.keys():
                    c_key = key.replace('\n', '')
                    row[c_key] = row[key].strip()

                    if not row[c_key]:
                        del row[c_key]

                brin = row['BRIN NUMMER']
                branch_id = int(row['VESTIGINGSNUMMER'])
                school_id = '%s-%s' % (brin, branch_id)

                school_ids[school_id] = {
                    'brin': brin,
                    'branch_id': branch_id
                }

                grades = {
                    'education_structure': row['ONDERWIJSTYPE VO'],
                    'course_identifier': row['VAKCODE'],
                    'course_abbreviation': row['AFKORTING VAKNAAM'],
                    'course_name': row['VAKNAAM']

                }

                if 'SCHOOLEXAMEN BEOORDELING' in row:
                    grades['school_exam_rating'] = row['SCHOOLEXAMEN BEOORDELING']

                if 'TOTAAL AANTAL SCHOOLEXAMENS MET BEOORDELING' in row:
                    grades['amount_of_school_exams_with_rating'] = int(row[
                        'TOTAAL AANTAL SCHOOLEXAMENS MET BEOORDELING'])

                if 'AANTAL SCHOOLEXAMENS MET BEOORDELING MEETELLEND VOOR DIPLOMA' in row:
                    grades['amount_of_school_exams_with_rating_counting_'
                           'for_diploma'] = int(row['AANTAL SCHOOLEXAMENS MET '
                                                    'BEOORDELING MEETELLEND VOOR '
                                                    'DIPLOMA'])

                if 'TOTAAL AANTAL SCHOOLEXAMENS MET CIJFER' in row:
                    grades['amount_of_school_exams_with_grades'] = int(row[
                        'TOTAAL AANTAL SCHOOLEXAMENS MET CIJFER'])

                if 'GEM. CIJFER TOTAAL AANTAL SCHOOLEXAMENS' in row:
                    grades['avg_grade_school_exams'] = float(row[
                        'GEM. CIJFER TOTAAL AANTAL SCHOOLEXAMENS']
                        .replace(',', '.'))

                if 'AANTAL SCHOOLEXAMENS MET CIJFER MEETELLEND VOOR DIPLOMA' in row:
                    grades['amount_of_school_exams_with_grades_counting_'
                           'for_diploma'] = int(row['AANTAL SCHOOLEXAMENS MET '
                                                    'CIJFER MEETELLEND VOOR DIPLOMA'])

                if 'GEM. CIJFER SCHOOLEXAMENS MET CIJFER MEETELLEND VOOR DIPLOMA' in row:
                    grades['avg_grade_school_exams_counting_for_diploma'] = \
                        float(row['GEM. CIJFER SCHOOLEXAMENS MET CIJFER '
                                  'MEETELLEND VOOR DIPLOMA'].replace(',', '.'))

                if 'TOTAAL AANTAL CENTRALE EXAMENS' in row:
                    grades['amount_of_central_exams'] = int(row['TOTAAL AANTAL'
                                                                ' CENTRALE EXAMENS'])

                if 'GEM. CIJFER TOTAAL AANTAL CENTRALE EXAMENS' in row:
                    grades['avg_grade_central_exams'] = float(row[
                        'GEM. CIJFER TOTAAL AANTAL CENTRALE EXAMENS']
                        .replace(',', '.'))

                if 'AANTAL CENTRALE EXAMENS MEETELLEND VOOR DIPLOMA' in row:
                    grades['amount_of_central_exams_counting_for_diploma'] = \
                        int(row['AANTAL CENTRALE EXAMENS MEETELLEND VOOR DIPLOMA'])

                if 'GEM. CIJFER CENTRALE EXAMENS MET CIJFER MEETELLEND VOOR DIPLOMA' in row:
                    grades['avg_grade_central_exams_counting_for_diploma'] = \
                        float(row['GEM. CIJFER CENTRALE EXAMENS MET CIJFER '
                                  'MEETELLEND VOOR DIPLOMA'].replace(',', '.'))

                if 'GEM. CIJFER CIJFERLIJST' in row:
                    grades['average_grade_overall'] = float(row[
                        'GEM. CIJFER CIJFERLIJST'].replace(',', '.'))

                if school_id not in courses_per_school:
                    courses_per_school[school_id] = []

                courses_per_school[school_id].append(grades)

            for school_id, grades in courses_per_school.iteritems():
                school = DuoVoBranch(
                    brin=school_ids[school_id]['brin'],
                    branch_id=school_ids[school_id]['branch_id'],
                    reference_year=reference_year,
                    havo_exam_grades_reference_url=csv_url,
                    havo_exam_grades_reference_date=reference_date,
                    havo_exam_grades_per_course=grades
                )

                yield school

    def vwo_exam_grades_per_course(self, response):
        """
        Parse "10. Examenkandidaten vwo en examencijfers per vak per instelling"
        """

        for csv_url, reference_date in find_available_csvs(response).iteritems():
            reference_year = reference_date.year
            reference_date = str(reference_date)
            school_ids = {}
            courses_per_school = {}
            for row in parse_csv_file(csv_url):
                # Remove newline chars and strip leading and trailing
                # whitespace.
                for key in row.keys():
                    c_key = key.replace('\n', '')
                    row[c_key] = row[key].strip()

                    if not row[c_key]:
                        del row[c_key]

                brin = row['BRIN NUMMER']
                branch_id = int(row['VESTIGINGSNUMMER'])
                school_id = '%s-%s' % (brin, branch_id)

                school_ids[school_id] = {
                    'brin': brin,
                    'branch_id': branch_id
                }

                grades = {
                    'education_structure': row['ONDERWIJSTYPE VO'],
                    'course_identifier': row['VAKCODE'],
                    'course_abbreviation': row['AFKORTING VAKNAAM'],
                    'course_name': row['VAKNAAM']
                }

                if 'SCHOOLEXAMEN BEOORDELING' in row:
                    grades['school_exam_rating'] = row['SCHOOLEXAMEN BEOORDELING']

                if 'TOTAAL AANTAL SCHOOLEXAMENS MET BEOORDELING' in row:
                    grades['amount_of_school_exams_with_rating'] = int(row[
                        'TOTAAL AANTAL SCHOOLEXAMENS MET BEOORDELING'])

                if 'AANTAL SCHOOLEXAMENS MET BEOORDELING MEETELLEND VOOR DIPLOMA' in row:
                    grades['amount_of_school_exams_with_rating_counting_'
                           'for_diploma'] = int(row['AANTAL SCHOOLEXAMENS MET '
                                                    'BEOORDELING MEETELLEND VOOR '
                                                    'DIPLOMA'])

                if 'TOTAAL AANTAL SCHOOLEXAMENS MET CIJFER' in row:
                    grades['amount_of_school_exams_with_grades'] = int(row[
                        'TOTAAL AANTAL SCHOOLEXAMENS MET CIJFER'])

                if 'GEM. CIJFER TOTAAL AANTAL SCHOOLEXAMENS' in row:
                    grades['avg_grade_school_exams'] = float(row[
                        'GEM. CIJFER TOTAAL AANTAL SCHOOLEXAMENS']
                        .replace(',', '.'))

                if 'AANTAL SCHOOLEXAMENS MET CIJFER MEETELLEND VOOR DIPLOMA' in row:
                    grades['amount_of_school_exams_with_grades_counting_'
                           'for_diploma'] = int(row['AANTAL SCHOOLEXAMENS MET '
                                                    'CIJFER MEETELLEND VOOR DIPLOMA'])

                if 'GEM. CIJFER SCHOOLEXAMENS MET CIJFER MEETELLEND VOOR DIPLOMA' in row:
                    grades['avg_grade_school_exams_counting_for_diploma'] = \
                        float(row['GEM. CIJFER SCHOOLEXAMENS MET CIJFER '
                                  'MEETELLEND VOOR DIPLOMA'].replace(',', '.'))

                if 'TOTAAL AANTAL CENTRALE EXAMENS' in row:
                    grades['amount_of_central_exams'] = int(row['TOTAAL AANTAL'
                                                                ' CENTRALE EXAMENS'])

                if 'GEM. CIJFER TOTAAL AANTAL CENTRALE EXAMENS' in row:
                    grades['avg_grade_central_exams'] = float(row[
                        'GEM. CIJFER TOTAAL AANTAL CENTRALE EXAMENS']
                        .replace(',', '.'))

                if 'AANTAL CENTRALE EXAMENS MEETELLEND VOOR DIPLOMA' in row:
                    grades['amount_of_central_exams_counting_for_diploma'] = \
                        int(row['AANTAL CENTRALE EXAMENS MEETELLEND VOOR DIPLOMA'])

                if 'GEM. CIJFER CENTRALE EXAMENS MET CIJFER MEETELLEND VOOR DIPLOMA' in row:
                    grades['avg_grade_central_exams_counting_for_diploma'] = \
                        float(row['GEM. CIJFER CENTRALE EXAMENS MET CIJFER '
                                  'MEETELLEND VOOR DIPLOMA'].replace(',', '.'))

                if 'GEM. CIJFER CIJFERLIJST' in row:
                    grades['average_grade_overall'] = float(row[
                        'GEM. CIJFER CIJFERLIJST'].replace(',', '.'))

                if school_id not in courses_per_school:
                    courses_per_school[school_id] = []

                courses_per_school[school_id].append(grades)

            for school_id, grades in courses_per_school.iteritems():
                school = DuoVoBranch(
                    brin=school_ids[school_id]['brin'],
                    branch_id=school_ids[school_id]['branch_id'],
                    reference_year=reference_year,
                    vwo_exam_grades_reference_url=csv_url,
                    vwo_exam_grades_reference_date=reference_date,
                    vwo_exam_grades_per_course=grades
                )
                yield school

    def parse_vavo_students(self, response):
        """
        Voortgezet onderwijs > Leerlingen
        Parse "Leerlingen per vestiging en bevoegd gezag (vavo apart)"
        """

        for csv_url, reference_date in find_available_csvs(response).iteritems():
            reference_year = reference_date.year
            reference_date = str(reference_date)
            school_ids = {}
            vavo_students_per_school = {}

            for row in parse_csv_file(csv_url):

                brin = row['BRIN NUMMER'].strip()
                branch_id = int(row['VESTIGINGSNUMMER'].strip()[-2:] or 0)
                school_id = '%s-%s' % (brin, branch_id)

                school_ids[school_id] = {
                    'brin': brin,
                    'branch_id': branch_id
                }

                vavo_students = {
                    'non_vavo' : int(row['AANTAL LEERLINGEN'] or 0),
                    'vavo' : int(row['AANTAL VO LEERLINGEN UITBESTEED AAN VAVO'] or 0),
                }

                if school_id not in vavo_students_per_school:
                    vavo_students_per_school[school_id] = []
                vavo_students_per_school[school_id].append(vavo_students)

            for school_id, per_school in vavo_students_per_school.iteritems():
                school = DuoVoBranch(
                    brin=school_ids[school_id]['brin'],
                    branch_id=school_ids[school_id]['branch_id'],
                    reference_year=reference_year,
                    vavo_students_reference_url=csv_url,
                    vavo_students_reference_date=reference_date,
                    vavo_students=per_school
                )
                yield school

    def parse_students_by_finegrained_structure(self, response):
        """
        Voortgezet onderwijs > Leerlingen
        Parse "05. Leerlingen per samenwerkingsverband en onderwijstype"
        """

        for csv_url, reference_date in find_available_csvs(response).iteritems():
            reference_year = reference_date.year
            reference_date = str(reference_date)
            school_ids = {}
            counts_per_school = {}

            for row in parse_csv_file(csv_url):

                brin = row['BRIN NUMMER'].strip()
                branch_id = int(row['VESTIGINGSNUMMER'].strip()[-2:] or 0)
                school_id = '%s-%s' % (brin, branch_id)

                school_ids[school_id] = {
                    'brin': brin,
                    'branch_id': branch_id
                }

                if school_id not in counts_per_school:
                    counts_per_school[school_id] = []

                # Don't make special fiends, just use all of 'em
                fields = [
                    'Brugjaar 1-2',
                    'Engelse Stroom',
                    'HAVO lj 4-5',
                    'HAVO uitbest. aan VAVO',
                    'HAVO/VWO lj 3',
                    'Int. Baccelaureaat',
                    'Praktijkonderwijs alle vj',
                    'VMBO BL lj 3-4',
                    'VMBO GL lj 3-4',
                    'VMBO KL lj 3-4',
                    'VMBO TL lj 3-4',
                    'VMBO uitbest. aan VAVO',
                    'VMBO-MBO2 lj 3-6',
                    'VWO lj 4-6',
                    'VWO uitbest. aan VAVO',
                ]
                for field, count in row.items():
                    if field.strip() in fields and count:
                        counts = {'type': field.strip(), 'count': int(count)}
                        counts_per_school[school_id].append(counts)

            for school_id, per_school in counts_per_school.iteritems():
                school = DuoVoBranch(
                    brin=school_ids[school_id]['brin'],
                    branch_id=school_ids[school_id]['branch_id'],
                    reference_year=reference_year,
                    students_by_finegrained_structure_reference_url=csv_url,
                    students_by_finegrained_structure_reference_date=reference_date,
                    students_by_finegrained_structure=per_school
                )
                yield school

class DuoPoBoards(BaseSpider):
    name = 'duo_po_boards'

    def start_requests(self):
        return [
            Request('http://data.duo.nl/organisatie/open_onderwijsdata/'
                    'databestanden/po/adressen/Adressen/po_adressen05.asp',
                    self.parse_po_boards),
            Request('http://data.duo.nl/organisatie/open_onderwijsdata/'
                    'databestanden/po/Financien/Jaarrekeninggegevens/'
                    'Kengetallen.asp', self.parse_po_financial_key_indicators),
            Request('http://data.duo.nl/organisatie/open_onderwijsdata/'
                    'databestanden/po/Leerlingen/Leerlingen/po_leerlingen7.asp',
                    self.parse_po_education_type)
        ]

    def parse_po_boards(self, response):
        """
        Primair onderwijs > Adressen
        Parse "05. Bevoegde gezagen basisonderwijs"
        """

        for csv_url, reference_date in find_available_csvs(response).iteritems():
            reference_year = reference_date.year
            reference_date = str(reference_date)
            for row in parse_csv_file(csv_url):
                # strip leading and trailing whitespace.
                for key in row.keys():
                    row[key] = row[key].strip()

                board = DuoPoBoard()
                board['board_id'] = int(row['BEVOEGD GEZAG NUMMER'])
                board['name'] = row['BEVOEGD GEZAG NAAM']
                board['address'] = {
                    'street': '%s %s' % (row['STRAATNAAM'],
                                         row['HUISNUMMER-TOEVOEGING']),
                    'zip_code': row['POSTCODE'].replace(' ', ''),
                    'city': row['PLAATSNAAM']
                }

                board['correspondence_address'] = {}
                if row['STRAATNAAM CORRESPONDENTIEADRES']:
                    board['correspondence_address']['street'] = '%s %s'\
                        % (row['STRAATNAAM CORRESPONDENTIEADRES'],
                           row['HUISNUMMER-TOEVOEGING CORRESPONDENTIEADRES'])
                else:
                    board['correspondence_address']['street'] = None

                if row['POSTCODE CORRESPONDENTIEADRES']:
                    board['correspondence_address']['zip_code'] = row[
                        'POSTCODE CORRESPONDENTIEADRES'].replace(' ', '')
                else:
                    board['correspondence_address']['zip_code'] = None

                board['correspondence_address']['city'] = row[
                        'PLAATSNAAM CORRESPONDENTIEADRES'] or None

                board['municipality'] = row['GEMEENTENAAM'] or None

                board['municipality_code'] = int_or_none(row['GEMEENTENUMMER'])

                board['phone'] = row['TELEFOONNUMMER'] or None

                board['website'] = row['INTERNETADRES'] or None

                board['denomination'] = row['DENOMINATIE'] or None

                board['administrative_office_id'] = \
                        int_or_none(row['ADMINISTRATIEKANTOORNUMMER'])

                board['reference_year'] = reference_year
                board['ignore_id_fields'] = ['reference_year']
                yield board

    def parse_po_financial_key_indicators(self, response):
        """
        Primair onderwijs > Financien > Jaarrekeninggegevens
        Parse "15. Kengetallen"
        """

        indicators_mapping = {
            'LIQUIDITEIT (CURRENT RATIO)': 'liquidity_current_ratio',
            'RENTABILITEIT': 'profitability',
            'SOLVABILITEIT 1': 'solvency_1',
            'SOLVABILITEIT 2': 'solvency_2',
            'ALGEMENE RESERVE / TOTALE BATEN': 'general_reserve_div_total_income',
            'BELEGGINGEN (T.O.V. EV)': 'investments_relative_to_equity',
            #'CONTRACTACTIVITEITEN / RIJKSBIJDRAGE': 'contract_activities_div_gov_funding',
            #'CONTRACTACTIVITEITEN / TOTALE BATEN': 'contractactivities_div_total_profits',
            'EIGEN VERMOGEN / TOTALE BATEN': 'equity_div_total_profits',
            #'INVESTERING HUISVESTING / TOTALE BATEN': 'housing_investment_div_total_profits',
            'INVESTERINGEN (INVENT.+APP.) / TOTALE BATEN': 'investments_div_total_profits',
            'KAPITALISATIEFACTOR': 'capitalization_ratio',
            'LIQUIDITEIT (QUICK RATIO)': 'liquidity_quick_ratio',
            'OV. OVERHEIDSBIJDRAGEN / TOT. BATEN': 'other_gov_funding_div_total_profits',
            'PERSONEEL / RIJKSBIJDRAGEN': 'staff_costs_div_gov_funding',
            'PERSONELE LASTEN / TOTALE LASTEN': 'staff_expenses_div_total_expenses',
            'RIJKSBIJDRAGEN / TOTALE BATEN': 'gov_funding_div_total_profits',
            'VOORZIENINGEN /TOTALE BATEN': 'facilities_div_total_profits',
            #'WEERSTANDSVERMOGEN (-/- MVA)': '',
            #'WEERSTANDSVERMOGEN VO TOTALE BN.': '',
            'WERKKAPITAAL / TOTALE BATEN': 'operating_capital_div_total_profits',
            'HUISVESTINGSLASTEN / TOTALE LASTEN': 'housing_expenses_div_total_expenses',
            'WERKKAPITAAL': 'operating_capital',
        }

        for csv_url, reference_date in find_available_csvs(response).iteritems():
            reference_year = reference_date.year
            reference_date = str(reference_date)
            indicators_per_board = {}
            for row in parse_csv_file(csv_url):
                # Strip leading and trailing whitespace from field names and values.
                for key in row.keys():
                    row[key.strip()] = row[key].strip()

                board_id = int(row['BEVOEGD GEZAG NUMMER'])
                if board_id not in indicators_per_board:
                    indicators_per_board[board_id] = []

                indicators = {}
                indicators['year'] = int(row['JAAR'])
                indicators['group'] = row['GROEPERING']

                for ind, ind_norm in indicators_mapping.iteritems():
                    # Some fields have no value, just an empty string ''.
                    # Set those to 0.
                    if row[ind] == '':
                        row[ind] = '0'
                    indicators[ind_norm] = float(row[ind].replace('.', '')
                                                         .replace(',', '.'))

                indicators_per_board[board_id].append(indicators)

            for board_id, indicators in indicators_per_board.iteritems():
                board = DuoPoBoard(
                    board_id=board_id,
                    reference_year=reference_year,
                    financial_key_indicators_per_year_url=csv_url,
                    financial_key_indicators_per_year_reference_date=reference_date,
                    financial_key_indicators_per_year=indicators
                )
                yield board

    def parse_po_education_type(self, response):
        """
        Primair onderwijs > Leerlingen
        Parse "07. Leerlingen primair onderwijs per bevoegd gezag naar denominatie en onderwijssoort"
        """

        possible_edu_types = ['BAO', 'SBAO', 'SO', 'VSO']

        for csv_url, reference_date in find_available_csvs(response).iteritems():
            reference_year = reference_date.year
            reference_date = str(reference_date)
            students_per_edu_type = {}
            for row in parse_csv_file(csv_url):
                # Strip leading and trailing whitespace from field names and values.
                for key in row.keys():
                    if row[key]:
                        row[key.strip()] = row[key].strip()
                    else:
                        row[key.strip()] = '0'

                board_id = int(row['BEVOEGD GEZAG NUMMER'])
                if board_id not in students_per_edu_type:
                    students_per_edu_type[board_id] = []

                for edu_type in possible_edu_types:
                    if edu_type in row:
                        if row[edu_type] == '':
                            continue

                        if row[edu_type] == 0:
                            continue

                        students_per_edu_type[board_id].append({
                            'denomination': row['DENOMINATIE'],
                            'edu_type': edu_type,
                            'students': int(row[edu_type].replace('.', ''))
                        })

            for board_id, e_types in students_per_edu_type.iteritems():
                board = DuoPoBoard(
                    board_id=board_id,
                    reference_year=reference_year,
                    students_per_edu_type_reference_url=csv_url,
                    students_per_edu_type_reference_date=reference_date,
                    students_per_edu_type=e_types
                )
                yield board


class DuoPoSchools(BaseSpider):
    name = 'duo_po_schools'

    def start_requests(self):
        return [
            # Request('http://data.duo.nl/organisatie/open_onderwijsdata/'
            #         'databestanden/po/adressen/Adressen/hoofdvestigingen.asp',
            #         self.parse_po_schools),
            # Request('http://data.duo.nl/organisatie/open_onderwijsdata/'
            #         'databestanden/po/Leerlingen/Leerlingen/po_leerlingen4.asp',
            #         self.parse_spo_students_per_cluster),
            # Request('http://data.duo.nl/organisatie/open_onderwijsdata/'
            #         'databestanden/passendow/Adressen/Adressen/passend_po_2.asp',
            #         self.parse_po_lo_collaboration),
            Request('http://data.duo.nl/organisatie/open_onderwijsdata/'
                    'databestanden/passendow/Adressen/Adressen/passend_po_4.asp',
                    self.parse_pao_collaboration),
        ]

    def parse_po_schools(self, response):
        """
        Primair onderwijs > Adressen
        Parse: "01. Hoofdvestigingen basisonderwijs"
        """

        # Fields that do not need additonal processing
        school_fields = {
            'BRIN NUMMER': 'brin',
            'PROVINCIE': 'province',
            'INSTELLINGSNAAM': 'name',
            'GEMEENTENAAM': 'municipality',
            'DENOMINATIE': 'denomination',
            'INTERNETADRES': 'website',
            'TELEFOONNUMMER': 'phone',
            'ONDERWIJSGEBIED NAAM': 'education_area',
            'NODAAL GEBIED NAAM': 'nodal_area',
            'RPA-GEBIED NAAM': 'rpa_area',
            'WGR-GEBIED NAAM': 'wgr_area',
            'COROPGEBIED NAAM': 'corop_area',
            'RMC-REGIO NAAM': 'rmc_region'
        }

        for csv_url, reference_date in find_available_csvs(response).iteritems():
            reference_year = reference_date.year
            reference_date = str(reference_date)
            for row in parse_csv_file(csv_url):
                # strip leading and trailing whitespace.
                for key in row.keys():
                    value = row[key].strip()
                    row[key] = value or None

                school = DuoPoSchool()
                school['board_id'] = int(row['BEVOEGD GEZAG NUMMER'])
                school['address'] = {
                    'street': '%s %s' % (row['STRAATNAAM'],
                                         row['HUISNUMMER-TOEVOEGING']),
                    'city': row['PLAATSNAAM'],
                    'zip_code': row['POSTCODE'].replace(' ', '')
                }

                school['correspondence_address'] = {
                    'street': '%s %s' % (row['STRAATNAAM CORRESPONDENTIEADRES'],
                                         row['HUISNUMMER-TOEVOEGING '
                                             'CORRESPONDENTIEADRES']),
                    'city': row['PLAATSNAAM CORRESPONDENTIEADRES'],
                    'zip_code': row['POSTCODE CORRESPONDENTIEADRES']
                }

                school['municipality_code'] = int(row['GEMEENTENUMMER'])

                if row['COROPGEBIED CODE']:
                    school['corop_area_code'] = int(row['COROPGEBIED CODE'])

                school['nodal_area_code'] = int_or_none(row['NODAAL GEBIED CODE'])

                school['rpa_area_code'] = int_or_none(row['RPA-GEBIED CODE'])

                school['wgr_area_code'] = int_or_none(row['WGR-GEBIED CODE'])

                school['education_area_code'] = int_or_none(row['ONDERWIJSGEBIED CODE'])

                school['rmc_region_code'] = int_or_none(row['RMC-REGIO CODE'])

                for field, field_norm in school_fields.iteritems():
                    school[field_norm] = row[field]

                school['reference_year'] = reference_year
                school['ignore_id_fields'] = ['reference_year']

                yield school

    def parse_spo_students_per_cluster(self, response):
        """
        Primair onderwijs > Leerlingen
        Parse "04. Leerlingen speciaal onderwijs naar cluster"
        """

        for csv_url, reference_date in find_available_csvs(response).iteritems():
            reference_year = reference_date.year
            reference_date = str(reference_date)
            spo_students_per_cluster_per_school = {}


            for row in parse_csv_file(csv_url):
                spo_students_per_cluster_per_school[row['BRIN NUMMER']] = {
                    'cluster_1': int(row['CLUSTER 1']),
                    'cluster_2': int(row['CLUSTER 2']),
                    'cluster_3': int(row['CLUSTER 3']),
                    'cluster_4': int(row['CLUSTER 4']),
                }

            for brin, spo_students_per_cluster in spo_students_per_cluster_per_school.iteritems():
                school = DuoPoSchool(
                    brin=brin,
                    reference_year=reference_year,
                    spo_students_per_cluster_reference_url=csv_url,
                    spo_students_per_cluster_reference_date=reference_date,
                    spo_students_per_cluster=spo_students_per_cluster
                )
                yield school

    def parse_po_lo_collaboration(self, response):
        """
        Passend onderwijs > Adressen
        Parse "02. Adressen instellingen per samenwerkingsverband lichte ondersteuning, primair onderwijs"
        """

        for csv_url, reference_date in find_available_csvs(response).iteritems():
            reference_year = reference_date.year
            reference_date = str(reference_date)
            po_lo_collaboration_per_school = {}

            for row in parse_csv_file(csv_url):
                # strip leading and trailing whitespace.
                for key in row.keys():
                    value = (row[key] or '').strip()
                    row[key] = value or None
                    row[key.strip()] = value or None

                if row.has_key('BRINNUMMER'):
                    row['BRIN NUMMER'] = row['BRINNUMMER']

                brin = row['BRIN NUMMER']
                collaboration = row['ADMINISTRATIENUMMER']

                if brin not in po_lo_collaboration_per_school:
                    po_lo_collaboration_per_school[brin] = []

                po_lo_collaboration_per_school[brin].append(collaboration)

            for brin, per_school in po_lo_collaboration_per_school.iteritems():
                school = DuoPoSchool(
                    brin=brin,
                    reference_year=reference_year,
                    po_lo_collaboration_reference_url=csv_url,
                    po_lo_collaboration_reference_date=reference_date,
                    po_lo_collaboration=per_school
                )
                yield school

    def parse_pao_collaboration(self, response):
        """
        Passend onderwijs > Adressen
        Parse "04. Adressen instellingen per samenwerkingsverband passend onderwijs, primair onderwijs"
        """

        for csv_url, reference_date in find_available_csvs(response).iteritems():
            reference_year = reference_date.year
            reference_date = str(reference_date)
            pao_collaboration_per_school = {}

            for row in parse_csv_file(csv_url):
                # strip leading and trailing whitespace.
                for key in row.keys():
                    value = (row[key] or '').strip()
                    row[key] = value or None
                    row[key.strip()] = value or None

                if row.has_key('BRINNUMMER'):
                    row['BRIN NUMMER'] = row['BRINNUMMER']

                brin = row['BRIN NUMMER']
                collaboration = row['ADMINISTRATIENUMMER']

                if brin not in pao_collaboration_per_school:
                    pao_collaboration_per_school[brin] = []

                pao_collaboration_per_school[brin].append(collaboration)

            for brin, per_school in pao_collaboration_per_school.iteritems():
                school = DuoPoSchool(
                    brin=brin,
                    reference_year=reference_year,
                    pao_collaboration_reference_url=csv_url,
                    pao_collaboration_reference_date=reference_date,
                    pao_collaboration=per_school
                )
                yield school

class DuoPoBranchesSpider(BaseSpider):
    name = 'duo_po_branches'

    def start_requests(self):
        return [
            # Request('http://data.duo.nl/organisatie/open_onderwijsdata/'
            #         'databestanden/po/adressen/Adressen/vest_bo.asp',
            #         self.parse_po_branches),
            # Request('http://data.duo.nl/organisatie/open_onderwijsdata/'
            #         'databestanden/po/Leerlingen/Leerlingen/po_leerlingen1.asp',
            #         self.parse_po_student_weight),
            # Request('http://data.duo.nl/organisatie/open_onderwijsdata/'
            #         'databestanden/po/Leerlingen/Leerlingen/po_leerlingen3.asp',
            #         self.parse_po_student_age),
            # Request('http://data.duo.nl/organisatie/open_onderwijsdata/'
            #         'databestanden/po/Leerlingen/Leerlingen/po_leerlingen9.asp',
            #         self.parse_po_born_outside_nl),
            # Request('http://data.duo.nl/organisatie/open_onderwijsdata/'
            #         'databestanden/po/Leerlingen/Leerlingen/po_leerlingen11.asp',
            #         self.parse_po_pupil_zipcode_by_age),
            # Request('http://data.duo.nl/organisatie/open_onderwijsdata/'
            #         'databestanden/po/Leerlingen/Leerlingen/leerjaar.asp',
            #         self.parse_po_student_year),
            # Request('http://data.duo.nl/organisatie/open_onderwijsdata/'
            #         'databestanden/po/Leerlingen/Leerlingen/po_leerlingen5.asp',
            #         self.parse_spo_students_by_birthyear),
            # Request('http://data.duo.nl/organisatie/open_onderwijsdata/'
            #         'databestanden/po/Leerlingen/Leerlingen/po_leerlingen6.asp',
            #         self.parse_spo_students_by_edu_type),
            Request('http://data.duo.nl/organisatie/open_onderwijsdata/'
                    'databestanden/po/Leerlingen/Leerlingen/Schooladvies.asp',
                    self.parse_spo_students_by_advice),
        ]

    def parse_po_branches(self, response):
        """
        Primair onderwijs > Adressen
        Parse "03. Alle vestigingen basisonderwijs"
        """

        for csv_url, reference_date in find_available_csvs(response).iteritems():
            reference_year = reference_date.year
            reference_date = str(reference_date)
            for row in parse_csv_file(csv_url):
                school = DuoPoBranch()

                # Correct this field name which has a trailing space.
                if row.has_key('VESTIGINGSNAAM '):
                    row['VESTIGINGSNAAM'] = row['VESTIGINGSNAAM ']

                school['reference_year'] = reference_year
                school['ignore_id_fields'] = ['reference_year']
                school['name'] = row['VESTIGINGSNAAM'].strip()
                school['address'] = {
                    'street': '%s %s' % (row['STRAATNAAM'].strip(),
                                         row['HUISNUMMER-TOEVOEGING'].strip()),
                    'city': row['PLAATSNAAM'].strip(),
                    'zip_code': row['POSTCODE'].strip().replace(' ', '')
                }

                school['website'] = row['INTERNETADRES'].strip() or None

                school['denomination'] = row['DENOMINATIE'].strip() or None

                school['province'] = row['PROVINCIE'].strip() or None

                school['board_id'] = int_or_none(row['BEVOEGD GEZAG NUMMER'].strip())

                if row['BRIN NUMMER'].strip():
                    school['brin'] = row['BRIN NUMMER'].strip()

                if row['VESTIGINGSNUMMER'].strip():
                    school['branch_id'] = int(row['VESTIGINGSNUMMER']
                                              .strip()
                                              .replace(row['BRIN NUMMER'], ''))

                school['municipality'] = row['GEMEENTENAAM'].strip() or None

                school['municipality_code'] = int_or_none(row['GEMEENTENUMMER'].strip())

                school['phone'] = row['TELEFOONNUMMER'].strip() or None

                school['correspondence_address'] = {}
                if row['STRAATNAAM CORRESPONDENTIEADRES'].strip():
                    school['correspondence_address']['street'] = '%s %s'\
                        % (row['STRAATNAAM CORRESPONDENTIEADRES'].strip(),
                           row['HUISNUMMER-TOEVOEGING CORRESPONDENTIEADRES'].strip())
                else:
                    school['correspondence_address']['street'] = None

                if row['POSTCODE CORRESPONDENTIEADRES'].strip():
                    school['correspondence_address']['zip_code'] = row[
                        'POSTCODE CORRESPONDENTIEADRES'].strip().replace(' ', '')
                else:
                    school['correspondence_address']['zip_code'] = None

                school['correspondence_address']['city'] = row[
                        'PLAATSNAAM CORRESPONDENTIEADRES'].strip() or None

                school['nodal_area'] = row['NODAAL GEBIED NAAM'].strip() or None

                if row['NODAAL GEBIED CODE'].strip():
                    school['nodal_area_code'] = int(row['NODAAL GEBIED CODE']
                                                    .strip())
                else:
                    school['nodal_area_code'] = None

                school['rpa_area'] = row['RPA-GEBIED NAAM'].strip() or None

                school['rpa_area_code'] = int_or_none(row['RPA-GEBIED CODE'].strip())

                school['wgr_area'] = row['WGR-GEBIED NAAM'].strip() or None

                school['wgr_area_code'] = int_or_none(row['WGR-GEBIED CODE'].strip())

                school['corop_area'] = row['COROPGEBIED NAAM'].strip() or None

                school['corop_area_code'] = int_or_none(row['COROPGEBIED CODE'].strip())

                school['education_area'] = row['ONDERWIJSGEBIED NAAM'].strip() or None

                if row['ONDERWIJSGEBIED CODE'].strip():
                    school['education_area_code'] = int(row['ONDERWIJSGEBIED '
                                                            'CODE'].strip())
                else:
                    school['education_area_code'] = None

                school['rmc_region'] = row['RMC-REGIO NAAM'].strip() or None

                school['rmc_region_code'] = int_or_none(row['RMC-REGIO CODE'].strip())

                yield school

    def parse_po_student_weight(self, response):
        """
        Primair onderwijs > Leerlingen
        Parse "01. Leerlingen basisonderwijs naar leerlinggewicht en per
                   vestiging het schoolgewicht en impulsgebied"
        """

        for csv_url, reference_date in find_available_csvs(response).iteritems():
            reference_year = reference_date.year
            reference_date = str(reference_date)
            school_ids = {}
            weights_per_school = {}

            for row in parse_csv_file(csv_url):
                # Datasets 2011 and 2012 suddenly changed these field names.
                if row.has_key('BRINNUMMER'):
                    row['BRIN NUMMER'] = row['BRINNUMMER']
                if row.has_key('GEWICHT0.00'):
                    row['GEWICHT 0'] = row['GEWICHT0.00']
                if row.has_key('GEWICHT0.30'):
                    row['GEWICHT 0.3'] = row['GEWICHT0.30']
                if row.has_key('GEWICHT1.20'):
                    row['GEWICHT 1.2'] = row['GEWICHT1.20']

                brin = row['BRIN NUMMER'].strip()
                # Bypasses error coming from the 2011 dataset which contains and
                # empty row.
                if row['VESTIGINGSNUMMER'].strip():
                    branch_id = int(row['VESTIGINGSNUMMER'])
                school_id = '%s-%s' % (brin, branch_id)

                school_ids[school_id] = {
                    'brin': brin,
                    'branch_id': branch_id
                }

                weights = {}
            
                weights['student_weight_0.0'] = int_or_none(row['GEWICHT 0'].strip())        

                weights['student_weight_0.3'] = int_or_none(row['GEWICHT 0.3'].strip())

                weights['student_weight_1.2'] = int_or_none(row['GEWICHT 1.2'].strip())

                weights['school_weight'] = int_or_none(row['SCHOOLGEWICHT'].strip())

                # The 2008 dataset doesn't contain the IMPULSGEBIED field.
                if row.has_key('IMPULSGEBIED'):
                    if row['IMPULSGEBIED'].strip():
                        weights['impulse_area'] = bool(int(row['IMPULSGEBIED'].strip()))
                    else:
                        weights['impulse_area'] = None

                if school_id not in weights_per_school:
                    weights_per_school[school_id] = []

                weights_per_school[school_id].append(weights)

            for school_id, w_per_school in weights_per_school.iteritems():
                school = DuoPoBranch(
                    brin=school_ids[school_id]['brin'],
                    branch_id=school_ids[school_id]['branch_id'],
                    reference_year=reference_year,
                    weights_per_school_reference_url=csv_url,
                    weights_per_school_reference_date=reference_date,
                    weights_per_school=w_per_school
                )
                yield school

    def parse_po_student_age(self, response):
        """
        Primair onderwijs > Leerlingen
        Parse "02. Leerlingen basisonderwijs naar leeftijd"
        """

        for csv_url, reference_date in find_available_csvs(response).iteritems():
            reference_year = reference_date.year
            reference_date = str(reference_date)
            school_ids = {}
            ages_per_branch_by_student_weight = {}

            for row in parse_csv_file(csv_url):
                # Datasets 2011 and 2012 suddenly changed these field names.
                if row.has_key('BRINNUMMER'):
                    row['BRIN NUMMER'] = row['BRINNUMMER']
                if row.has_key('GEMEENTE NUMMER'):
                    row['GEMEENTENUMMER'] = row['GEMEENTE NUMMER']
                if row.has_key('VESTIGINGS NUMMER'):
                    row['VESTIGINGSNUMMER'] = row['VESTIGINGS NUMMER']

                brin = row['BRIN NUMMER'].strip()
                branch_id = int(row['VESTIGINGSNUMMER'])
                school_id = '%s-%s' % (brin, branch_id)

                school_ids[school_id] = {
                    'brin': brin,
                    'branch_id': branch_id
                }

                # The 2012 dataset had fields like 'LEEFTIJD 4 JAAR' instead of
                # '4 JAAR'. This fixes the problem.
                for key in row.keys():
                    key_norm = key.replace('LEEFTIJD ', '')
                    row[key_norm] = row[key]

                # Remove leading/trailing spaces from field names.
                for key in row.keys():
                    row[key.strip()] = row[key]

                ages = {}
                possible_ages = '3 4 5 6 7 8 9 10 11 12 13 14'.split()
                for age in possible_ages:
                    if row.has_key('%s JAAR' % age):
                        if row['%s JAAR' % age].strip():
                            ages['age_%s' % age] = int(row['%s JAAR' % age])
                        else:
                            ages['age_%s' % age] = 0
                    # The 2011 dataset uses other field names.
                    elif row.has_key('LEEFTIJD.%s' % age):
                        if row['LEEFTIJD.%s' % age].strip():
                            ages['age_%s' % age] = int(row['LEEFTIJD.%s' % age])
                        else:
                            ages['age_%s' % age] = 0

                if school_id not in ages_per_branch_by_student_weight:
                    ages_per_branch_by_student_weight[school_id] = {}

                if row['GEWICHT'].strip():
                    weight = 'student_weight_%.1f' % float(row['GEWICHT'].strip().replace(',', '.'))
                else:
                    weight = None

                ages_per_branch_by_student_weight[school_id][weight] = ages

            for school_id, a_per_school in ages_per_branch_by_student_weight.iteritems():
                school = DuoPoBranch(
                    brin=school_ids[school_id]['brin'],
                    branch_id=school_ids[school_id]['branch_id'],
                    reference_year=reference_year,
                    ages_per_branch_by_student_weight_reference_url=csv_url,
                    ages_per_branch_by_student_weight_reference_date=reference_date,
                    ages_per_branch_by_student_weight=a_per_school
                )
                yield school

    def parse_po_born_outside_nl(self, response):
        """
        Primair onderwijs > Leerlingen
        Parse "09. Leerlingen basisonderwijs met een niet-Nederlandse achtergrond naar geboorteland"
        """

        for csv_url, reference_date in find_available_csvs(response).iteritems():
            reference_year = reference_date.year
            reference_date = str(reference_date)
            school_ids = {}
            students_by_origin = {}

            for row in parse_csv_file(csv_url):
                brin = row['BRIN NUMMER'].strip()
                branch_id = int(row['VESTIGINGSNUMMER'])
                school_id = '%s-%s' % (brin, branch_id)

                school_ids[school_id] = {
                    'brin': brin,
                    'branch_id': branch_id
                }

                # Remove leading/trailing spaces from field names and values.
                for key in row.keys():
                    row[key.strip()] = row[key].strip()

                origins = []
                for origin, country in settings['ORIGINS'].iteritems():
                    orig = {'country': country}
                    if row[origin].strip():
                        orig['students'] = int(row[origin].strip())
                    else:
                        orig['students'] = 0

                    origins.append(orig)

                if school_id not in students_by_origin:
                    students_by_origin[school_id] = origins

            for school_id, origs in students_by_origin.iteritems():
                school = DuoPoBranch(
                    brin=school_ids[school_id]['brin'],
                    branch_id=school_ids[school_id]['branch_id'],
                    reference_year=reference_year,
                    students_by_origin_reference_url=csv_url,
                    students_by_origin_reference_date=reference_date,
                    students_by_origin=origs
                )
                yield school

    def parse_po_pupil_zipcode_by_age(self, response):
        """
        Primair onderwijs > Leerlingen
        Parse "11. Leerlingen primair onderwijs per gemeente naar postcode leerling en leeftijd"
        """
        hxs = HtmlXPathSelector(response)

        # For some reason, DUO decided to create a seperate file for each
        # municipality, zip them and only provide xls files.
        available_zips = {}
        zips = hxs.select('//tr[.//a[contains(@href, ".zip")]]')
        for zip_file in zips:
            ref_date = zip_file.select('./td[1]/span/text()').extract()
            ref_date = datetime.strptime(ref_date[0], '%d %B %Y').date()

            zip_url = zip_file.select('.//a/@href').re(r'(.*\.zip)')[0]

            available_zips['http://duo.nl%s' % zip_url] = ref_date

        for zip_url, reference_date in available_zips.iteritems():
            reference_year = reference_date.year
            reference_date = str(reference_date)

            zip_file = requests.get(zip_url)

            csv_files = []
            zfiles = ZipFile(cStringIO.StringIO(zip_file.content))
            for zfile in zfiles.filelist:
                xls = cStringIO.StringIO(zfiles.read(zfile))
                # Suppress warnings as the xls files are wrongly initialized.
                with open(devnull, 'w') as OUT:
                    wb = xlrd.open_workbook(file_contents=xls.read(), logfile=OUT)
                sh = wb.sheet_by_index(0)
                data = []
                for rownum in xrange(sh.nrows):
                    data.append(sh.row_values(rownum))
                data = [[unicode(x) for x in row] for row in data]
                data = [';'.join(row) for row in data]
                data = '\n'.join(data)
                csv_files.append(csv.DictReader(cStringIO.StringIO(data.encode('utf8')), delimiter=';'))

            for csv_file in csv_files:
                school_ids = {}
                student_residences = {}

                for row in csv_file :
                    # Remove leading/trailing spaces from field names and values.
                    for key in row.keys():
                        row[key.strip()] = row[key].strip()

                    brin = row['BRIN_NUMMER'].strip()
                    branch_id = int(row['VESTIGINGSNUMMER'])
                    school_id = '%s-%s' % (brin, branch_id)

                    school_ids[school_id] = {
                        'brin': brin,
                        'branch_id': branch_id
                    }

                    if school_id not in student_residences:
                        student_residences[school_id] = []

                    student_residence = {
                        'zip_code': row['POSTCODE_LEERLING'].strip(),
                        'ages': []
                    }

                    for age in range(3, 26):
                        if row.has_key('LEEFTIJD_%i_JAAR' % age):
                            student_residence['ages'].append({
                                'age': age,
                                # Find out why Sicco casts to a float before he
                                # cast to an int..
                                'students': int(float(row['LEEFTIJD_%i_JAAR' % age].strip()))
                            })

                    student_residences[school_id].append(student_residence)

                    for school_id, residence in student_residences.iteritems():
                        school = DuoPoBranch(
                            brin=school_ids[school_id]['brin'],
                            branch_id=school_ids[school_id]['branch_id'],
                            reference_year=reference_year,
                            student_residences_reference_url=zip_url,
                            student_residences_reference_date=reference_date,
                            student_residences=residence
                        )

                    yield school

    def parse_po_student_year(self, response):
        """
        Primair onderwijs > Leerlingen
        Parse "11. Leerlingen (speciaal) basisonderwijs per schoolvestiging naar leerjaar"
        """

        for csv_url, reference_date in find_available_csvs(response).iteritems():
            reference_year = reference_date.year
            reference_date = str(reference_date)
            school_ids = {}
            years_per_branch = {}

            for row in parse_csv_file(csv_url):
                # Datasets 2011 and 2012 suddenly changed these field names. (?)
                if row.has_key('BRINNUMMER'):
                    row['BRIN NUMMER'] = row['BRINNUMMER']
                if row.has_key('GEMEENTE NUMMER'):
                    row['GEMEENTENUMMER'] = row['GEMEENTE NUMMER']
                if row.has_key('VESTIGINGS NUMMER'):
                    row['VESTIGINGSNUMMER'] = row['VESTIGINGS NUMMER']
                if row.has_key('VESTIGINSNUMMER'): # don't ask
                    row['VESTIGINGSNUMMER'] = row['VESTIGINSNUMMER']

                brin = row['BRIN NUMMER'].strip()
                branch_id = 0 if not row['VESTIGINGSNUMMER'] else int(row['VESTIGINGSNUMMER'])
                school_id = '%s-%s' % (brin, branch_id)

                school_ids[school_id] = {
                    'brin': brin,
                    'branch_id': branch_id
                }

                # Remove leading/trailing spaces from field names.
                for key in row.keys():
                    row[key.strip()] = row[key]

                years = {}
                possible_years = '1 2 3 4 5 6 7 8'.split()
                for year in possible_years:
                    if row['LEERJAAR %s' % year].strip():
                        years['year_%s' % year] = int(row['LEERJAAR %s' % year])
                    else:
                        years['year_%s' % year] = 0
                # Is there a total student number from somewhere?
                # if row['TOTAAL'].strip():
                #         years['students'] = int(row['TOTAAL'])

                if school_id not in years_per_branch:
                    years_per_branch[school_id] = {}

                years_per_branch[school_id] = years

            for school_id, y_per_branch in years_per_branch.iteritems():
                school = DuoPoBranch(
                    brin=school_ids[school_id]['brin'],
                    branch_id=school_ids[school_id]['branch_id'],
                    reference_year=reference_year,
                    students_by_year_reference_url=csv_url,
                    students_by_year_reference_date=reference_date,
                    students_by_year=y_per_branch
                )
                yield school

    def parse_spo_students_by_birthyear(self, response):
        """
        Passend onderwijs > Leerlingen
        Parse: "05. Leerlingen speciaal (basis)onderwijs naar geboortejaar"
        """

        for csv_url, reference_date in find_available_csvs(response).iteritems():
            reference_year = reference_date.year
            reference_date = str(reference_date)

            for row in parse_csv_file(csv_url):
                # Datasets 2011 and 2012 suddenly changed these field names. (?)
                if row.has_key('BRINNUMMER'):
                    row['BRIN NUMMER'] = row['BRINNUMMER']
                if row.has_key('VESTIGINGS NUMMER'):
                    row['VESTIGINGSNUMMER'] = row['VESTIGINGS NUMMER']
                if row.has_key('VESTIGINSNUMMER'): # don't ask
                    row['VESTIGINGSNUMMER'] = row['VESTIGINSNUMMER']


                branch = DuoPoBranch()
                branch['brin'] = row['BRIN NUMMER'].strip()
                branch['branch_id'] = 0 if not row['VESTIGINGSNUMMER'] else int(row['VESTIGINGSNUMMER'])
                branch['reference_year']=reference_year

                branch['spo_law'] = row['AANDUIDING WET']
                branch['spo_edu_type'] = row['SOORT PRIMAIR ONDERWIJS'] # possibly multiple with slash
                branch['spo_cluster'] = row['CLUSTER'] # i hope they don't use slashes                

                # ignoring total
                students_by_birthyear = []
                for k, v in row.iteritems():
                    row_words = k.split('.')
                    # k is of the form 'aantal.2005' or just the year (yes, really)
                    if row_words[-1].isdigit() and v.isdigit() and int(v)>0 :
                        students_by_birthyear.append({
                            'birthyear' : int(row_words[-1]),
                            'students' : int(v),
                        })
                        

                branch['spo_students_by_birthyear'] = students_by_birthyear
                branch['spo_students_by_birthyear_reference_url'] = csv_url
                branch['spo_students_by_birthyear_reference_date'] = reference_date

                yield branch
    
    def parse_spo_students_by_edu_type(self, response):
        """
        Primair onderwijs > Leerlingen
        Parse "06. Leerlingen speciaal (basis)onderwijs naar onderwijssoort"
        """

        for csv_url, reference_date in find_available_csvs(response).iteritems():
            reference_year = reference_date.year
            reference_date = str(reference_date)
            school_ids = {}
            spo_students_by_edu_type_per_school = {}

            for row in parse_csv_file(csv_url):
                # strip leading and trailing whitespace.
                for key in row.keys():
                    value = (row[key] or '').strip()
                    row[key] = value or None
                    row[key.strip()] = value or None

                # Datasets 2011 and 2012 suddenly changed these field names.
                if row.has_key('BRINNUMMER'):
                    row['BRIN NUMMER'] = row['BRINNUMMER']
                if row.has_key('VESTIGINGS NUMMER'):
                    row['VESTIGINGSNUMMER'] = row['VESTIGINGS NUMMER']
                if row.has_key('VESTIGINSNUMMER'): # don't ask
                    row['VESTIGINGSNUMMER'] = row['VESTIGINSNUMMER']

                if row.has_key('INDICATIE SPECIAAL (BASIS)ONDERWIJS'): # really now
                    row['INDICATIE SPECIAL BASIS ONDERWIJS'] = row['INDICATIE SPECIAAL (BASIS)ONDERWIJS']

                brin = row['BRIN NUMMER'].strip()
                if row['VESTIGINGSNUMMER'].strip():
                    branch_id = int(row['VESTIGINGSNUMMER'])
                school_id = '%s-%s' % (brin, branch_id)

                school_ids[school_id] = {
                    'brin': brin,
                    'branch_id': branch_id
                }


                spo_students_by_edu_type = {
                    'spo_indication' : row['INDICATIE SPECIAL BASIS ONDERWIJS'],
                    'sbao' : int(row['SBAO'] or 0),
                    'so' : int(row['SO'] or 0),
                    'vso' : int(row['VSO'] or 0),
                    }

                if school_id not in spo_students_by_edu_type_per_school:
                    spo_students_by_edu_type_per_school[school_id] = []

                spo_students_by_edu_type_per_school[school_id].append(spo_students_by_edu_type)

            for school_id, per_school in spo_students_by_edu_type_per_school.iteritems():
                school = DuoPoBranch(
                    brin=school_ids[school_id]['brin'],
                    branch_id=school_ids[school_id]['branch_id'],
                    reference_year=reference_year,
                    spo_students_by_edu_type_reference_url=csv_url,
                    spo_students_by_edu_type_reference_date=reference_date,
                    spo_students_by_edu_type=per_school
                )
                yield school

    def parse_spo_students_by_advice(self, response):
        """
        Primair onderwijs > Leerlingen
        Parse "12. Leerlingen (speciaal) basisonderwijs per schoolvestiging naar schooladvies"
        """

        for csv_url, reference_date in find_available_csvs(response).iteritems():
            reference_year = reference_date.year
            reference_date = str(reference_date)
            school_ids = {}
            spo_students_by_advice_per_school = {}

            for row in parse_csv_file(csv_url):
                # strip leading and trailing whitespace.
                for key in row.keys():
                    value = (row[key] or '').strip()
                    row[key] = value or None
                    row[key.strip()] = value or None

                # Datasets 2011 and 2012 suddenly changed these field names.
                if row.has_key('BRINNUMMER'):
                    row['BRIN NUMMER'] = row['BRINNUMMER']
                if row.has_key('VESTIGINGS NUMMER'):
                    row['VESTIGINGSNUMMER'] = row['VESTIGINGS NUMMER']
                if row.has_key('VESTIGINSNUMMER'): # don't ask
                    row['VESTIGINGSNUMMER'] = row['VESTIGINSNUMMER']

                brin = row['BRIN NUMMER'].strip()
                if row['VESTIGINGSNUMMER'].strip():
                    branch_id = int(row['VESTIGINGSNUMMER'])
                school_id = '%s-%s' % (brin, branch_id)

                school_ids[school_id] = {
                    'brin': brin,
                    'branch_id': branch_id
                }


                spo_students_by_advice = {
                    # TODO intOrNone
                    'vso' : int(row['VSO'] or 0),
                    'pro' : int(row['PrO'] or 0),
                    'vmbo_bl' : int(row['VMBO BL'] or 0),
                    'vmbo_bl_kl' : int(row['VMBO BL-KL'] or 0),
                    'vmbo_kl' : int(row['VMBO KL'] or 0),
                    'vmbo_kl_gt' : int(row['VMBO KL-GT'] or 0),
                    'vmbo_gt' : int(row['VMBO GT'] or 0),
                    'vmbo_gt_havo' : int(row['VMBO GT-HAVO'] or 0),
                    'havo' : int(row['HAVO'] or 0),
                    'havo_vwo' : int(row['HAVO-VWO'] or 0),
                    'vwo' : int(row['VWO'] or 0),
                    'unknown' : int(row['ONBEKEND'] or 0),
                    }

                if school_id not in spo_students_by_advice_per_school:
                    spo_students_by_advice_per_school[school_id] = []

                spo_students_by_advice_per_school[school_id].append(spo_students_by_advice)

            for school_id, per_school in spo_students_by_advice_per_school.iteritems():
                school = DuoPoBranch(
                    brin=school_ids[school_id]['brin'],
                    branch_id=school_ids[school_id]['branch_id'],
                    reference_year=reference_year,
                    spo_students_by_advice_reference_url=csv_url,
                    spo_students_by_advice_reference_date=reference_date,
                    spo_students_by_advice=per_school
                )
                yield school


class DuoPaoCollaborationsSpider(BaseSpider):
    name = 'duo_pao_collaborations'

    def start_requests(self):
        return [
            Request('http://data.duo.nl/organisatie/open_onderwijsdata/'
                    'databestanden/passendow/Adressen/Adressen/passend_po_1.asp',
                    self.parse_collaborations),
            Request('http://data.duo.nl/organisatie/open_onderwijsdata/'
                    'databestanden/passendow/Adressen/Adressen/passend_po_3.asp',
                    self.parse_collaborations),
            Request('http://data.duo.nl/organisatie/open_onderwijsdata/'
                    'databestanden/passendow/Adressen/Adressen/passend_vo_1.asp',
                    self.parse_collaborations),
            Request('http://data.duo.nl/organisatie/open_onderwijsdata/'
                    'databestanden/passendow/Adressen/Adressen/passend_vo_7.asp',
                    self.parse_collaborations),
        ]

    def parse_collaborations(self, response):
        """
        Passend onderwijs > Adressen
        Parse: "01. Adressen samenwerkingsverbanden lichte ondersteuning primair onderwijs"
        Parse: "03. Adressen samenwerkingsverbanden passend onderwijs, primair onderwijs"
        Parse: "05. Adressen samenwerkingsverbanden lichte ondersteuning, voortgezet onderwijs"
        Parse: "07. Adressen samenwerkingsverbanden passend onderwijs, voortgezet onderwijs"
        """
        # Fields that do not need additonal processing
        collaboration_fields = {
            'SAMENWERKINGSVERBAND': 'collaboration'
        }

        for csv_url, reference_date in find_available_csvs(response).iteritems():
            reference_year = reference_date.year
            reference_date = str(reference_date)
            for row in parse_csv_file(csv_url):

                collaboration = DuoPaoCollaboration()
                
                cid = row['ADMINISTRATIENUMMER'].strip()
                if '-' in cid:
                    int_parts = map(int_or_none, cid.split('-'))
                    if any([i == None for i in int_parts]):
                        cid = '-'.join(map(str, int_parts))
                collaboration['collaboration_id'] = cid

                collaboration['address'] = {
                    'street': row['ADRES'].strip() or None,
                    'city': row['PLAATSNAAM'].strip() or None,
                    'zip_code': row['POSTCODE'].replace(' ', '') or None
                }

                collaboration['correspondence_address'] = {
                    'street': row['CORRESPONDENTIEADRES'],
                    'city': row['PLAATS CORRESPONDENTIEADRES'],
                    'zip_code': row['POSTCODE CORRESPONDENTIEADRES'].replace(' ', '')
                }

                for field, field_norm in collaboration_fields.iteritems():
                    collaboration[field_norm] = row[field]

                collaboration['reference_year'] = reference_year
                collaboration['ignore_id_fields'] = ['reference_year']

                yield collaboration
