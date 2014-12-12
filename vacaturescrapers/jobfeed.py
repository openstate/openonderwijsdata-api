import elasticsearch
import sys
import xml.etree.ElementTree as ET
from datetime import datetime

"""
Super quick 'n dirty shallow xml thing loader

TODO:
	lat/lon geo in ES
"""

es = elasticsearch.Elasticsearch([{'host': 'localhost'}])
index = 'jobfeed_%s'%datetime.now().strftime('%y%m%d')

print sys.argv[1]
tree = ET.parse(sys.argv[1])
root = tree.getroot()

for job in root:
	print 'Adding job (id=%s)' % job.find('id').text
	body = {}
	for f in job:
		text = f.text
		if text is not None:
			if any(s in f.tag for s in ['_id','_min','_max']) or f.tag=='sic':
				text = int(text)
			if f.tag in ['expired_at', 'date']:
				text = datetime.strptime( text, "%Y-%m-%d" )
			body[f.tag] = text
	# print body
	es.index(index=index, doc_type='job', body=body)

esi = elasticsearch.client.IndicesClient(es)
if esi.exists_alias(name='jobfeed'):
	esi.delete_alias(index='_all', name='jobfeed')
esi.put_alias(index=index, name='jobfeed')