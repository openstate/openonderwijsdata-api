"""
Generate documentation ReStructuredText
using tabular schema definitions and a jinja2 template
"""

if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('sources', nargs='*', type=argparse.FileType('r'))
    parser.add_argument('--schema_dir', default='.')
    args = parser.parse_args()

    from jinja2 import Template
    template = Template(open('docs_template.rst').read())

    import csv, os
    resources = []
    for f in args.sources:
        source_name = f.name
        sources_per_schema = {}
        schemas = {}
        for source in csv.DictReader(f):
            schema = source.pop('schema')
            sources_per_schema.setdefault(schema,[]).append(source)

        for schema_name in sources_per_schema:
            fname = os.path.join(args.schema_dir, schema_name+'.csv')
            schema = open(fname)
            schemas[schema_name] = {
                'header': next(schema),
                'content': '   '.join(schema)
            }

        resources.append({
            'name': f.name,
            'sources': sources_per_schema,
            'schemas': schemas,
        })

    print template.render(resources=resources).encode('utf8')