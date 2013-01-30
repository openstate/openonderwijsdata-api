import os
import uuid
from scrapy.conf import settings
from onderwijsscrapers import exporters
from onderwijsscrapers import items


class OnderwijsscrapersPipeline(object):
    def __init__(self):
        self.exporters = {}

    def process_item(self, item, spider):
        # Initialize the required exporter if necessary
        if spider.name not in self.exporters:
            if settings['EXPORT_METHOD'] == 'elasticsearch':
                essetup = settings['ELASTIC_SEARCH'][spider.name]
                self.exporters[spider.name] = exporters.ElasticSearchExporter(
                    essetup['url'], essetup['index'], essetup['doctype'])
            elif settings['EXPORT_METHOD'] == 'file':
                self.exporters[spider.name] = exporters.FileExporter(
                    os.path.join(settings['EXPORT_DIR'], spider.name))

        if isinstance(item, items.SchoolVOItem):
            del item['available_indicators']
            doc_id = item['schoolvo_code']

        if isinstance(item, items.OnderwijsInspectieItem):
            doc_id = str(uuid.uuid1())

        if isinstance(item, items.DUOSchoolItem):
            if 'brin' not in item:
                print '*' * 200
                return item
            doc_id = '%s-%s' % (item['brin'], item['branch_id'])

        self.exporters[spider.name].save(doc_id, dict(item))

        return item
