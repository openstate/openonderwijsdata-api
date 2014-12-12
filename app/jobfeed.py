from flask import Flask, render_template, request
from flask.ext import restful
from flask.ext.restful import abort, reqparse
import rawes
from settings import (ES_URL)

es = rawes.Elastic(ES_URL)


class JobSearch(restful.Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('q', type=str)

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

    def get(self):
        args = self.parser.parse_args()

        args['indexes'] = 'jobfeed'
        args['doctypes'] = 'job'

        query = {'query': {'filtered': {'query': {}}}}
        if args['q']:
            query['query']['filtered']['query']['query_string'] = {
                'fields': self.text_fields,
                'allow_leading_wildcard': False,
                'query': args['q']
            }
        else:
            query['query']['filtered']['query'] = {'match_all': {}}

        return es.get('%s/%s/_search'
           % (args['indexes'],
              args['doctypes']),
           data=query)

class JobFeed():
    def __init__(self, api):
        api.add_resource(JobSearch, '/api/v2/job_search')
