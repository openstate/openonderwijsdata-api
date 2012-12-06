import os
import json

import rawes

from scrapy.conf import settings


class ElasticSearchExporter(object):
    def __init__(self, url=settings['ES_URL'], index=settings['ES_INDEX'],
                 doctype=settings['ES_DOCTYPE']):
        self.index = index
        self.doctype = doctype

        self.es = rawes.Elastic(url)

    def save(self, doc_id, item):
        self.es.put('%s/%s/%s' % (self.index, self.doctype, doc_id), data=item)


class FileExporter(object):
    def __init__(self, path=settings['FILE_PATH']):
        self.path = path

    def save(self, doc_id, item):
        f = open(os.path.join(self.path, '%s.json' % doc_id), 'w')
        json.dump(dict(item), f)
        f.close()
