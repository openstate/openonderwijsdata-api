import elasticsearch
import sys
import xml.etree.ElementTree as ET
from xml.etree.ElementTree import iterparse
from datetime import datetime
from itertools import islice

"""
Super quick 'n dirty shallow xml thing loader

TODO:
	lat/lon geo in ES
"""

es = elasticsearch.Elasticsearch([{'host': 'localhost'}])
index = 'jobfeed_%s'%datetime.now().strftime('%y%m%d')

print sys.argv[1]
# jobs = ET.parse(sys.argv[1]).getroot() # whole file parsing
jobs = (e for _, e in iterparse(sys.argv[1]) if e.tag == 'job')

for job in islice(jobs, None):
	print 'Adding job (id=%s)' % job.find('id').text
	body = {}
	for f in job:
		text = f.text
		if text is not None:
			try:
				if any(s in f.tag for s in ['possible_startersjob']):
					text = bool(text)
				if any(s in f.tag for s in ['_id','_min','_max']) or f.tag=='sic':
					text = int(float(text))
				if f.tag in ['expired_at', 'date']:
					text = datetime.strptime( text, "%Y-%m-%d" )
				body[f.tag] = text
			except:
				pass
			
	es.index(index=index, doc_type='job', body=body)

esi = elasticsearch.client.IndicesClient(es)
if esi.exists_alias(name='jobfeed'):
	esi.delete_alias(index='_all', name='jobfeed')
esi.put_alias(index=index, name='jobfeed')