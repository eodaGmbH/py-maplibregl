#!/bin/sh
set -e

cp CHANGELOG.md docs/changelog.md

poetry run mkdocs build
