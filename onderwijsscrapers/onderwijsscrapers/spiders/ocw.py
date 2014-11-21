import requests
from scrapy.spider import Spider
from scrapy.http import Request
from itertools import islice
import cStringIO
from os import devnull
import xlrd

from onderwijsscrapers.items import OCWPoBranch

def float_or_none(string):
    try:
        return float(string.replace(',','.'))
    except Exception:
        return None

class OCWPoBranchesSpider(Spider):
    name = 'ocw_po_branches'

    def start_requests(self):
        return [
            Request(
                'http://www.rijksoverheid.nl/ministeries/ocw/documenten-en-publicaties/'
                'wob-verzoeken/2013/09/26/bijlage-bij-besluit-op-bezwaar-wob-verzoek-'
                'inzake-eindresultaten-van-leerlingen-van-groep-8-op-basisscholen.html', 
                self.parse_po_finals
            )
        ]

    def parse_po_finals(self, response):
        """
        Bijlage bij besluit op bezwaar Wob-verzoek inzake eindresultaten van leerlingen van groep 8 op basisscholen

        Parses primary schools final examination scores.
        Schools can use different test types.
        Some test types have two parts, an RW and BL test.
        Other test types have associated DE or VHE score variants.
        There are two student counts, DLN and AFN.
        """
        years =  [2010, 2011, 2012]



        sels = response.xpath('.//a[contains(@href, ".xls")]/@href')
        xls_urls = ['http://www.rijksoverheid.nl%s'%sel.extract() for sel in sels]

        # just download the first xls file and use the first sheet
        xls_file = requests.get(xls_urls[0])
        xls = cStringIO.StringIO(xls_file.content)
        with open(devnull, 'w') as OUT:
            wb = xlrd.open_workbook(file_contents=xls.read(), logfile=OUT)
        sh = wb.sheet_by_index(0)

        head = sh.row_values(0)
        for n in xrange(1, sh.nrows):
            row = dict(zip(head, sh.row_values(n)))

            brin = row['BRIN']
            branch_id = int(row['VESTNR'])

            school = OCWPoBranch(brin = brin, branch_id = branch_id, reference_year = None)
            school['ignore_id_fields'] = ['reference_year']
            school['name'] = row['naam'].strip()
            school['address'] = {
                'street': row['adres'].strip(),
                'city': row['plaats'].strip(),
                'zip_code': row['postcode'].strip().replace(' ', '')
            }
            school['denomination'] = row['denominatie'].strip()
            school['vision'] = row['visie'].strip()
            school['board_name'] = row['bestuur'].strip()
            school['school_type'] = row['schooltype'].strip()
            yield school


            for y in years:
                school = OCWPoBranch(brin = brin, branch_id = branch_id, reference_year = y)
                scores = {}
                scores['test'] = row['TOETS_%s'%y].strip()

                for n in ['N_AFN', 'N_DLN']:
                    n_val = row['%s_%s'%(n,y)].split()
                    if len(n_val) == 1:
                        scores[n.lower()] = float_or_none(n_val[0])
                    if len(n_val) == 4:
                        # bl: $ rw: $
                        scores['%s_bl'%n.lower()] = float_or_none(n_val[1])
                        scores['%s_rw'%n.lower()] = float_or_none(n_val[3])

                if scores['test'] == 'lvs':
                    bl = row['VERSIE_BL_%s'%y].strip()
                    if bl and bl != 'NEE' and bl != '-':
                        scores['bl_version'] = ' '.join(sorted(bl.lower().split()))
                        
                    rw = row['VERSIE_RW_%s'%y].strip()
                    if rw and rw != 'NEE' and rw != '-':
                        scores['rw_version'] = ' '.join(sorted(rw.lower().split()))

                if row['SCORE_JR_%s'%y] != 'minder dan 5 leerlingen':
                    for s in row['SCORE_JR_%s'%y].split('|'):
                        val = s.strip().split(':')
                        if len(val) == 2:
                            k,v = val
                            k = k.lower()
                            if "dle" in k:
                                k = '%s_dle' % k
                            k = k.replace('%dle ','')
                            k = k.replace('-','_')
                            k = k.replace('#','')
                            k = k.replace(' ','_')
                            v = v.split()
                            # (vhd) & (%de)
                            if v and len(v) > 1 and v[1][0]=='(' and v[1][-1]==')':
                                k  = '%s_%s' % (k, v[1][1:-1].replace('%',''))
                            v = float_or_none(v[0]) if v else None
                            if v is not None:
                                scores[k] = v

                    for k in scores.keys():
                        if scores[k] is None:
                            scores.pop(k)

                    if scores['test'] in ['', 'anders']:
                        scores['test'] = None

                school['mean_finals'] = scores
                yield school

