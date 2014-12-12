import elasticsearch
import sys
import xml.etree.ElementTree as ET
from datetime import datetime

"""
Super quick 'n dirty shallow xml thing loader
"""

es = elasticsearch.Elasticsearch([{'host': 'localhost'}])
def add(doc):
	index = 'jobfeed_%s'%datetime.now().strftime('%y%m%d')
	es.index(index=index, doc_type='job', body=doc)

print sys.argv[1]
tree = ET.parse(sys.argv[1])
root = tree.getroot()

for job in root:
	print 'Adding job (id=%s)' % job.find('id').text
	# add({f.tag: f.text for f in job})