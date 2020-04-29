#!/usr/bin/env python3

import argparse
from yaml import dump as dump_yaml, safe_load as load_yaml
from pathlib import Path


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
    definitions = load_yaml(Path(args.definitions).read())
    output = definitions

    schemas_dir_path = args.schemas
    (schemas_dir_path / 'donor.schema.yaml').write(dump_yaml(output))
    (schemas_dir_path / 'sample.schema.yaml').write(dump_yaml(output))
    (schemas_dir_path / 'dataset.schema.yaml').write(dump_yaml(output))
    return 0
