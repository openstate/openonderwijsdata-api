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

# Allow all settings to be overridden by a local file that is not in
# the VCS.
try:
    from local_settings import *
except ImportError:
    pass
