#!/usr/bin/env python3

import argparse
from yaml import dump as dump_yaml, safe_load as load_yaml
from pathlib import Path
import sys


def _dir_path(string):
    path = Path(string)
    path.mkdir(parents=True, exist_ok=True)
    return path


def main():
    parser = argparse.ArgumentParser(
        description='Translate definitions as YAML into JSON Schemas.')
    parser.add_argument(
        '--definitions', type=argparse.FileType('r'),
        required=True,
        help='Definitions YAML')
    parser.add_argument(
        '--schemas', type=_dir_path,
        required=True,
        help='Output directory for JSON Schema')

    args = parser.parse_args()
    definitions = load_yaml(args.definitions.read())

    for entity_type in ['donor', 'sample', 'dataset']:
        path = args.schemas / f'{entity_type}.schema.yaml'
        path.write_text(dump_yaml(make_schema(entity_type, definitions)))

    return 0


def make_schema(entity_type, definitions):
    properties = {
        k: {
            'description': v['description']
        }
        for k, v in definitions['fields'].items()
        if entity_type in v['entity_types']
    }
    required = [
        k
        for k, v in definitions['fields'].items()
        if entity_type in v['entity_types']
        and v['required'] is True
        # TODO: Some (true-y) strings are used for special cases.
    ]
    return {
        'type': 'object',
        'properties': properties,
        'required': required,
        'additionalProperties': False
    }


if __name__ == "__main__":
    exit_status = main()
    sys.exit(exit_status)
