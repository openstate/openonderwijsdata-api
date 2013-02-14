from flask import Flask
from flask.ext import restful
from flask.ext.restful import abort, reqparse
import rawes
import re

app = Flask(__name__)
api = restful.Api(app)

ES_URL = 'localhost:9200'
ES_INDEXES = set(['duo', 'schoolvo', 'onderwijsinspectie'])
ES_DOCUMENT_TYPES_PER_INDEX = {
    'duo': set(['vo_school', 'vo_branch', 'vo_board']),
    'schoolvo': set(['vo_branch']),
    'onderwijsinspectie': set(['vo_branch'])
}
ES_DOCUMENT_TYPES = set()
for index, doctypes in ES_DOCUMENT_TYPES_PER_INDEX.iteritems():
    ES_DOCUMENT_TYPES = ES_DOCUMENT_TYPES | doctypes

es = rawes.Elastic(ES_URL)


@app.route('/')
def index():
    return 'test'


def format_es_single_doc(es_doc):
    return {
        '_type': es_doc['_type'],
        '_index': es_doc['_index'],
        '_id': es_doc['_id'],
        '_source': es_doc['_source']
    }


def format_es_search_results(es_results):
    return {
        'total': es_results['hits']['total'],
        'took': es_results['took'],
        'hits': es_results['hits']['hits'],
    }


class Search(restful.Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('q', type=str)
    parser.add_argument('brin', type=str)
    parser.add_argument('board_id', type=int)
    parser.add_argument('branch_id', type=int)
    parser.add_argument('zip_code', type=str)
    parser.add_argument('city', type=str)

    parser.add_argument('indexes', type=str, default=','.join(ES_INDEXES))
    parser.add_argument('doctypes', type=str,
        default=','.join(ES_DOCUMENT_TYPES))
    parser.add_argument('size', type=int, default=10)
    parser.add_argument('from', type=int, default=0)

    parser.add_argument('geo_sort', type=str)
    parser.add_argument('geo_filter', type=str)
    parser.add_argument('geo_filter_distance', type=str, default='10km')

    filters = {
        'brin': 'brin',
        'board_id': 'board_id',
        'branch_id': 'branch_id',
        'zip_code': 'address.zip_code',
        'city': 'address.city',
        'geo_filter_coords': 'address.geo_location'
    }

    def get(self):
        args = self.parser.parse_args()

        # Return an error if one of the indexes does not exist or if none
        # of the requested doctypes exist for the requested indexes.
        req_doctypes = set(args['doctypes'].split(','))
        existing_doctypes = []
        for index in args['indexes'].split(','):
            if index not in ES_INDEXES:
                abort(400, message='Index "%s" does not exist' % index)

            existing_doctypes.extend(ES_DOCUMENT_TYPES_PER_INDEX[index]\
                & req_doctypes)

        if not existing_doctypes:
            abort(400, message='The requested doctype(s) do not appear in the '
                'requested index(es)')

        # Return an error if none of the query parameters contains a value
        # (except for 'indexes' and 'doctypes', as these always contain
        # a value).
        no_args = True
        for arg, value in args.iteritems():
            if arg in ['indexes', 'doctypes']:
                continue

            if value:
                no_args = False

        if no_args:
            abort(400, message='No query or filter specified')

        # Validate the 'size' and 'from' arguments
        if args['size'] > 50 or args['size'] < 1:
            abort(400, message='Size must be between 1 and 50')

        query = {'query': {'filtered': {'query': {}}}}

        # FT query
        if args['q']:
            query['query']['filtered']['query']['query_string'] = {
                'fields': ['name^10', 'address.street', 'address.city',
                           'address.zip_code' 'municipality', 'wgr_area',
                           'rmc_region', 'rpa_area', 'province', 'corop_area',
                           'nodal_area', 'website'],
                'allow_leading_wildcard': False,
                'query': args['q']
            }
        else:
            query['query']['filtered']['query'] = {'match_all': {}}

        # Add filters to the query
        for arg, field in self.filters.iteritems():
            if args[arg] is None:
                continue

            if 'filter' not in query['query']['filtered']:
                query['query']['filtered']['filter'] = {'and': []}

            arg_value = args[arg]
            if type(arg_value) is str and arg != 'geo_filter_coords':
                arg_value = arg_value.lower().split(' ')

            if type(arg_value) is int:
                arg_value = [arg_value]

            if arg != 'geo_filter_coords':
                query['query']['filtered']['filter']['and'].append({
                    'terms': {
                        field: arg_value,
                        'execution': 'and'
                    }
                })
            else:
                coords = re.sub(r'\s{1,}', ' ', args[arg])
                query['query']['filtered']['filter']['and'].append({
                    'geo_distance': {
                        field: coords.strip(),
                        'distance': args['geo_filter_distance']
                    }
                })

        # Number of hits to return and the offset
        query['size'] = args['size']
        query['from'] = args['from']

        # Sort results based on distance to provided coordinate
        if args['geo_sort']:
            coords = re.sub(r'\s{1,}', ' ', args['geo_sort'])
            query['sort'] = {
                '_geo_distance': {
                    'address.geo_location': coords.strip(),
                    'order': 'asc',
                    'unit': 'km'
                }
            }

        print query

        return format_es_search_results(es.get('%s/%s/_search'
                % (args['indexes'], args['doctypes']), data=query))


class GetDocument(restful.Resource):
    def get(self, index, doc_type, doc_id):
        # Return an error if the requested index does not exist
        if index not in ES_INDEXES:
            abort(400, message='Index "%s" does not exist' % index)
        # Return an error if the requested doctype does not exist in the
        # requested index
        if doc_type not in ES_DOCUMENT_TYPES_PER_INDEX[index]:
            abort(400, message='Doctype "%s" does not exist in index "%s"'
                % (doc_type, index))

        doc = es.get('%s/%s/%s' % (index, doc_type, doc_id))
        if not doc['exists']:
            abort(404, message='The requested document does not exist')

        return format_es_single_doc(doc)


api.add_resource(Search, '/api/v1/search')
api.add_resource(GetDocument, '/api/v1/get_document/<index>/<doc_type>/<doc_id>')

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=5001)
