from collections import namedtuple
"""
	A Codebook describes the data in a table.


	fields: dict<field object>
	field: object<source info>
	nesting stack

	field_rules (dict list): The rules for parsing the table
        Each rule has the properties:
            field: target name
            type: type of target
            source (optional): a regex for the source field
            keyed (optional): key level
            pattern (optional): regex that matches the value
            repl (optional): replacement for the regex, with back-references
            description, etc ...
"""

Field = namedtuple('Field', ['type', 'source', 'keyed', 'pattern', 'repl', 'description'])

class Codebook(dict):
    def __init__(self, field_dicts, datatypes):
        # Load the fields file
        for rule in field_dicts:
            name = rule.pop('field', None)
            if name:
                self[name] = Field(**rule)
        self.keyed_fields = set(name for name, f in self.items() if f.keyed)
        self.unique_key = generate_unique_key(self.keyed_fields)

        self.datatypes = datatypes

    def parse_table(self, heads, rows):
        """ Parse a table """
        UniqueKey = self.unique_key

        def get_value(v, typ, sub1=None, sub2=None):
            """ Transform a value with a regex and type it """
            try:
                if sub1 is not None and sub2 is not None:
                    v = re.sub(sub1, sub2, v)
                return self.datatypes[typ](v)
            except ValueError:
                return None

        def field_and_value_iter(row, indexed_fields):
            """ Generate fields for this row and the associated values """
            for i, fields in indexed_fields.iteritems():
                for (field, groups) in fields:
                    field_value = get_value(row[i], self[field].type)
                    if field_value is not None:
                        
                        nest_key = {}
                        for nest_name, nest_val in groups.iteritems():
                            nest_val = get_value(nest_val, self[nest_name].type)
                            if nest_val is not None:
                                nest_key[nest_name] = nest_val
                        
                        yield field, field_value, nest_key

        def collect_dataset(rows, (keyed_per_head, unkeyed_per_head)):
            """ Group data by unique key  """
            dataset = defaultdict(dict)
            for row in rows:
                root_key = {}
                # fill root_key with keyed fields
                for field, value, nest_key in field_and_value_iter(row, keyed_per_head):
                    # keyed fields shouldn't have groups
                    root_key[field] = value

                # parse rest of fields
                for field, value, nest_key in field_and_value_iter(row, unkeyed_per_head):
                    if nest_key:
                        nest_key = dict(root_key.items()+nest_key.items())
                        dataset[UniqueKey(**nest_key)][field] = value
                    else:
                        # add rooted
                        dataset[UniqueKey(**root_key)][field] = value
            return dataset

        return collect_dataset(rows, associate_heads(heads))




def generate_unique_key(keyed_fields):
    class UniqueKey(namedtuple('UniqueKey', list(keyed_fields))):
        """ A named tuple, with default None value  """
        def __new__(cls, **kwargs):
            kwargs = { f:kwargs.get(f, None) for f in keyed_fields }
            return super(UniqueKey, cls).__new__(cls, **kwargs)
        def items(self):
            return zip(self._fields, self)
    return UniqueKey