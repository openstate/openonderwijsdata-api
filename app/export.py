from flask import make_response
from flask.ext import restful
from flask.ext.restful import abort, reqparse

import elasticsearch.helpers
from elasticsearch import Elasticsearch
import json
import csv
import io

from settings import (ES_URL, ES_INDEXES, ES_DOCUMENT_TYPES_PER_INDEX,
                      ES_DOCUMENT_TYPES, ES_VALIDATION_RESULTS_INDEX)



def iter_flattened_doc(root, branch, name_part, keys):
    """ Flatten a nested doc into rows """
    def name(k):
        return '.'.join([name_part,k]) if name_part else k
    row = dict(root) # copy row
    for k,v in branch.iteritems():
        if type(v) is not list and name(k) in keys:
            row[name(k)] = v.encode('utf-8') if type(v)==unicode else v
    has_nest = False
    for k,v in branch.iteritems():
        if type(v) is list:
            has_nest = True
            for i in v:
                for j in iter_flattened_doc(row, i, name(k), keys):
                    yield j
    if not has_nest:
        yield row

class ExportTable(restful.Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('fields', type=str)

    def get(self, filetype, index, doc_type):
        # Use elasticsearch python bindings
        es = Elasticsearch()

        # Return an error if the requested index does not exist
        if index not in ES_INDEXES:
            abort(400, message='Index "%s" does not exist' % index)

        # Return an error if the requested doctype does not exist in the
        # requested index
        if doc_type not in ES_DOCUMENT_TYPES_PER_INDEX[index]:
            abort(400, message='Doctype "%s" does not exist in index "%s"'
                               % (doc_type, index))

        # Make a CSV table
        args = self.parser.parse_args()
        keys = args['fields'].split(',') if args['fields'] else []
        query = {"query": { "match_all": {} } }
        query["_source"] = keys

        # get nested keys from mapping
        mapping = es.indices.get_mapping(index="duo",doc_type="vo_board")
        if mapping.keys():
            mapping = mapping[mapping.keys()[0]]['mappings'][doc_type]
            def maptree(t, nest):
                for n, prop in t['properties'].iteritems():
                    if 'properties' in prop:
                        for m in maptree(prop, nest+[n]):
                            yield m
                    else:
                        yield nest+[n]
            keys = ['.'.join(k) for k in maptree(mapping, []) 
                    if (k[0] in keys) or not keys]
        else:
            keys = []

        hits = list(elasticsearch.helpers.scan(es, index = index, 
            doc_type = doc_type, query=query))
        if not hits:
            abort(400, message='No documents of type "%s" in index "%s"'
                               % (doc_type, index))

        if filetype == 'json':
            tree = [hit['_source'] for hit in hits]
            response = make_response(json.dumps(tree))
            response.headers['content-type'] = 'application/json'
            return response
        elif filetype == 'csv':  
            output = io.BytesIO()
            dict_writer = csv.DictWriter(output, fieldnames=keys)
            dict_writer.writeheader()
            for hit in hits:
                for row in iter_flattened_doc({}, hit['_source'], '', set(keys)):
                    dict_writer.writerow(row)

            response = make_response(str(output.getvalue()))
            response.headers['content-type'] = 'text/csv'
            return response
        else:
            abort(400, message='Export filetype %s is not supported'%filetype)