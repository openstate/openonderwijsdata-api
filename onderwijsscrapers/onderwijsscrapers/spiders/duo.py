import csv
import cStringIO
import locale
import xlrd
from datetime import datetime
from os import devnull
from zipfile import ZipFile
from collections import defaultdict

import requests
from scrapy.spider import BaseSpider
from scrapy.http import Request
from scrapy.selector import HtmlXPathSelector

locale.setlocale(locale.LC_ALL, 'nl_NL.UTF-8')



class DuoSpider(BaseSpider):
    """ Duo spider """
    def __init__(self):
        self.requests = {}

    def start_requests(self):

        return [
            Request(
                'http://data.duo.nl/organisatie/open_onderwijsdata/databestanden/' + url, 
                # lambda self, response: self.parse_cvs(self, response, parse_row)
                parse_row
            ) for url,parse_row in self.requests.items()
        ]


    # # lambda self, response: self.parse_cvs(response, parse_row)
    # def parse_cvs(self, response, parse_row):
    #     """
    #     Parse the CVS function
    #     `parse_row` returns a scrapy item
    #     """

    #     for csv_url, reference_date in find_available_csvs(response).iteritems():
    #         reference_year = reference_date.year
    #         reference_date = str(reference_date)
    #         yield parse_row(row)

    # # lambda self, response: self.parse_cvs_seperate(response, parse_row, DuoPoSchool, 'po_lo_collaboration')
    # # def some_parse_row(row):
    # #     yield row['BRIN'], {
    # #         'brin' : \
    # #             row['BRIN NUMMER']
    # #         'po_lo_collaboration' : \
    # #             row['ADMINISTRATIENUMMER']
    # #     }
    # def parse_cvs_separate(self, response, parse_row, itemtype, setname):
    #     """
    #     Parse the CVS function
    #     `parse_row` returns an index & dict for separate dataset
    #     """

    #     for csv_url, reference_date in find_available_csvs(response).iteritems():
    #         reference_year = reference_date.year
    #         reference_date = str(reference_date)
    #         items = defaultdict(list)

    #         # Collect all items
    #         for row in parse_csv_file(csv_url):
    #             k,v = parse_row(row)
    #             items[k].append(v)

    #         # Create objects for items
    #         for value in items.values():
    #             value.update({
    #                 'reference_year' = reference_year,
    #                 setname+'_reference_url' = csv_url,
    #                 setname+'_reference_date' = reference_date,
    #             })
    #             yield itemtype(value)



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

def find_available_zips(response):
    """ Get all URLS of ZIP files on the DUO page """
    hxs = HtmlXPathSelector(response)
    available_zips = {}
    zips = hxs.select('//tr[.//a[contains(@href, ".zip")]]')
    for zip_file in zips:
        ref_date = zip_file.select('./td[1]/span/text()').extract()
        ref_date = datetime.strptime(ref_date[0], '%d %B %Y').date()

        zip_url = zip_file.select('.//a/@href').re(r'(.*\.zip)')[0]

        available_zips['http://duo.nl%s' % zip_url] = ref_date
    return available_zips

def extract_csv_files(zip_url):
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

    return csv_files


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