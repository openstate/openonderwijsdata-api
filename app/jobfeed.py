from flask import Flask, render_template, request
from flask.ext import restful
from flask.ext.restful import abort, reqparse
import rawes
from settings import (ES_URL)

es = rawes.Elastic(ES_URL)

ES_INDEXES = ['jobfeed']
ES_DOCUMENT_TYPES_PER_INDEX = {
    'jobfeed': ['job'],
}
ES_DOCUMENT_TYPES = [d for i in ES_DOCUMENT_TYPES_PER_INDEX.values() for d in i]

class JobSearch(restful.Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('q', type=str)
    parser.add_argument('size', type=int, default=10)
    parser.add_argument('from', type=int, default=0)
    parser.add_argument('sort', type=str)
    parser.add_argument('order', type=str, default='asc')


    text_fields = [
        "title",
        "organization_name",
        "employer_descr",
        "candidate_descr",
        "application_descr",
        "education_level",
        "fulltxt",
        "conditions_descr",
        "sic_descr",
        "job_descr",
        "jobfeed_profession",
        "jobfeed_profession_group",
        "jobfeed_profession_class",
        "job_location",
        "employment_type",
        "sector",
    ]
    num_fields = [
        "job_location_id",
        "jobfeed_profession_id",
        "jobfeed_profession_group_id",
        "jobfeed_profession_class_id",
        "source_type_id",
        "education_level_id",
        "employment_type_id",
        "contract_type_id",
        "working_hours_id",
        "hours_per_week_min",
        "hours_per_week_max",
        "salary_min",
        "salary_max",
        "experience_min",
        "experience_max",
        "sector_id",
        "org_size_id",
        "sic",
    ]
    for t in text_fields:
        parser.add_argument(t, type=str)
    for n in num_fields:
        parser.add_argument(n, type=int)

    def get(self):
        args = self.parser.parse_args()

        args['indexes'] = ','.join(ES_INDEXES)
        args['doctypes'] = ','.join(ES_DOCUMENT_TYPES)

        query = {'query': {'filtered': {'query': {}}}}
        if args['q']:
            query['query']['filtered']['query']['query_string'] = {
                'fields': self.text_fields,
                'allow_leading_wildcard': False,
                'query': args['q']
            }
        else:
            query['query']['filtered']['query'] = {'match_all': {}}

        for arg in (self.text_fields + self.num_fields):
            if args[arg] is None:
                continue

            if 'filter' not in query['query']['filtered']:
                query['query']['filtered']['filter'] = {'and': []}

            arg_value = args[arg]
            if type(arg_value) is str:
                arg_value = arg_value.lower().split(' ')
            if type(arg_value) is int:
                arg_value = [arg_value]

            query['query']['filtered']['filter']['and'].append({
                'terms': {
                    arg: arg_value,
                    'execution': 'and'
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

        return es.get('%s/%s/_search'
           % (args['indexes'],
              args['doctypes']),
           data=query)

class JobDoc(restful.Resource):
    def get(self, index, doc_type, doc_id):
        # Return an error if the requested index does not exist
        if index not in ES_INDEXES:
            abort(400, message='Index "%s" does not exist' % index)

        # Return an error if the requested doctype does not exist in the
        # requested index
        if doc_type not in ES_DOCUMENT_TYPES_PER_INDEX[index]:
            abort(400, message='Doctype "%s" does not exist in index "%s"'
                               % (doc_type, index))
 
        try:
            doc = es.get('%s/%s/%s' % (index, doc_type, doc_id))
        except rawes.elastic_exception.ElasticException, error:
            if error.status_code == 404:
                abort(404, message='The requested document does not exist')
            else:
                print(error)

        return doc

class JobFeed():
    def __init__(self, api):
        api.add_resource(JobSearch, '/api/v2/job_search')
        api.add_resource(JobDoc, '/api/v2/job_doc/<index>/<doc_type>/<doc_id>')
