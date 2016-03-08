from __future__ import absolute_import
from datetime import datetime
import locale
import csv
import re

import os
import urlparse, urllib, urllib2
from messytables import any_tableset, CSVRowSet, \
  headers_guess, headers_processor, \
  offset_processor, error

from scrapy.spider import Spider
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors import LinkExtractor
from scrapy.http import Request

from onderwijsscrapers.items import FlexibleItem

from transformer import Transformer
from structure_utils import structure

locale.setlocale(locale.LC_ALL, 'nl_NL.UTF-8')

## Utilities

def extend_to_blank(l):
    """ Transform ['','a','','b',''] into ['','a','a','b','b'] """
    out, extend = [], ''
    for i in l:
        extend = i or extend
        out.append(extend)
    return out

def flatten_headers(row_set):
    """Flatten multiple header rows using newlines, extending blank cells"""
    offset, headers = headers_guess(row_set.sample)

    if offset>0:
        header_rows = islice(row_set.sample, offset+1)
        extended = (extend_to_blank(c.value for c in r) for r in header_rows)
        headers = ['\n'.join(l) for l in zip(*extended)]

    row_set.register_processor(headers_processor(headers))
    row_set.register_processor(offset_processor(offset + 1))
    return headers

def schematable2fields(schematable):
    fields = []
    for row in csv.DictReader(schematable):
        descriptor = {'constraints':{'required':False}}
        if row.get('name', None):
            descriptor.update(row)
            if not descriptor['type']:
                descriptor.pop('type')
            fields.append( descriptor )
    return fields

## Spiders

class DuoSpider(CrawlSpider):
    name = 'duo'
    allowed_domains = ['duo.nl']

    start_urls = ['https://duo.nl/open_onderwijsdata/databestanden/']
    rules = (
        Rule(LinkExtractor(allow=(r'databestanden', )), 
             follow=True, callback='parse_item'),
    )

    def get_sources(self):
        for source in self.sources:
            req = Request(source['web'], self.parse_item)
            req.meta['source'] = source
            yield req

    def __init__(self, sources=None, cache=None, schema_dir='.'):
        """Either use start_urls+rules or use get_sources"""
        self.cache = cache
        self.schema_dir = schema_dir

        if self.name != 'duo' and not sources:
            # for overriding class
            sources = self.name+'.csv'

        if sources:
            self.sources = csv.DictReader(open(sources))
            self.start_requests = self.get_sources

        CrawlSpider.__init__(self)

    def parse_item(self, response):
        """ source -> scrape -> table -> row """
        source = response.meta.get('source', {})
        if response.url.split('/')[-1] != 'default.asp':
            scrapes = self.get_scrapes(response)
            for scrape in self.match_scrapes(source, scrapes):
                for table in self.match_scrape_tables(source, scrape):
                    
                    schema_name = source.get('schema')
                    fname = os.path.join(self.schema_dir, schema_name+'.csv')
                    schema = {"fields": schematable2fields(open(fname))}
                    schema = Transformer(schema, metadata=scrape)

                    headers = next(table.dicts(sample=True)).keys()
                    schema.fit(headers)

                    rows = (row.values() for row in table.dicts())
                    for doc in structure(schema.transform(rows)):
                        yield FlexibleItem(**doc)

    def get_scrapes(self, response):
        """Scrape the page for links to tables"""
        extensions = ['csv', 'xls', 'zip']
        scraped = False
        for ext in extensions:
            for cell in response.xpath('//tr[.//a[contains(@href, ".%s")]]'%ext):
                scrape = {}

                ref_date = cell.xpath('./td[1]/span/text()').extract()
                scrape['peildatum'] = \
                    datetime.strptime(ref_date[0], '%d %B %Y').date()
                scrape['reference_year'] = \
                    datetime.strptime(ref_date[0], '%d %B %Y').year
                scrape['status']  = \
                    cell.xpath('./td[2]/text()').extract()[0]
                
                scrape['page_title'] = \
                    response.xpath("//h1/text()").extract()[0]
                scrape['page_url'] = \
                    response.url
                
                scrape['file_title']  = \
                    cell.xpath('./td[3]/a/@alt').extract()[0]
                scrape['file_link'] = \
                    cell.xpath('.//a/@href').re(r'(.*\.%s)' % ext)[0]

                yield scrape
                scraped = True
            if scraped:
                break # only get the urls for the best file types

    def match_scrapes(self, source, scrapes):
        """Yield the scrapes that match this source"""
        for scrape in scrapes:
            title_match = source.get('file_title', None) or '.*'
            if re.match(title_match, scrape['file_title']):
                yield scrape

    def match_scrape_tables(self, source, scrape):
        """Yield the (messy)tables that match this source"""
        url, link = scrape['page_url'], scrape['file_link']
        ext = os.path.splitext(urlparse.urlparse(link).path)[1][1:]
        with self.download_or_cache(url, link) as fobj:
            # find matching tables in file
            table_match = source.get('table', None)
            # auto-detect file format
            table_set = any_tableset(fobj, extension=ext, quotechar='"')
            for row_set in table_set.tables:
                if (not table_match) or re.match(table_match, row_set.name):
                    # combine multiple header rows into a single header
                    flatten_headers(row_set)
                    yield row_set

    def download_or_cache(self, page_url, file_link):
        """Download a file or try to read it from a cache directory"""
        file_url = urlparse.urljoin(page_url, file_link)
        if self.cache:
            # see if the file is in the cache
            local_path = urlparse.urlparse(file_link).path.lstrip('/')
            cache_path = os.path.join(self.cache, local_path)
            if not os.path.exists(os.path.dirname(cache_path)):
                os.makedirs(os.path.dirname(cache_path))
            if not os.path.isfile(cache_path):
                # TODO: log download
                # download the file into the cache
                urllib.urlretrieve(file_url, cache_path)
            return open(cache_path)
        else:
            return urllib2.urlopen(file_url)

class DuoVoBoardsSpider(DuoSpider):
    name = 'duo_vo_boards'

class DuoVoSchoolsSpider(DuoSpider):
    name = 'duo_vo_schools'

class DuoVoBranchesSpider(DuoSpider):
    name = 'duo_vo_branches'

class DuoPoBoardsSpider(DuoSpider):
    name = 'duo_po_boards'

class DuoPoSchoolsSpider(DuoSpider):
    name = 'duo_po_schools'

class DuoPoBranchesSpider(DuoSpider):
    name = 'duo_po_branches'

class DuoPaoCollaborationsSpider(DuoSpider):
    name = 'duo_pao_collaborations'

class DuoMboBoardSpider(DuoSpider):
    name = 'duo_mbo_boards'

class DuoMboInstitutionSpider(DuoSpider):
    name = 'duo_mbo_institutions'

class DuoHoInstitutionsSpider(DuoSpider):
    name = 'duo_ho_institutions'

class DuoHoBoardsSpider(DuoSpider):
    name = 'duo_ho_boards'