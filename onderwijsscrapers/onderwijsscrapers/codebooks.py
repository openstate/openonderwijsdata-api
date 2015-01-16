from collections import namedtuple, defaultdict
import csv, StringIO
import colander
import re

default_datatypes = {
    'int': (int, colander.Int()), 
    'float': (float, colander.Float()), 
    'string': (str, colander.String())
}
class Field(namedtuple('Field', ['keyed','source','cast', 'typ'])):
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
            rule['cast'], rule['typ'] = datatypes[rule.pop('type', 'string')]
            name = rule.pop('field', None)
            if name:
                self[name] = Field(**rule)

    def schema(self, root=False, **kwargs):
        schema = colander.SchemaNode(typ=colander.Mapping(), **kwargs)
        schema.__doc__ = schema.description
        for name, field in self.items():
            if root or field.keyed != '0':
                schema.add(colander.SchemaNode(typ=field.typ, name=name, missing=None ))
        return schema

    def parse(self, heads, rows):
        # Associate each head index with some fields and head-value matches
        keyed_per_head = defaultdict(list)
        unkeyed_per_head = defaultdict(list)
        for i,head in enumerate(heads):
            for fieldname, field in self.iteritems():
                if field.source:
                    m = re.match(field.source, head)
                    if m: # add non-trivial matches
                        if field.keyed:
                            keyed_per_head[i].append(fieldname)
                        else:
                            unkeyed_per_head[i].append((fieldname, m.groupdict()))

        for row in rows:
            yield self.parse_row(row, keyed_per_head, unkeyed_per_head)


    def parse_row(self, row, keyed_per_head, unkeyed_per_head):
        key = {}
        # fill key with keyed fields
        for i, fieldnames in keyed_per_head.iteritems():
            for fieldname in fieldnames:
                for val in self[fieldname].get_value(row[i]):
                    key[fieldname] = val
        # parse rest of fields
        for i, fieldnames in unkeyed_per_head.iteritems():
            for (fieldname, groups) in fieldnames:
                for val in self[fieldname].get_value(row[i]):
                    nest_key = { name: nest_val
                        for name, nest_str in groups.iteritems()
                        for nest_val in self[name].get_value(nest_str)
                    }
                    if nest_key:
                        nest_key.update(key)
                        key = nest_key
                    return key, {fieldname: val}

if __name__ == '__main__':
    import sys
    book = """field;keyed;source;type
board_id;0;BEVOEGD GEZAG NUMMER;int
vavo;;AANTAL LEERLINGEN;int
"""

    table = """BEVOEGD GEZAG NUMMER;AANTAL LEERLINGEN
1;10
2;20
"""

    cb = CodebookMini(csv.DictReader(StringIO.StringIO(book), delimiter=';'))
    print cb

    print ''
    def print_schema(sch, n=0):
        print ' '*n, sch.name, '(%s)' % type(sch.typ).__name__
        for s in sch:
            if type(sch.typ).__name__ in ['Mapping', 'Sequence']:
                print_schema(s, n+1)
    
    print_schema(cb.schema(root=True))

    t = csv.reader(StringIO.StringIO(table), delimiter=';')
    for l in cb.parse(next(t), t):
        print l