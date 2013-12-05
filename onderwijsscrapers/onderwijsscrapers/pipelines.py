from datetime import datetime
import pytz


from scrapy.conf import settings
from scrapy.exceptions import DropItem
from scrapy import log

# from onderwijsscrapers import exporters
from onderwijsscrapers.item_enrichment import bag42_geocode
from onderwijsscrapers.validation import validate


class OnderwijsscrapersPipeline(object):
    def __init__(self):
        self.scrape_started = datetime.utcnow().replace(tzinfo=pytz.utc)\
            .strftime('%Y-%m-%dT%H:%M:%SZ')
        self.items = {}
        self.universal_items = {}

    def process_item(self, item, spider):
        # Check if the fields that identify the item are present. If not,
        # log and drop the item.
        id_fields = settings['EXPORT_SETTINGS'][spider.name]['id_fields']
        if not all(field in item for field in id_fields):
            log.msg('Dropped item, not all required fields are present. %s'
                % item, level=log.WARNING, spider=spider)
            raise DropItem
            return

        item_id = '-'.join([str(item[field]) for field in id_fields])
        print '=' * 10
        print item_id

        if item_id not in self.items:
            self.items[item_id] = dict(item)
        else:
            self.items[item_id].update(dict(item))

        # Check if this item should be included into all related items
        # of the same spider (e.g. ignore reference year)
        universal_item = False
        if 'ignore_id_fields' in item:
            for field in item['ignore_id_fields']:
                item[field] = None

            del item['ignore_id_fields']
            universal_item = True

        item_id = '-'.join([str(item[field]) for field in id_fields])
        if universal_item:
            self.universal_items[item_id] = dict(item).copy()

        return item

    def close_spider(self, spider):
        export_settings = settings['EXPORT_SETTINGS'][spider.name]

        items = {}
        validation_reports = []

        # Add metadata to items and (if required) merge universal items.
        # Also validate and perform 'item_enrichment' functions
        # (i.e. geocodeing).
        id_fields = export_settings['id_fields']
        total_items = len(self.items.keys())
        count = 0
        for item_id, item in self.items.iteritems():
            universal_item = 'None-%s' % '-'.join([str(item[field]) for field in
                                                   id_fields[1:]])
            if universal_item in self.universal_items:
                universal_item = self.universal_items[universal_item]
                if 'reference_year' in universal_item:
                    del universal_item['reference_year']
                item.update(universal_item)

            if 'ignore_id_fields' in item:
                del item['ignore_id_fields']

            item['meta'] = {
                'scrape_started_at': self.scrape_started,
                'item_scraped_at': datetime.utcnow().replace(tzinfo=pytz.utc)
                                                    .strftime('%Y-%m-%dT%H:%M:%SZ')
            }

            # Geocode if enabled for this index
            if export_settings['geocode']:
                count += 1
                for address_field in export_settings['geocode_fields']:
                    if address_field in item:
                        geocoded = bag42_geocode(item[address_field])
                        if geocoded:
                            item[address_field].update(geocoded)
                log.msg('Geocoded %d/%d' % (count, total_items), level=log.INFO)

            # Validate the item is this is enabled
            if export_settings['validate']:
                item, validation = validate(export_settings['schema'],
                                            export_settings['index'],
                                            export_settings['doctype'],
                                            item_id, item)

                validation_reports.append(validation)

            items[item_id] = item

        for method, method_properties in settings['EXPORT_METHODS'].items():
            # Export the document
            exporter = method_properties['exporter'](self.scrape_started,
                                                     export_settings['index'],
                                                     export_settings['doctype'],
                                                     **method_properties['options'])

            for item_id, item in items.iteritems():
                exporter.save(item, item_id)

            exporter.close()

            # Export validation documents
            if export_settings['validate']:
                exporter = method_properties['exporter'](self.scrape_started,
                                                         export_settings['validation_index'],
                                                         'doc_validation',
                                                         **method_properties['options'])

                for item in validation_reports:
                    exporter.save(item)

                exporter.close()
