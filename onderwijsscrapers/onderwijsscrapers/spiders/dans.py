import csv
from scrapy.spider import BaseSpider
from scrapy.http import Request
import os
from itertools import islice

from onderwijsscrapers.items import DANSVoBranch

def float_or_none(string):
    try:
        return float(string.replace(',','.'))
    except Exception:
        return None

class DANSVoBranchesSpider(BaseSpider):
    name = 'dans_vo_branches'

    def __init__(self, root_path=''):
        self.root_path = root_path


    def start_requests(self):
        return [
            Request(
                'https://easy.dans.knaw.nl/ui/datasets/id/easy-dataset:57879', 
                self.parse_all
            )
        ]

    def parse_all(self, response):
        """
        Uses information from `bestandsbeschrijving.doc`
        """
        # Doesn't use `response`

        # The .cvs files, and .fields.cvs files
        csvs = [
          'achtergrond12',
          'exvk12',
          'naw13',
          'ok2013',
          'verschilsece1012',
          'adv12',
          'idu12',
          'oordeel1113',
          'exvc12',
          'lwoo12',
        ]

        # Data format definitions
        formats = {
          'F1' : int,
          'F2' : int,
          'F3' : int,
          'F4' : int,
          'F5' : int,
          'F8.2' : lambda s: float(s.replace(',','.')),
        }

        # Values coded with integer identifiers, from .values.csv files
        # header: value;description
        coded_values = [
          'opbrengst',
          'regnr',
          'opl',
          'soortlln',
          'vak',
          'leerweg',
        ]
        coded_values = {
          cname : { 
            int(row.pop('value')) : row.pop('description')
            for row in csv.DictReader(file(os.path.join(self.root_path, '%s.values.csv' % cname)), delimiter=';') 
          } for cname in coded_values
        }

        # Index all datasets per branch
        per_school = {}
        for fname in csvs:
            table = csv.DictReader(file(os.path.join(self.root_path, '%s.csv' % fname)), delimiter=';')
            # .fields.csv files have header `field;description;format;key`
            fields = csv.DictReader(file(os.path.join(self.root_path, '%s.fields.csv' % fname)), delimiter=';')
            fields = { f.pop('field').lower() : f for f in fields }
            keys = [n for n,f in fields.items() if f['key']]

            # Every row has a brin and branch id
            for t in table:
                branch = ( t.pop('brin'), int(t.pop('vestnr')) )
                if branch not in per_school:
                    per_school[branch] = {}
                if fname not in per_school[branch]:
                    per_school[branch][fname] = []

                # take the key fields seperately
                per_key = { fname: {} }
                for k,v in t.items():
                    k = k.lower()
                    v = unicode(v.strip().decode('cp1252'))
                    if v:
                        # Typecast this variable given the format
                        if fields[k]['format'] in formats:
                            v = formats[fields[k]['format']](v)

                        # Uncode this variable given the var name
                        var_code = k.split('_')[0]
                        if var_code in coded_values:
                            if v in coded_values[var_code]:
                                v = coded_values[var_code][v]
                            else:
                                print v, 'not in ', var_code, 'for', fname

                        # Add the keyed variables directly
                        if fields[k]['key']:
                            per_key[k] = v
                        else:
                            per_key[fname][k] = v

                # If it's just per branch, add it directly
                if len(keys) > 2:
                    per_school[branch][fname].append(per_key)
                else:
                    per_school[branch][fname] = per_key[fname]

        for (brin, branch_id), per_school in per_school.iteritems():
            school = DANSVoBranch(brin=brin, branch_id=branch_id)
            for fname in per_school:
                school[fname] = per_school[fname]
            yield school

