#!/bin/bash

find src -name "*.pyc" -exec rm {} \;
coverage erase
PYTHONPATH=src coverage run --omit "*venv*,*migrations*,test_settings.py,settings.py,manage.py" src/runtests.py  || echo "Test failed"
coverage xml
coverage html
echo "Checking for PEP-8 violations"
pep8 --ignore=W293,E128,E501,E127 --exclude=migrations,manage.py,docs,assets,settings.py -r src > pep8.txt || echo "PEP-8 violations."
