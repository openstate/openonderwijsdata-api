import json
from datetime import datetime

import pytz
from colander import Invalid

import inspect

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

def generate_documentation(schema, mappinglink = '%s'):
    """ Generate docs that describe the schema """
    name = schema.__name__ if inspect.isclass(schema) else schema.name
    doc = ''
    if schema.__doc__:
        doc += schema.__doc__ + '\n'

    tables = {}
    docs = {}

    # Build the table for this schema    
    table = 'Field,Type,Original term,Description\n'
    schema = schema() if inspect.isclass(schema) else schema
    for field in schema:
        orig = field.orig if hasattr(field, 'orig') else ''
        typ = type(field.typ).__name__
        typname = ''
        if typ == 'Sequence':
            field = [f for f in field][0] # should be only one
            typ = type(field.typ).__name__

            typname = 'array of '
            if typ != 'Mapping':
                typname += '%s (%s)' % (field.name, typ)
        if typ == 'Mapping':
            typname += mappinglink % field.__class__.__name__
            subdocs, subtables = generate_documentation(field.__class__, mappinglink=mappinglink)

            tables = dict(tables.items() + subtables.items())
            docs = dict(docs.items() + subdocs.items())

        if not typname:
            typname = typ.lower()

        table +=  '"%s"\n'% '","'.join([field.name, typname, orig, field.title])

    tables[name] = table
    docs[name] = doc

    return docs, tables
