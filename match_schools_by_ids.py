import rawes

es = rawes.Elastic('chimay.dispectu.com:9200')


def get_all_docs(index):
    docs = es.get('%s/_search' % index, data={
        'size': 5000,
        'query': {
            'match_all': {}
        }
    })

    return docs['hits']['hits']

available_indexes = ['duo', 'onderwijsinspectie', 'schoolvo']

brin_vestiging_per_index = {}
missing_ids = []

for index in available_indexes:
    docs = get_all_docs(index)

    brin_vestiging_per_index[index] = set()
    for doc in docs:

        if index in ['duo', 'onderwijsinspectie']:
            doc_id = '%s-%s' % (doc['_source']['brin'], doc['_source']['branch_id'])

        if index == 'schoolvo':
            schoolvo_code = doc['_source']['schoolvo_code'].split('-')
            doc_id = '%s-%s' % (schoolvo_code[1], int(schoolvo_code[2]))

        brin_vestiging_per_index[index].add(doc_id)
