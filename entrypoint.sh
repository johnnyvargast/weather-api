#!/bin/bash

PREFIX="[*]"

echo

echo $PREFIX "Django check"
python3 manage.py check

echo

echo $PREFIX "Current test"
python3 manage.py test

echo $PREFIX "Run server"

exec "$@"
