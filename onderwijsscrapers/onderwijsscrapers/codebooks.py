from collections import namedtuple, defaultdict, OrderedDict
import csv, re
import colander
from colander import SchemaNode

import os
def load_codebook(path):
    path = os.path.join('codebooks', '%s.csv'%path)
    path = os.path.join(os.path.dirname(os.path.realpath(__file__)), path)
    return Codebook(csv.DictReader(open(path), delimiter=','))

default_datatypes = {
    'int': (int, colander.Int()), 
    'float': (float, colander.Float()), 
    'string': (str, colander.String())
}
class Field(namedtuple('Field', ['keyed','source','cast', 'typ', 'description'])):
    __slots__ = ()
    def get_value(self, v):
        """ Transform a value with a regex and type it """
        try:
            # TODO: value transformations and lookups
            # if self.sub1 is not None and self.sub2 is not None:
            #     v = re.sub(self.sub1, self.sub2, v)
            yield self.cast(v)
        except ValueError:
            return

class Codebook(dict):
    def __init__(self, field_dicts, datatypes=default_datatypes):
        # Load the fields file
        for rule in field_dicts:
            typ = rule.pop('type', 'string')
            if typ not in datatypes:
                typ = 'string'
            rule['cast'], rule['typ'] = datatypes[typ]
            name = rule.pop('field', None)
            if '.' in name:
                # Allow hierarchical fields
                name = tuple(name.split('.'))
            if name:
                self[name] = Field(**rule)

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

        self.root = namedtuple('Root', [n for n in self if self[n].keyed=='0'])

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
        # Associate each head index with some fields and head-value matches
        keyed_per_head = defaultdict(list)
        unkeyed_per_head = defaultdict(list)
        for i,head in enumerate(heads):
            for name, field in self.iteritems():
                if field.source:
                    m = re.match(field.source, head)
                    if m: # add non-trivial matches
                        if field.keyed:
                            keyed_per_head[i].append(name)
                        else:
                            unkeyed_per_head[i].append((name, m.groupdict()))

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

        

    def parse_row(self, row, keyed_per_head, unkeyed_per_head):
        key = {}
        root = {}
        # fill key with keyed fields
        for i, fieldnames in keyed_per_head.iteritems():
            for fieldname in fieldnames:
                for val in self[fieldname].get_value(row[i]):
                    if self[fieldname].keyed == '0':
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
                            if self[name].keyed == '0':
                                root[name] = nest_val
                            else:
                                key[name] = nest_val
                    yield root, key, {fieldname: val}

if __name__ == '__main__':
    import sys, StringIO

    def print_schema(sch, n=0):
        print ' '*n, sch.name, '(%s)' % type(sch.typ).__name__
        for s in sch:
            if type(sch.typ).__name__ in ['Mapping', 'Sequence']:
                print_schema(s, n+1)

    if len(sys.argv)>1:
        cb = load_codebook(sys.argv[1])
        print cb
        print_schema(cb.schema(root=True))
        from tabular_utilities import get_tables
        from os.path import splitext
        root, ext = splitext(sys.argv[2])
        filt = [sys.argv[3]] if len(sys.argv)>3 else None
        for table in get_tables(open(sys.argv[2]), ext, filt=filt):
            rows = table.rows()
            head = next(rows)
            key, val = next(cb.parse(head, rows))
            print key
            print cb.schema(root=False).deserialize(val)
    else:

        book = """field;keyed;source;type;description
board_id;0;BEVOEGD GEZAG NUMMER;int;
vavo;;AANTAL LEERLINGEN;int;
"""
        table = """BEVOEGD GEZAG NUMMER;AANTAL LEERLINGEN
1;10
2;20
"""

        cb = Codebook(csv.DictReader(StringIO.StringIO(book), delimiter=';'))
        print cb
        print_schema(cb.schema(root=True))
        t = csv.reader(StringIO.StringIO(table), delimiter=';')
        for l in cb.parse(next(t), t):
            print l

        # artificial
        book = """field;keyed;source;type;description
board_id;0;BEVOEGD GEZAG NUMMER;int;
reference_year;0;JAAR;int;
student_year;1;LEERJAAR;int;
vavo;;AANTAL LEERLINGEN;int;
non_vavo;;NIET VAVO;int;
"""
        table = """BEVOEGD GEZAG NUMMER;JAAR;LEERJAAR;AANTAL LEERLINGEN;NIET VAVO
1;2014;1;10;40
2;2014;1;20;70
2;2014;2;4;34
"""
        cb = Codebook(csv.DictReader(StringIO.StringIO(book), delimiter=';'))
        print cb
        print_schema(cb.schema(root=True))
        t = csv.reader(StringIO.StringIO(table), delimiter=';')
        for l in cb.parse(next(t), t):
            print l

        
