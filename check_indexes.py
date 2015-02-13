import rawes
import json
import os

from app.settings import (ES_URL, ES_INDEXES)

es = rawes.Elastic(ES_URL)

def get_fields(tree):
    if 'properties' in tree:
        for k,v in tree['properties'].iteritems():
            yield [k]
            for n in get_fields(v):
                yield [k] + n

for index in ES_INDEXES:
    print '==== %s ====' % index
    for maps in es.get('%s/_mapping' % index).values():
        for doc_type, tree in maps['mappings'].iteritems():
            count = es.get('%s/%s/_search' % (index, doc_type), data={
                    "query": { "match_all": {} },
                    "size": 0
                })['hits']['total']
            print count, doc_type

            if count > 0:
                indent = len(str(count))
                for field in get_fields(tree):
                    missing = es.get('%s/%s/_search' % (index, doc_type), data={
                            "query": {
                                "constant_score" : {
                                    "filter" : {
                                        "missing" : { "field" : '.'.join(field) }
                                    }
                                }
                            },
                            "size":0
                        })['hits']['total']
                    percent = int(float(missing)/float(count)*100)
                    print ' %s%%' % percent,
                    print (len(str(percent))-indent)*' ', len(field)*'\t','\t', 
                    print '.'.join(field)

            print ''

