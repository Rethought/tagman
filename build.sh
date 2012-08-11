#!/bin/bash
# build script for apps that are packaged in isolation from a wrapping
# django project.

VIRTUALENV=../.venv
if [ -e "$VIRTUALENV" ]
then
    echo "Re-using existing virtualenv"
    . $VIRTUALENV/bin/activate
else
    virtualenv --no-site-packages $VIRTUALENV || { echo "Virtualenv failed"; exit -1; }
    . $VIRTUALENV/bin/activate
    easy_install -U setuptools
    easy_install pip
    rm -f ../md5.test_requirements.last
fi

md5sum src/test_requirements.txt > ../md5.test_requirements.new
diff ../md5.test_requirements.new ../md5.test_requirements.last
TEST_REQUIREMENTS_DIFF=$?

if [ "$TEST_REQUIREMENTS_DIFF" -ne 0 ]
then
    pip install --timeout 300 -r src/test_requirements.txt || { echo "pip failed (test_requirements)"; exit -1; }
    mv ../md5.test_requirements.new ../md5.test_requirements.last
fi

# MOVE INTO SRC
cd src
find . -name "*.pyc" -exec rm {} \;
coverage erase
PYTHONPATH=. coverage run --omit "*venv*,*test*,*migrations*,test_settings.py,settings.py,manage.py" runtests.py  || echo "Test failed"
coverage xml
coverage html
echo "Checking for PEP-8 violations"
pep8 --ignore=W293,E128,E501,E127 --exclude=migrations,manage.py,docs,assets,settings.py -r . > pep8.txt || echo "PEP-8 violations."

# due to MP inability to get Jenkins to find the files here, let's move them
# up one
mv pep8.txt ..
mv coverage.xml ..
