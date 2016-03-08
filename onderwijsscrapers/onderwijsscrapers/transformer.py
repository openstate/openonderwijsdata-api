"""
A Transformer is a Dataprotocols JSON Table Schema with a transformation definition.
http://dataprotocols.org/json-table-schema/#field-descriptors

The `source` field descriptor property is a regex that matches the source field name.
The `pattern` field descriptor property is a regex that matches the source value.

TODO: Should an `engine` property specifies the regex engine?
https://en.wikipedia.org/wiki/Comparison_of_regular_expression_engines
Or can we get by with semi-compatible regexes (e.g. no backreferences)
"""

from collections import defaultdict
import re
from jsontableschema.model import SchemaModel
from jsontableschema.exceptions import InvalidCastError

class Transformer(SchemaModel):
    def __init__(self, *args, **kwargs):
        self.set_metadata(kwargs.pop('metadata', {}))
        SchemaModel.__init__(self, *args, **kwargs)

    def set_metadata(self, metadata):
        # convert to unicode for casting
        self.metadata = {'meta:%s'%k:unicode(v) for k,v in metadata.items()}

    def fit(self, headers):
        headers = self.metadata.keys() + headers
        # Associate each head index with some fields and head-value matches
        self.fields_per_head = defaultdict(list)
        for column,head in enumerate(headers):
            for field in self.fields:
                if field.get('source_titles_match', None):
                    m = re.match(field['source_titles_match']+'$', head)
                    if m:
                        match = field['name'], tuple(m.groupdict().items())
                        self.fields_per_head[column].append(match)
        return self

    def transform(self, rows):
        for row in rows:
            for new_row in self.transform_row(row):
                yield new_row

    def transform_row(self, row):
        row = self.metadata.values() + row

        new_rows = defaultdict(dict)
        matched_patterns = defaultdict(dict)
        # parse fields
        for column, field_names in self.fields_per_head.iteritems():
            for (field_name, nesting) in field_names:
                # TODO: substitution instead of named capture
                pattern = self.get_field(field_name).get('source_values_match', None)
                if pattern:
                    m = re.match(pattern+'$', row[column])
                    if m:
                        matched_patterns[nesting].update(m.groupdict())
                    else:
                        # if the value doesn't match, discard it
                        break # TODO: logging
                try:
                    cast_val = self.cast(field_name, row[column])
                    new_rows[nesting][field_name] = cast_val
                except InvalidCastError as e:
                    pass # TODO: logging of malformed row
                except IndexError as e:
                    raise e
        # the row without nesting is the root
        root = new_rows.pop((), {})
        root.update(matched_patterns[()])
        if new_rows:
            # there's more left over after popping the root
            for nesting, new_row in new_rows.iteritems():
                new_row.update(root)
                new_row.update(dict(nesting))
                new_row.update(matched_patterns[nesting])
                yield new_row
        else:
            yield root
