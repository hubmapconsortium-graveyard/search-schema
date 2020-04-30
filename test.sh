#!/usr/bin/env bash
set -o errexit

red=`tput setaf 1`
green=`tput setaf 2`
reset=`tput sgr0`
start() { [[ -z $CI ]] || echo travis_fold':'start:$1; echo $green$1$reset; }
end() { [[ -z $CI ]] || echo travis_fold':'end:$1; }
die() { set +v; echo "$red$*$reset" 1>&2 ; exit 1; }

start flake8
  flake8 || die 'Try: autopep8 --in-place --aggressive -r .'
end flake8

start doctests
  find src | grep '\.py$' | xargs python -m doctest
end doctests

start tsv-to-yaml
  REAL_YAML=data/definitions.yaml
  TEST_YAML=data/definitions.yaml.test
  CMD="src/definitions-tsv-to-yaml.py --definitions data/definitions"

  WHOLE_CMD="$CMD > $TEST_YAML"
  echo "Running '$WHOLE_CMD'"
  eval $WHOLE_CMD

  diff --ignore-blank-lines $REAL_YAML $TEST_YAML \
    || die "To refresh: $CMD > $REAL_YAML"
  rm $TEST_YAML
end tsv-to-yaml

start yaml-to-schema
  REAL_SCHEMAS=data/schemas/
  TEST_SCHEMAS=data/schemas.test/
  CMD="src/definitions-yaml-to-schema.py --definitions $REAL_YAML --schemas"

  WHOLE_CMD="$CMD $TEST_SCHEMAS"
  echo "Running '$WHOLE_CMD'"
  eval $WHOLE_CMD

  diff --ignore-blank-lines $REAL_SCHEMAS $TEST_SCHEMAS \
    || die "To refresh: $CMD $REAL_SCHEMAS"
  rm -rf $TEST_SCHEMAS
end yaml-to-schema

start examples
  for EXAMPLE in examples/*; do
    TYPE=`basename $EXAMPLE .json`
    src/validate.py --document $EXAMPLE --schema data/schemas/$TYPE.schema.yaml
  done
end examples

start changelog
  if [ "$TRAVIS_BRANCH" != 'master' ]; then
    diff CHANGELOG.md <(curl -s https://raw.githubusercontent.com/hubmapconsortium/search-schema/master/CHANGELOG.md) \
      && die 'Update CHANGELOG.md'
  fi
end changelog
