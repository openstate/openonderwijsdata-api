import os
import json
import string
import tarfile
from uuid import uuid1

import rawes


class Exporter(object):
    def __init__(self, crawl_started_at, index, doctype):
        self.crawl_started_at = crawl_started_at
        self.index = index
        self.doctype = doctype

    def close(self):
        pass


class ElasticSearchExporter(Exporter):
    def __init__(self, crawl_started_at, index, doctype, url, index_suffix=None):
        super(ElasticSearchExporter, self).__init__(crawl_started_at, index,
            doctype)

        self.url = url
        self.es = rawes.Elastic(self.url)
        self.index_suffix = index_suffix

    def save(self, item, doc_id=None):
        if self.index_suffix is not None:
            suffix = '_' + self.index_suffix
        else:
            suffix = ''

        if doc_id:
            url = '%s%s/%s/%s' % (self.index, suffix, self.doctype, doc_id)
        else:
            url = '%s%s/%s/%s' % (self.index, suffix, self.doctype, uuid1())

        self.es.put(url, data=json.dumps(item, sort_keys=True))


class FileExporter(Exporter):
    def __init__(self, crawl_started_at, index, doctype, export_dir,
                 remove_json, create_tar):
        super(FileExporter, self).__init__(crawl_started_at, index,
            doctype)

        self.create_tar = create_tar
        if self.create_tar:
            stared_at_f = crawl_started_at.translate(string.maketrans('', ''),
                '-:')
            tar_name = '%s_%s_%s.tar.gz' % (index, doctype, stared_at_f)
            self.tar = tarfile.open(os.path.join(export_dir, tar_name),
                'w:gz')

        self.export_dir = os.path.join(export_dir, '%s_%s' % (index, doctype))

        if not os.path.exists(self.export_dir):
            os.makedirs(self.export_dir)

    def save(self, item, doc_id=None):
        if doc_id:
            f_name = '%s.json' % doc_id
        else:
            f_name = '%s.json' % uuid1()

        f_path = os.path.join(self.export_dir, f_name)
        f = open(f_path, 'w')
        json.dump(item, f, indent=4, separators=(',', ': '), sort_keys=True)
        f.close()

        if self.create_tar:
            self.tar.add(f_path, arcname=f_name)

    def close(self):
        if self.create_tar:
            self.tar.close()
