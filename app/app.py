from flask import Flask, render_template, request
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
ES_VALIDATION_RESULTS_INDEX = 'onderwijsdata_validation'

es = rawes.Elastic(ES_URL)


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


@app.route('/')
def index():
    counts = {}

    counts['schoolvo'] = es.get('schoolvo/_search', data={
        "facets": {
            "doc_types": {
                "terms": {"field": "_type"}
            }
        },
        "size": 0
    })

    counts['onderwijsinspectie'] = es.get('onderwijsinspectie/_search', data={
        "facets": {
            "doc_types": {
                "terms": {"field": "_type"}
            }
        },
        "size": 0
    })

    counts['duo_vo_schools'] = es.get('duo/vo_school/_search', data={
        "facets": {
            "years": {
                "terms": {"field": "reference_year", "order": "term"}
            }
        },
        "size": 0
    })

    counts['duo_vo_boards'] = es.get('duo/vo_board/_search', data={
        "facets": {
            "years": {
                "terms": {"field": "reference_year", "order": "term"}
            }
        },
        "size": 0
    })

    counts['duo_vo_branches'] = es.get('duo/vo_branch/_search', data={
        "facets": {
            "years": {
                "terms": {"field": "reference_year", "order": "term"}
            }
        },
        "size": 0
    })

    type_names = {
        'vo_board': 'Boards',
        'vo_school': 'Schools',
        'vo_branch': 'School Branches'
    }

    return render_template('index.html', counts=counts, type_names=type_names)


@app.route('/search')
def simple_search():
    query = {
        'query': {
            'query_string': {
                'fields': ['name^10', 'address.street', 'address.city',
                           'address.zip_code' 'municipality', 'wgr_area',
                           'rmc_region', 'rpa_area', 'province', 'corop_area',
                           'nodal_area', 'website', 'brin'],
                'allow_leading_wildcard': False,
                'query': request.args.get('q')
            }
        },
        'size': 20
    }

    es_results = es.get('%s/%s/_search' % (','.join(ES_INDEXES),
                                           ','.join(ES_DOCUMENT_TYPES)),
                        data=query)
    hits = format_es_search_results(es_results)

    return render_template('search.html', hits=hits)


class Search(restful.Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('q', type=str)
    parser.add_argument('brin', type=str)
    parser.add_argument('board_id', type=int)
    parser.add_argument('branch_id', type=int)
    parser.add_argument('zip_code', type=str)
    parser.add_argument('city', type=str)

    parser.add_argument('sort', type=str)
    parser.add_argument('order', type=str, default='asc')
    parser.add_argument('geo_location', type=str)
    parser.add_argument('geo_distance', type=str, default='10km')
    parser.add_argument('indexes', type=str, default=','.join(ES_INDEXES))
    parser.add_argument('doctypes', type=str,
                        default=','.join(ES_DOCUMENT_TYPES))
    parser.add_argument('size', type=int, default=10)
    parser.add_argument('from', type=int, default=0)

    filters = {
        'brin': 'brin',
        'board_id': 'board_id',
        'branch_id': 'branch_id',
        'zip_code': 'address.zip_code',
        'city': 'address.city',
        'geo_location': 'address.geo_location'
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

            existing_doctypes.extend(ES_DOCUMENT_TYPES_PER_INDEX[index]
                                     & req_doctypes)

        if not existing_doctypes:
            abort(400, message='The requested doctype(s) do not appear in the '
                               'requested index(es)')

        # Return an error if none of the query parameters contains a value
        # (except for 'indexes' and 'doctypes', as these always contain
        # a value).
        no_args = True
        for arg, value in args.iteritems():
            if arg in ['indexes', 'doctypes', 'geo_distance', 'order', 'size',
                       'from']:
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

        # Format coordinates if necessary
        if args['geo_location']:
            args['geo_location'] = re.sub(r'\s{1,}', ' ', args['geo_location'])

        # Add filters to the query
        for arg, field in self.filters.iteritems():
            if args[arg] is None:
                continue

            if 'filter' not in query['query']['filtered']:
                query['query']['filtered']['filter'] = {'and': []}

            arg_value = args[arg]
            if type(arg_value) is str and arg != 'geo_location':
                arg_value = arg_value.lower().split(' ')

            if type(arg_value) is int:
                arg_value = [arg_value]

            if arg != 'geo_location':
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
                        field: coords,
                        'distance': args['geo_distance']
                    }
                })

        # Number of hits to return and the offset
        query['size'] = args['size']
        query['from'] = args['from']

        # Sort results
        if args['order'] not in ['asc', 'desc']:
            abort(400, message='Order can only be "asc" or "desc"')

        if args['sort']:
            if args['sort'] == 'distance':
                if not args['geo_location']:
                    abort(400, message='Cannot sort by distance if '
                                       'geo_location is not provided.')

                query['sort'] = [{
                    '_geo_distance': {
                        'address.geo_location': args['geo_location'],
                        'order': args['order'],
                        'unit': 'km'
                    }
                }]
            else:
                query['sort'] = [
                    {args['sort']: {'order': args['order']}}
                ]

        return format_es_search_results(es.get('%s/%s/_search'
                                               % (args['indexes'],
                                                  args['doctypes']),
                                               data=query))


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


class GetValidationResults(restful.Resource):
    def get(self, index, doc_type, doc_id):
        # Return an error if the requested index does not exist
        if index not in ES_INDEXES:
            abort(400, message='Index "%s" does not exist' % index)

        # Return an error if the requested doctype does not exist in the
        # requested index
        if doc_type not in ES_DOCUMENT_TYPES_PER_INDEX[index]:
            abort(400, message='Doctype "%s" does not exist in index "%s"'
                               % (doc_type, index))

        query = {
            'query': {
                'filtered': {
                    'query': {'match_all': {}},
                    'filter': {
                        'and': [
                            {'terms': {'index': index}},
                            {'terms': {'doc_type': doc_type}},
                            {'terms': {'doc_id': doc_id}}
                        ]
                    }
                }
            }
        }
        print query
        return es.get('%s/_search' % (ES_VALIDATION_RESULTS_INDEX), data=query)

api.add_resource(Search, '/api/v1/search')
api.add_resource(GetDocument, '/api/v1/get_document/<index>/<doc_type>/<doc_id>')
api.add_resource(GetValidationResults, '/api/v1/get_validation_results/'
                                       '<index>/<doc_type>/<doc_id>')


if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=5001)
