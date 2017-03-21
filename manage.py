#!/usr/bin/env python
import json
from glob import glob
import os

import click
from click.core import Command
from click.decorators import _make_command

from elasticsearch import Elasticsearch
from elasticsearch.exceptions import RequestError

def command(name=None, cls=None, **attrs):
    """
    Wrapper for click Commands, to replace the click.Command docstring with the
    docstring of the wrapped method (i.e. the methods defined below). This is
    done to support the autodoc in Sphinx, and the correct display of docstrings
    """
    if cls is None:
        cls = Command
    def decorator(f):
        r = _make_command(f, name, attrs, cls)
        r.__doc__ = f.__doc__
        return r
    return decorator

@click.group()
def cli():
    """Open Onderwijs Data"""

@cli.group()
def elasticsearch():
    """Manage Elasticsearch"""

@command('create_indexes')
@click.argument('mapping_dir', type=click.Path(exists=True, resolve_path=True))
def create_indexes(mapping_dir):
    """
    Create all indexes for which a mapping- and settings file is available.

    It is assumed that mappings in the specified directory follow the
    following naming convention: "ocd_mapping_{SOURCE_NAME}.json".
    For example: "ocd_mapping_rijksmuseum.json".
    """
    click.echo('Creating indexes for ES mappings in %s' % (mapping_dir))

    es = Elasticsearch()

    for mapping_file_path in glob('%s/*.json' % mapping_dir):
        # Extract the index name from the filename
        mapping_file = os.path.split(mapping_file_path)[-1].split('.')[0]
        index_name = '%s' % (mapping_file)

        click.echo('Creating ES index %s' % index_name)

        mapping_file = open(mapping_file_path, 'rb')
        mapping = json.load(mapping_file)
        mapping_file.close()

        try:
            es.indices.create(index=index_name, body=mapping)
        except RequestError as e:
            error_msg = click.style('Failed to create index %s due to ES '
                                    'error: %s' % (index_name, e.error),
                                    fg='red')
            click.echo(error_msg)

# Register commands explicitly with groups, so we can easily use the docstring
# wrapper
elasticsearch.add_command(create_indexes)

if __name__ == '__main__':
    cli()
