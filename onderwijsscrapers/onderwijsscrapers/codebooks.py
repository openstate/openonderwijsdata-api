from collections import namedtuple, defaultdict, OrderedDict
import csv
import re
import colander
from colander import SchemaNode
from groupnested import GroupNested

import os
def load_codebook(path, nested=False):
    path = os.path.join('codebooks', '%s.csv'%path)
    path = os.path.join(os.path.dirname(os.path.realpath(__file__)), path)
    if nested:
        return CodebookNested(csv.DictReader(open(path), delimiter=','))
    else:
        return Codebook(csv.DictReader(open(path), delimiter=','))

default_datatypes = {
    'int': (int, colander.Int()), 
    'float': (float, colander.Float()), 
    'string': (str, colander.String())
}
def generate_unique_key(keyed_fields, name='UniqueKey'):
    class UniqueKey(namedtuple(name, list(keyed_fields))):
        """ A named tuple, with default None value  """
        def __new__(cls, **kwargs):
            kwargs = { f:kwargs.get(f, None) for f in keyed_fields }
            return super(UniqueKey, cls).__new__(cls, **kwargs)
        def items(self):
            return zip(self._fields, self)
    return UniqueKey

class Field(generate_unique_key(['keyed','source','cast', 'typ', 'description'], 'Field')):
    __slots__ = ()
    def get_value(self, v):
        """ Transform a value with a regex and type it """
        try:
            # TODO: value transformations and lookups
            # if self.sub1 is not None and self.sub2 is not None:
            #     v = re.sub(self.sub1, self.sub2, v)
            yield self.cast(v.strip())
        except ValueError:
            return

class Codebook(dict):
    """
        Codebook
    """
    def __init__(self, field_dicts, datatypes=default_datatypes):
        # Load the fields file
        for rule in field_dicts:
            typ = rule.pop('type', 'string')
            if typ not in datatypes:
                typ = 'string'
            rule['cast'], rule['typ'] = datatypes[typ]
            try:
                rule['keyed'] = int(rule['keyed'])
            except ValueError:
                rule['keyed'] = None
            name = rule.pop('field', None)
            if name:
                self[name] = Field(**rule)

        self.root = generate_unique_key([n for n in self if self[n].keyed==0])

    def match_heads(self, heads):
        # Associate each head index with some fields and head-value matches
        keyed_per_head = defaultdict(list)
        unkeyed_per_head = defaultdict(list)
        unmatched_sources = set(f.source for f in self.values() if f.source)
        for i,head in enumerate(heads):
            for name, field in self.iteritems():
                if field.source:
                    m = re.match(field.source, head)
                    if m: # add non-trivial matches
                        if field.keyed != None:
                            keyed_per_head[i].append(name)
                        else:
                            unkeyed_per_head[i].append((name, m.groupdict()))
                        unmatched_sources.discard(field.source)
        if unmatched_sources:
            print 'unmatched', unmatched_sources

        return keyed_per_head, unkeyed_per_head

    def parse_row(self, row, keyed_per_head, unkeyed_per_head):
        key = {}
        root = {}
        # fill key with keyed fields
        for i, fieldnames in keyed_per_head.iteritems():
            for fieldname in fieldnames:
                for val in self[fieldname].get_value(row[i]):
                    if self[fieldname].keyed == 0:
                        root[fieldname] = val
                    else:
                        key[fieldname] = val
        # parse rest of fields
        for i, fieldnames in unkeyed_per_head.iteritems():
            for (fieldname, groups) in fieldnames:
                for val in self[fieldname].get_value(row[i]):
                    # add other fields to root or n
                    for name, nest_str in groups.iteritems():
                        for nest_val in self[name].get_value(nest_str):
                            if self[name].keyed == 0:
                                root[name] = nest_val
                            else:
                                key[name] = nest_val
                    yield root, key, {fieldname: val}

    def schema(self, root=False, **kwargs):
        """ Create Colander Schema """
        # TODO: mappings for mapping fields
        schema = SchemaNode(typ=colander.Mapping(), **kwargs)
        schema.__doc__ = schema.description
        for name,val in self.items():
            if val.keyed != 0 or root:
                schema.add(SchemaNode(
                    typ=val.typ, 
                    name=name, 
                    missing=colander.drop, 
                    title=val.description))
        seq = SchemaNode(typ=colander.Sequence(), **kwargs)
        seq.add(schema)
        return seq

    def parse(self, heads, rows):
        keyed_per_head, unkeyed_per_head = self.match_heads(heads)

        # store items with root-keys as key
        dataset = defaultdict(list)
        setkey = generate_unique_key([n for n in self if self[n].keyed>0])

        for row in rows:
            parse = self.parse_row(row, keyed_per_head, unkeyed_per_head)
            row_items = defaultdict(dict)
            for root, key, up in parse:
                row_items[(self.root(**root), setkey(**key))].update(up)
            for (root, key), item in row_items.iteritems():
                item.update(key._asdict())
                dataset[root].append(item)

        def deep_set(tree, stack, item):
            """ Use a list of keys to set a nested dict """
            for l in stack[:-1]:
                if l not in tree:
                    tree[l] = {}
                tree = tree[l]
            tree[stack[-1]] = item

        for key, data in dataset.iteritems():
            for d in data:
                for k,v in d.items():
                    if '.' in k:
                        d.pop(k)
                        deep_set(d, k.split('.'), v)
            yield dict(key._asdict()), data

        
class CodebookNested(Codebook):
    """
        Nested codebook

    """
    def __init__(self, field_dicts, datatypes=default_datatypes):
        Codebook.__init__(self, field_dicts, datatypes)

        # nested representation
        def nest(key, val, thedict, nest_stack):
            if nest_stack:
                n = nest_stack.pop()
                thedict.setdefault(n, {})
                nest(key, val, thedict[n], nest_stack)
            else:
                thedict[key] = val
        keyed_fields = set(name for name, f in self.items() if f.keyed)
        keys = set(n for n,r in self.items() if int(r.keyed or 0) and r.source)
        self.nested = {}
        for n,r in self.iteritems():
            if not r.keyed:
                # add to tree by root keys and nested keys
                # Don't allow hierarchical fields inside source
                nests = set(k for k in keys if '<%s>'%str(k) in r.source)
                stack = sorted(keys|nests, key=lambda k: -int(self[k].keyed))
                nest(n,r, self.nested, stack)

    def schema(self, root=False, **kwargs):
        def to_validator(val, name=''):
            if type(val) == Field:
                if val.description:
                    return SchemaNode(typ=val.typ, name=name, 
                        missing=colander.drop, title=val.description)
                else:
                    return SchemaNode(typ=val.typ, name=name, 
                        missing=colander.drop)
            elif type(val) == dict:
                seq = SchemaNode(typ=colander.Sequence(), name = 'per_%s'%name)
                out = SchemaNode(typ=colander.Mapping() , name = name)
                out.add(to_validator(self[name], name=name))
                tree = {}
                def add_tree(k):
                    """add mappings to `tree` with tuple key, return deepest"""
                    if k not in tree:
                        tree[k] = SchemaNode(typ=colander.Mapping(), name=k[-1])
                        if k[:-1]: # add nested
                            if k[:-1] not in tree:
                                add_tree(k[:-1])
                            tree[k[:-1]].add(tree[k]) # add schema to parent                        
                        else:
                            out.add(tree[k]) # add to root
                    return tree[k]
                for k,v in val.iteritems():
                    if type(k) == tuple and k:
                        node, name = add_tree(k[:-1]), k[-1]
                    else:
                        node, name = out, k
                    node.add(to_validator(v, name))
                seq.add(out)
                return seq

        schema = SchemaNode(typ=colander.Mapping(), **kwargs)
        schema.__doc__ = schema.description
        for k,v in self.nested.items():
            schema.add(to_validator(v,k))
        for name, field in self.items():
            if root and field.keyed == '0':
                schema.add(SchemaNode(typ=field.typ, name=name))
        return schema

    def parse(self, heads, rows):
        keyed_per_head, unkeyed_per_head = self.match_heads(heads)

        # Make nested dataset for grouping values
        def no_fields(nest):
            return {
                k:no_fields(v) if type(v)==dict else False
                for k,v in nest.iteritems()
            }
        def sortkey(k):
            return int(self[k[0]].keyed or 0)
        # store items with root-keys as key
        dataset = GroupNested({'root': no_fields(self.nested)})

        for row in rows:
            parse = self.parse_row(row, keyed_per_head, unkeyed_per_head)
            for root, key, up in parse:
                try:
                    root = [('root', self.root(**root))]
                except TypeError:
                    print 'ERROR: Wrong root structure for', self.root.__doc__
                    print '\t root = %s, key = %s'%(root, key)
                    raise SystemExit
                root += sorted(key.items(), key=sortkey)
                dataset[OrderedDict(root)].update(up)

        for key, data in dataset.store['root'].iteritems():
            yield dict(key._asdict()), data.struct()
