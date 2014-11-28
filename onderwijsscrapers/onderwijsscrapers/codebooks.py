from collections import namedtuple, defaultdict
import re
from colander import SchemaNode, Mapping, Sequence
import colander
"""
	A Codebook describes the data in a table.

    This module is still a proof-of-concept and needs major refactoring.
    The fields are now stored as a flat dict, but we'd like to move to
    a nested underlying representation.

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

def generate_unique_key(keyed_fields, name='UniqueKey'):
    class UniqueKey(namedtuple(name, list(keyed_fields))):
        """ A named tuple, with default None value  """
        def __new__(cls, **kwargs):
            kwargs = { f:kwargs.get(f, None) for f in keyed_fields }
            return super(UniqueKey, cls).__new__(cls, **kwargs)
        def items(self):
            return zip(self._fields, self)
    return UniqueKey

fields = ['type', 'source', 'keyed', 'pattern', 'repl', 'description']
Field = generate_unique_key(fields, name='Field')

class Codebook(dict):
    def __init__(self, name, field_dicts, datatypes):
        """
        Create a codebook from a list of fields.
        """
        self.name = name
        # Load the fields file
        for rule in field_dicts:
            name = rule.pop('field', None)
            if name:
                self[name] = Field(**rule)
        self.keyed_fields = set(name for name, f in self.items() if f.keyed)
        self.unique_key = generate_unique_key(self.keyed_fields)

        self.datatypes = datatypes

        # nested representation
        def add_to_nested(key, val, thedict, nest_stack):
            n = nest_stack.pop()
            per = '%s_per_%s'%(self.name, n)
            if per not in thedict:
                thedict[per] = { n: self[n] }
            if nest_stack:
                add_to_nested(key, val, thedict[per], nest_stack)
            else:
                thedict[per][key] = val

        sourced_keys = set(n for n,r in self.iteritems() if r.keyed and r.source)
        nest = {}
        for n,r in self.iteritems():
            if not r.keyed:
                t = sourced_keys|set(k for k in self.keyed_fields if '<%s>'%k in r.source)
                add_to_nested(n,r, nest, sorted(t, key=lambda k: -int(self[k].keyed) ))
        self.nest = nest

    def parse_table(self, heads, rows):
        """ Parse a table """
        UniqueKey = self.unique_key

        # Associate each head index with some fields and head-value matches
        unkeyed_per_head = defaultdict(list)
        keyed_per_head = defaultdict(list)
        for i,head in enumerate(heads):
            for fieldname, field in self.iteritems():
                if field.source:
                    m = re.match(field.source, head)
                    # add non-trivial matches
                    if m and fieldname:
                        if field.keyed:
                            keyed_per_head[i].append((fieldname, m.groupdict()))
                        else:
                            unkeyed_per_head[i].append((fieldname, m.groupdict()))

        def get_value(v, typ, sub1=None, sub2=None):
            """ Transform a value with a regex and type it """
            try:
                if sub1 is not None and sub2 is not None:
                    v = re.sub(sub1, sub2, v)
                yield self.datatypes[typ](v)
            except ValueError:
                return

        def fields_and_values(row, indexed_fields):
            """ Generate fields for this row and the associated values """
            for i, fields in indexed_fields.iteritems():
                for (field, groups) in fields:
                    # Every cell in this row can give us some fields,
                    # and nesting values that come from the heads themselves
                    for field_value in get_value(row[i], self[field].type):
                        nest_key = { name: nest_val
                            for name, nest_str in groups.iteritems()
                            for nest_val in get_value(nest_str, self[name].type)
                        }
                        yield field, field_value, nest_key

        # Group data by unique key
        dataset = defaultdict(dict)
        for row in rows:
            root_key = {}
            # fill root_key with keyed fields
            for field, value, nest_key in fields_and_values(row, keyed_per_head):
                # keyed fields shouldn't have groups
                root_key[field] = value

            # parse rest of fields
            for field, value, nest_key in fields_and_values(row, unkeyed_per_head):
                if nest_key:
                    nest_key.update(root_key)
                    dataset[UniqueKey(**nest_key)][field] = value
                else:
                    # add rooted
                    dataset[UniqueKey(**root_key)][field] = value
        

        def nested_set(dic, keys, value):
            for key in keys[:-1]:
                dic = dic.setdefault(key, {})
            dic[keys[-1]] = value

        def selectnest(items, header):
            """ Transform a list of dicts to a dist nested by `header` """
            # Basically nested named GROUP BY
            # https://github.com/mbostock/d3/wiki/Arrays#-nest
            h = header.pop(0)
            out = {}
            per = []
            if header: # recursive case
                collect = defaultdict(list)
                for i in items:
                    collect[i.pop(h)].append(i)
                for key, nested in collect.items():
                    i = selectnest(nested, list(header))
                    i_ = {}
                    for k,v in i.iteritems():
                        nested_set(i_, k.split('.'), v)
                    if key is None:
                        out.update(i_)
                    else:
                        i_[h] = key
                        per.append(i_)
            else: # base case
                for i in items:
                    i_ = {}
                    for k,v in i.iteritems():
                        nested_set(i_, k.split('.'), v)
                    if i_[h] is None: # add items to root
                        i_.pop(h)
                        out.update(i_)
                    else:
                        per.append(i_) # add items to the group list
            if per:
                out['%s_per_%s' % (self.name, h)] = per
            return out

        dataset = (dict(k.items() + v.items()) for k,v in dataset.iteritems())
        nesting_stack = sorted(self.keyed_fields, key=lambda k: int(self[k].keyed))
        return selectnest(dataset, nesting_stack)

    def add_to_validation(self, schema):
        """
        Add the validation for the fields to the parent schema object

        TODO: better id_fields filters
        """
        val_types = {
            'int': colander.Int(),
            'float': colander.Float()
        }
        def to_validator(nested, name):
            if type(nested) == Field:
                typ = val_types[nested.type] if nested.type in val_types else colander.String()
                node = SchemaNode(typ=typ, name=name, missing=None )
                node.type_doc = nested.type
                return node
            elif type(nested) == dict:
                seq = SchemaNode(typ=Sequence(), name = name)
                seq.type_doc = 'Array of %s'%name
                out = SchemaNode(typ=Mapping() , name = name)
                out.type_doc = name
                for k,v in nested.iteritems():
                    out.add(to_validator(v, k))
                seq.add(out)
                return seq
        
        # TODO: This only works for singleton id_fields
        groupby = schema.id_fields[0]
        for nest_name, nest in self.nest['%s_per_%s'%(self.name, groupby)].items():
            if nest_name != groupby:
                schema.add(to_validator(nest, nest_name))