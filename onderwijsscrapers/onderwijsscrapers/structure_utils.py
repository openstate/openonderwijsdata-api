"""
    Utilities for converting JSON-like structures to CSV-like tables and back

    You should be able to convert your structure to a table and back perfectly:
        assert equal( next(structure(flatten(doc))), doc )


    TODO
     - convert tables schemas to json schemas and back

"""

def fields(structured_object, prefix=''):
    """ Get the field names of a structured object """
    if type(structured_object) == dict:
        for k,v in structured_object.iteritems():
            for field in fields(v, prefix='.'+k):
                yield prefix+field
    elif type(structured_object) == list:
        for row in structured_object:
            for field in fields(row, prefix='[]'):
                yield prefix+field
    else:
        yield prefix

def equal(a, b):
    assert type(a) == type(b)
    if type(a) == dict:
        for k in a:
            if not (k in b and equal(a[k], b[k])):
                return False
    elif type(a) == list:
        for a_,b_ in zip(sorted(a), sorted(b)):
            if not equal(a_,b_):
                return False
    else:
        if not a==b:
            return False
    return True

def flatten(structured_object, prefix=''):
    """ Flatten a structured object into rows of flat dicts """
    if type(structured_object) == dict:
        flat_row = {}
        nested_rows = []
        for k,v in structured_object.iteritems():
            for row in flatten(v, prefix='.'+k):
                for k_ in row.keys():
                    if '[]' not in k_:
                        flat_row[prefix+k_] = row.pop(k_)
                if row:
                    nested_rows.append(row)

        if nested_rows:
            # all lists in the structure create extra rows
            for row in nested_rows:
                row = {prefix+k_:v_ for k_,v_ in row.iteritems()}
                row.update(flat_row)
                yield row
        else:
            # if the structure didn't contain any lists, it's just one row
            yield flat_row

    elif type(structured_object) == list:
        for row in structured_object:
            for row_ in flatten(row, prefix='[]'):
                yield {prefix+k_:v_ for k_,v_ in row_.iteritems()}
    else:
        yield {prefix: structured_object}

def add_nested(obj, key, val):
    assert type(obj) == dict, 'obj must be a dict'
    _, _, key_ = key.rpartition('[]')
    k1, _, k2 = key_.partition('.')
    if k2:
        add_nested(obj.setdefault(k1, {}) if k1 else obj, k2, val)
    else:
        obj[k1] = val

def structure(flat_objects):
    """ Proof of concept """
    struct = {}
    key = {}
    for obj in flat_objects:
        for k,v in obj.iteritems():
            prefix, _, suffix = k.rpartition('[]')
            
            # add to a dict for everything on this level
            # the dict is then indexed by everything except
            #   items that only share the prefix and not the rest
            outside = {}
            for k_,v_ in obj.iteritems():
                prefix_, _, suffix_ = k_.rpartition('[]')
                if not(prefix_.startswith(prefix) and prefix!=prefix_):
                    if v_:
                        outside[k_] = v_
            index = tuple(sorted(outside.items()))

            if v:
                struct.setdefault(index, {})[k] = v
                key[index] = prefix

    root = []
    for outside, obj in struct.iteritems():
        parent = {k:v for k,v in outside if k not in obj}
        index = tuple(sorted(parent.items()))
        if index in struct:
            for k in obj.keys():
                # add non-object list items
                if k.endswith('[]'):
                    struct[index].setdefault(key[outside], []).append(obj.pop(k))
            if obj:
                struct[index].setdefault(key[outside], []).append( obj )
        else:
            root.append(obj)

    for obj in struct.itervalues():
        for key in obj.keys():
            add_nested(obj, key, obj.pop(key))

    for part in root:
        yield part

if __name__ == '__main__':
    import argparse, sys, csv, json
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('command', choices=['fields', 'structure', 'flatten'])
    parser.add_argument('--input', '-i', nargs='?', type=argparse.FileType('r'),
        default=sys.stdin, help='default: stdin')
    args = parser.parse_args()

    def csv_field(field):
        return field.lstrip('[]').lstrip('.')

    if args.command == 'structure':
        with sys.stdout as w:
            struct = list(structure(csv.DictReader(args.input)))
            if len(struct) == 1:
                struct = struct[0]
            print >> w, json.dumps(struct, indent=4)
    elif args.command == 'flatten':
        full_structure = json.loads(args.input.read())
        header = map(csv_field, set(fields(full_structure)))
        with sys.stdout as w:
            writer = csv.DictWriter(w, header)
            writer.writeheader()
            for row in flatten(full_structure):
                writer.writerow({csv_field(k): v for k,v in row.items()})
    elif args.command == 'fields':
        full_structure = json.loads(args.input.read())
        for field in set(fields(full_structure)):
            print csv_field(field)