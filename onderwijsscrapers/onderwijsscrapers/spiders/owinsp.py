import csv
from datetime import datetime
import re
import urlparse

from scrapy.conf import settings
from scrapy.spider import BaseSpider
from scrapy.http import Request
from scrapy.selector import HtmlXPathSelector

from onderwijsscrapers.items import VOSchool

SCHOOL_ID = re.compile(r'(sch_id=\d+)')
PAGES = re.compile(r'^Pagina (\d+) van (\d+)$')
ZIPCODE = re.compile(r'(\d{4}\s?\w{2})')


class OWINSPSpider(BaseSpider):
    search_url = 'http://toezichtkaart.owinsp.nl/schoolwijzer/'\
                 'zoekresultaat?xl=0&p1=%%23&p2=maxpg&p3=-1&p1=%%23'\
                 '&p2=hits&p3=-1&p1=sector&p2=%%3D'\
                 '&p3=%(education_sector)s&p1=naam&p2=%%3D&p3=&p1=postcode'\
                 '&p2=%%3D&p3=%(zipcode)s&p1=%%23&p2=submit&p3=Zoeken'\
                 '&p1=%%23&p2=curpg&p3=1'

    def open_blocks(self, url):
        """ Append '.22' to a matched school_id, in order to obtain urls to
        pages where the content blocks are unfolded. """
        def _open(match):
            return '%s.22' % match.group(1)

        return re.sub(SCHOOL_ID, _open, url)

    def generate_search_urls(self):
        raise NotImplementedError('Your spider should implement this method.')

    def start_requests(self):
        return [Request(url, self.parse_search_results) for url in
                self.generate_search_urls()]

    def parse_search_results(self, response):
        hxs = HtmlXPathSelector(response)

        # Extract the link to the detail page of each school
        search_hits = hxs.select('//li[@class="match"]/noscript/a/@href')
        if not search_hits:
            return

        for link in search_hits:
            url = 'http://toezichtkaart.owinsp.nl/schoolwijzer/%s'\
                % link.extract()
            # Find sch_id, and append '.22' to unfold content blocks
            url = self.open_blocks(url)

            yield Request(url, self.parse_education_structure_page)

        pages = hxs.select('//span[@class="pagnr"]/text()').extract()[0]\
                                                           .strip()
        current_page, total_pages = re.compile(r"^Pagina (\d+) van (\d+)$")\
                                      .search(pages).groups()

        if current_page != total_pages:
            nav_urls = hxs.select('//span[@class="browse"]/noscript//a')
            if len(nav_urls) > 1:
                next_page = nav_urls[1].select('@href').extract()
            else:
                next_page = nav_urls[0].select('@href').extract()

            yield Request('http://toezichtkaart.owinsp.nl/schoolwijzer/%s'
                          % next_page[0], self.parse_search_results)

    def parse_organisation_detail_page(self, response):
        raise NotImplementedError('Your spider should implement this method.')


class VOSpider(OWINSPSpider):
    name = 'vo.owinsp.nl'

    def generate_search_urls(self, zips=settings['ZIPCODES']):
        with open(zips, 'r') as f:
            search_urls = [self.search_url % {'education_sector': 'vo',
                                              'zipcode': line.strip()}
                           for line in f]

        return search_urls

    def parse_search_results(self, response):
        hxs = HtmlXPathSelector(response)

        # Extract the link to the detail page of each school
        search_hits = hxs.select('//li[@class="match"]/noscript/a/@href')
        if not search_hits:
            return

        for link in search_hits:
            url = 'http://toezichtkaart.owinsp.nl/schoolwijzer/%s'\
                % link.extract()
            # Find sch_id, and append '.22' to unfold content blocks
            url = self.open_blocks(url)

            yield Request(url, self.parse_education_structure_page)

        pages = hxs.select('//span[@class="pagnr"]/text()').extract()[0]\
                                                           .strip()

        page_match = PAGES.search(pages)

        if page_match:
            current_page, total_pages = page_match.groups()

            if current_page != total_pages:
                nav_urls = hxs.select('//span[@class="browse"]/noscript//a')
                if len(nav_urls) > 1:
                    next_page = nav_urls[1].select('@href').extract()
                else:
                    next_page = nav_urls[0].select('@href').extract()

                yield Request('http://toezichtkaart.owinsp.nl/schoolwijzer/%s'
                              % next_page[0], self.parse_search_results)

    def parse_education_structure_page(self, response):
        """ This method is specific for the VO-schools, as these can have
        multiple educational structures (vmbo, havo, vwo, ...) """
        hxs = HtmlXPathSelector(response)
        structures = hxs.select('//li[@class="match"]/noscript/a')

        # The VOSchool item to be populated
        organisation = VOSchool()
        organisation['education_structures_to_scrape'] = set()

        # If we end up at the schools page directly, immediately yield request
        if not structures:
            request = Request(response.url, self.parse_organisation_detail_page)
            request.meta['item'] = organisation
            yield request

        organisation['name'] = hxs.select('//h1[@class="stitle"]/text()').extract()[0].strip()
        organisation['education_structures'] = []
        organisation['current_ratings'] = []

        crawl_structures = {}
        for structure in structures:
            url = 'http://toezichtkaart.owinsp.nl/schoolwijzer/%s'\
                % structure.select('@href').extract()[0]
            url = self.open_blocks(url)
            crawl_structures[url] = structure.select('text()').extract()[0]
            organisation['education_structures_to_scrape'].add(url)

        for url, structure in crawl_structures.iteritems():
            request = Request(url, self.parse_organisation_detail_page)
            request.meta['item'] = organisation
            request.meta['structure'] = structure
            yield request

    def parse_organisation_detail_page(self, response):
        organisation = response.meta['item']
        structure = response.meta['structure']

        hxs = HtmlXPathSelector(response)
        h_content = hxs.select('//div[@id="hoofd_content"]')
        address = h_content.select('./p[@class="detpag"]/text()').extract()
        address = ', '.join([x.strip() for x in address])
        organisation['address'] = {
            'street': address.replace(u'\xa0\xa0', u' '),
            'city': None,
            'zip_code': None
        }

        website = h_content.select('ul/li[@class="actlink"]/a/@href').extract()
        if website:
            organisation['website'] = website[0]
        else:
            organisation['website'] = None

        organisation['denomination'] = h_content.select('p/em/text()')\
                                                .extract()[0].strip()

        if 'education_structures' not in organisation:
            organisation['education_structures'] = []

        rating_excerpt = h_content.select('p[3]/text()').extract()[1].strip()

        # Wait... what? Are we going to use an element's top-padding to
        # get the div we are interested in? Yes we are :(.
        tzk_rating = hxs.select('//div[@class="content_main wide" and @style'
                                '="padding-top:0px"]/div[@class="tzk"]')
        rating = tzk_rating.select('div/text()').extract()
        if rating:
            # There are schools without ratings, such as new schools
            current_rating = rating[0]
            rating_valid_since = tzk_rating.select('h3/div/text()')\
                .extract()[0].replace('\n', ' ').strip()[-10:]

            # Try to parse the date
            try:
                rating_valid_since = datetime.strptime(rating_valid_since,
                                                       '%d-%m-%Y')
                rating_valid_since = rating_valid_since.date().isoformat()
            except:
                rating_valid_since = None
        else:
            current_rating = None
            rating_valid_since = None

        urlparams = urlparse.parse_qs(response.url)
        owinsp_id = urlparams['sch_id'][0].split('.')[0]

        organisation['education_structures'].append(structure)
        organisation['current_ratings'].append({
            'education_structure': structure,
            'owinsp_id': owinsp_id,
            'owinsp_url': response.url,
            'rating': current_rating,
            'rating_valid_since': rating_valid_since,
            'rating_excerpt': rating_excerpt
        })

        if 'reports' not in organisation:
            organisation['reports'] = []

        reports = hxs.select('//div[@class="report" and span'
                             '[@class="icoon_pdf2"]]/span'
                             '[@class="icoon_download"]/a')
        if reports:
            report_urls = []

            for report in reports:
                title = report.select('text()').extract()[0]
                date, title = title.split(': ')
                try:
                    # Try to parse date
                    date = datetime.strptime(date, '%d-%m-%Y')\
                                   .strftime('%Y-%m-%d')
                except:
                    pass

                url = 'http://toezichtkaart.owinsp.nl/schoolwijzer/%s'\
                    % report.select('@href').extract()[0]

                # Some pages contain the same reports multiple times, we
                # only want to include them once.
                if url in report_urls:
                    continue

                organisation['reports'].append({
                    'education_structure': structure,
                    'url': url,
                    'title': title.strip(),
                    'date': date
                })

                report_urls.append(url)

        if 'rating_history' not in organisation:
            organisation['rating_history'] = []

        rating_history = hxs.select('//table[@summary="Rapporten"]//'
                                    'li[@class="arrref"]/text()').extract()
        if rating_history:
            for ratingstring in rating_history:
                date, rating = ratingstring.split(': ')
                try:
                    # Try to parse date
                    date = datetime.strptime(date, '%d-%m-%Y')\
                                   .strftime('%Y-%m-%d')
                except:
                    pass

                organisation['rating_history'].append({
                    'education_structure': structure,
                    'rating': rating.strip(),
                    'date': date
                })

        # Remove this structure from education_sectors_to_scrape
        organisation['education_structures_to_scrape'].remove(response.url)

        # If all structures are scraped, either return the item or crawl
        # the 'Opbrengstenoordeel'
        if not organisation['education_structures_to_scrape']:
            del organisation['education_structures_to_scrape']
            result_url = hxs.select('//ul[@class="opboor"]//a/@href').extract()

            if not result_url:
                yield organisation
            else:
                # Append '&p_navi=11111' in order to open all tabs
                organisation['result_card_url'] = result_url[0] + '&p_navi=11111'
                urlparams = urlparse.parse_qs(urlparse.urlparse(
                    organisation['result_card_url']).query)
                organisation['brin'] = urlparams['p_brin'][0]
                try:
                    branch_id = int(urlparams['p_vestnr'][0])
                except:
                    pass

                organisation['branch_id'] = branch_id

                request = Request(organisation['result_card_url'],
                                  self.parse_resultcard)
                request.meta['organisation'] = organisation

                yield request

    def parse_resultcard(self, response):
        hxs = HtmlXPathSelector(response)
        organisation = response.meta['organisation']

        address_table = hxs.select('//table[@summary="Adresgegevens school"]')

        if not address_table:
            # Some pages are empty, so just return organisation here
            return organisation

        organisation['board'] = address_table.select('tr[td/text() ="Bevoegd '
                                                     'gezag"]/td[2]/text()')\
                                             .extract()[0]

        board_id = address_table.select('tr[td/text() ="Bevoegd gezagnr."]/'
                                        'td[4]/text()').extract()[0]

        try:
            board_id = int(board_id)
        except:
            pass

        organisation['board_id'] = board_id

        organisation['address'].update({'city': None, 'zip_code': None})

        organisation['address']['street'] = address_table.select('tr[td/text() ='
                                                                 '"Adres"]/td[2]'
                                                                 '/text()').extract()[0]

        branch_id = address_table.select('tr[td/text() ="Vestigingsnr."]/td[4]'
                                         '/text()').extract()[0]
        try:
            branch_id = int(branch_id)
        except:
            pass

        organisation['branch_id'] = branch_id

        place = address_table.select('tr[td/text() ="Plaats"]/td[2]/text()')\
                             .extract()[0].replace(u'\xa0', '')

        zip_code = re.match(ZIPCODE, place)
        if zip_code:
            organisation['address']['zip_code'] = zip_code.group(1)\
                .replace(' ', '')
            city = re.sub(ZIPCODE, '', place)
            organisation['address']['city'] = city.strip()

        return organisation


class POSpider(OWINSPSpider):
    name = 'po.owinsp.nl'

    search_url = 'http://toezichtkaart.owinsp.nl/schoolwijzer/zoekresultaat'\
                 '?xl=1&sector=%%23&sch_id=-1&arr_id=-1&p1=%%23&p2=curpg&p3=-1'\
                 '&p1=%%23&p2=maxpg&p3=0&p1=%%23&p2=hits&p3=301.09&p1=sector'\
                 '&p2=%%3D&p1=naam&p2=%%3D&p1=plaats&p2=%%3D&p1=afstand&p2=%%3D&'\
                 'p1=pc_num&p2=%%3D&p3=PO&p3=&p3=&p3=&p3=&p1=brin&p2=%%3D'\
                 '&p3=%(brin)s&p1=%%23&p2=submit&p3=Zoeken'

    def generate_search_urls(self, addresses=settings['PO_ADDRESSES']):
        with open(addresses, 'rb') as f:
            reader = csv.DictReader(f, delimiter=';')
            search_urls = [self.search_url % {'brin': row['BRIN NUMMER']}
                           for row in reader]

        return search_urls

    def parse_search_results(self, response):
        hxs = HtmlXPathSelector(response)
        search_hits = hxs.select('//li[@class="match"]/noscript/a/@href')

        if search_hits:
            # There are multiple schools with this BRIN (probably different
            # branches of the same school), so make sure to process each one
            pass
        else:
            # Check whether we've found a school or not
            pass

    def parse_organisation_detail_page(self, response):
        raise NotImplementedError('Implement this')
