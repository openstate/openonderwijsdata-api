import yaml
import os
with open(os.path.join(os.path.dirname(__file__), "config.yaml"), 'r') as f:
    config = yaml.load(f)

ES_URL = os.getenv('ES_URL', config['elasticsearch']['host'])
ES_INDEXES = set(config['elasticsearch']['indexes'])
ES_DOCUMENT_TYPES_PER_INDEX = {}
for i in ES_INDEXES:
    ES_DOCUMENT_TYPES_PER_INDEX[i] = set(config['elasticsearch']['types_per_index'][i])

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
