#!/usr/bin/env python3

import argparse
import os
from csv import DictReader
from pathlib import Path
from yaml import dump as dump_yaml
import sys


def _dir_path(string):
    if os.path.isdir(string):
        return string
    else:
        raise Exception(f'"{string}" is not a directory')


def main():
    parser = argparse.ArgumentParser(
        description='Translate a directory of TSVs into YAML.')
    parser.add_argument(
        '--definitions', type=_dir_path,
        required=True,
        help='Definitions directory, containing TSVs')

    args = parser.parse_args()
    definitions_path = Path(args.definitions)

    output = {}
    fields_path = definitions_path / 'fields.tsv'
    output['fields'] = read_fields(fields_path)

    print(dump_yaml(output))
    return 0


def read_fields(path):
    fields = {}
    with open(path) as f:
        rows = list(DictReader(f, dialect='excel-tab'))
        for row in rows:
            fields[row['ES document attribute']] = {
                'neo4j': row['Neo4j Attribute'],
                'required': to_boolean(row['Required Attribute']),
                'description': row['Description'],
                'entity_types': [
                    type.lower() for type in
                    row['Entity types with attribute'].split(', ')
                ]
            }
    return fields


def to_boolean(s):
    map = {
        'Yes': True,
        'No': False
    }
    if s in map:
        return map[s]
    return s


if __name__ == "__main__":
    exit_status = main()
    sys.exit(exit_status)
