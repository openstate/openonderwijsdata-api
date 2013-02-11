import os
import json
from uuid import uuid1
from datetime import datetime

import pytz
import rawes
from colander import Invalid


class Exporter(object):
    def __init__(self, scrape_started_at, spider, config):
        self.scrape_started_at = scrape_started_at
        self.spider = spider
        self.config = config

    def validate(self, schema, validation_index, doc_id, item):
        validated_at = datetime.utcnow().replace(tzinfo=pytz.utc)\
            .strftime('%Y-%m-%dT%H:%M:%SZ')
        validation = {
            'index': self.index,
            'doc_type': self.doctype,
            'doc_id': doc_id,
            'scrape_started_at': self.scrape_started_at,
            'item_scraped_at': item['meta']['item_scraped_at'],
            'validated_at': validated_at,
            'result': 'invalid'
        }

        item['meta']['validated_at'] = validated_at
        item['meta']['validation_result'] = 'invalid'

        messages = []
        # Dirty 'hack' to validate the item with sorted keys. This is
        # done to keep references to keys in sync between the validation
        # result and the scraped item.
        item_sorted = json.dumps(item, sort_keys=True)
        item_sorted = json.loads(item_sorted)
        try:
            validation_schema = schema()
            validation_schema.deserialize(item_sorted)
        except Invalid, e:
            messages = map(lambda item: dict(field=item[0], message=item[1]),
                e.asdict().items())
        else:
            validation['result'] = 'valid'
            item['meta']['validation_result'] = 'valid'

        validation['messages'] = messages

        self._save(validation_index, 'doc_validation', validation)

        return item

    def _save(self, index, doc_type, item, doc_id=None):
        raise NotImplemented

    def save(self, doc_id, item):
        if self.config['validate']:
            item = self.validate(self.config['schema'],
                self.config['validation_index'], doc_id, item)

        self._save(self.index, self.doctype, item, doc_id)


class ElasticSearchExporter(Exporter):
    def __init__(self, scrape_started_at, spider, config, url, index, doctype):
        super(ElasticSearchExporter, self).__init__(scrape_started_at, spider,
            config)

        self.index = index
        self.doctype = doctype

        self.es = rawes.Elastic(url)

    def _save(self, index, doc_type, item, doc_id=None):
        if doc_id:
            url = '%s/%s/%s' % (index, doc_type, doc_id)
        else:
            url = '%s/%s' % (index, doc_type)

        self.es.put(url, data=json.dumps(item, sort_keys=True))


class FileExporter(Exporter):
    def __init__(self, scrape_started_at, spider, config, url, index, doctype,
        path):
        super(FileExporter, self).__init__(scrape_started_at, spider, config)

        if not os.path.exists(path):
            os.makedirs(path)

        self.path = path
        self.index = index
        self.doctype = doctype

    def _save(self, index, doc_type, item, doc_id=None):
        if doc_id:
            fname = '%s.json' % doc_id
        else:
            fname = '%s.json' % uuid1()

        f = open(os.path.join(self.path, fname), 'w')
        json.dump(item, f, indent=4, separators=(',', ': '), sort_keys=True)
        f.close()
