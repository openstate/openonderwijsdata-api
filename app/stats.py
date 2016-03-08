import rawes
import json
import os

from settings import (ES_URL, ES_INDEXES)

es = rawes.Elastic(ES_URL)

def get_fields(tree):
    if 'properties' in tree:
        for k,v in tree['properties'].iteritems():
            yield [k]
            for n in get_fields(v):
                yield [k] + n

def get_counts(index, doc_type, tree):
    """ Get the coverage of the fields per year for this index, doc type """
    search = '%s/%s/_search' % (index, doc_type)
    facet = {
        "years": {
            "terms": {
                "field": "reference_year", 
                "order": "term"
            }
        }
    }
    response = es.get(search, data={
        "facets": facet,
        "size": 0
    })['facets']['years']
    total = {None: response['total'] }
    percent = lambda year,count: int(float(count)/float(total[year])*100)

    row = {'total': total[None]}
    for year in response['terms']:
        total[year['term']]= year['count']
        row['count_%s'%year['term']]= year['count']
    yield None, row

    if total[None] > 0:
        for field in sorted(get_fields(tree)):
            field = '.'.join(field)
            response = es.get(search, data={
                "facets": facet,
                "query": {
                    "constant_score" : {
                        "filter" : {
                            "exists" : { "field" : field }
                        }
                    }
                },
                "size":0
            })['facets']['years']
            row = {
                'total': response['total'],
                'total_percent': percent(None, response['total'])
            }
            for year in response['terms']:
                row['count_%s'%year['term']]= year['count']
                row['percent_%s'%year['term']] = percent(year['term'], year['count'])
            yield field, row

def make_statsfile(index, doc_type, ftype):
    rows = []
    for maps in es.get('%s/%s/_mapping' % (index, doc_type)).values():
        for tree in maps['mappings'].values():
            rows = get_counts(index, doc_type, tree)
    rows = list(rows)
    if rows:
        if ftype == 'csv':
            import csv, StringIO
            header = frozenset(h for field, r in rows for h in r.keys() )
            header = ['field'] + sorted(list(header))
            f = StringIO.StringIO()
            w = csv.DictWriter(f, fieldnames=header)
            w.writeheader()
            for field, r in rows:
                r['field'] = field
                w.writerow(r)
            return f.getvalue()
        
        if ftype == 'json':
            import json
            from collections import OrderedDict
            return json.dumps(OrderedDict((f or 'total',r) for f,r in rows))



if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("-s", "--suffix", default=None,
                        help="index suffix")
    parser.add_argument("-i", "--index", default=None,
                        help="index")
    args = parser.parse_args()
    indexes = [args.index] if args.index else ES_INDEXES

    for index in indexes:
        if args.suffix:
            index = '%s_%s' % (index, args.suffix)
        print '==== %s ====' % index
        for maps in es.get('%s/_mapping' % index).values():
            for doc_type, tree in maps['mappings'].iteritems():
                print doc_type
                for field, row in get_counts(index, doc_type, tree):
                    print row.get('total_percent', None), field

