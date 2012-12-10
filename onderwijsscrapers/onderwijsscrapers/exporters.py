from datetime import datetime
import os
import json

import time
import rawes


class ElasticSearchExporter(object):
    def __init__(self, url, index, doctype):
        self.index = index
        self.doctype = doctype

        self.es = rawes.Elastic(url)

    def save(self, doc_id, item):
        print '=' * 20
        print datetime.now()
        self.es.put('%s/%s/%s' % (self.index, self.doctype, doc_id), data=item)
        time.sleep(1)
        print datetime.now()


class FileExporter(object):
    def __init__(self, path):
        if not os.path.exists(path):
            os.makedirs(path)

        self.path = path

    def save(self, doc_id, item):
        f = open(os.path.join(self.path, '%s.json' % doc_id), 'w')
        json.dump(dict(item), f)
        f.close()
