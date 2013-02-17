import json
from datetime import datetime

import pytz
from colander import Invalid


def validate(schema, index, doctype, doc_id, item):
    validated_at = datetime.utcnow().replace(tzinfo=pytz.utc)\
        .strftime('%Y-%m-%dT%H:%M:%SZ')

    validation = {
        'index': index,
        'doctype': doctype,
        'doc_id': doc_id,
        'scrape_started_at': item['meta']['scrape_started_at'],
        'item_scraped_at': item['meta']['item_scraped_at'],
        'validated_at': validated_at,
        'result': 'invalid'
    }

    item['meta']['validated_at'] = validated_at
    item['meta']['validation_result'] = 'invalid'

    messages = []
    # Dirty 'hack' to validate the item with sorted keys. This is
    # done to keep references to keys in sync between the validation
    # result document and the scraped item.
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

    return item, validation
