from scrapy.conf import settings


class SchoolVOPipeline(object):
    def __init__(self):
        if settings['EXPORT_METHOD'] == 'elasticsearch':
            from schoolvenstersonline.exporters import ElasticSearchExporter
            self.export = ElasticSearchExporter()
        elif settings['EXPORT_METHOD'] == 'file':
            from schoolvenstersonline.exporters import FileExporter
            self.export = FileExporter()

    def process_item(self, item, spider):
        del item['available_indicators']

        self.export.save(item['schoolvo_code'], dict(item))
        return item
