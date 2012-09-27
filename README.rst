Tagman for Django
=================

A django tagging app that, unlike taggit and django-tagging, does not implement
free-form tagging but focuses on more curated tags that can be added to any
model.

In trying to reconcile concepts of 'categorisation' and 'tagging' in certain
projects we found that a qualified tag worked well. Thus a tag is not just
'beef' or 'onion' it is 'meat:beaf' or 'flavour:beef'. A given model can thus
have many tags belonging to one or more groups and this can be useful in
many cases.

We have also eschewed, at least in this code, the option to add free-form
tags to models in favour of a controlled vocabulary. Thus admin permissions
can be used to allow only certain users to create new tags and tag groups,
and even if all are allowed to do so, the mechanism introduces a little
friction that makes tag creation a more considered process.

Functionality is also provided for 'system' tags that can be made not to appear
in M2M widgets by default so users cannot add them directly to objects. They
may be added automatically on the fly thus providing 'auto tagging'.

Installation
------------

With pip::

 > pip install tagman

From a GIT checkout::

 > python setup.py install


Testing
-------

If you have a GIT checkout of this repository you can run the tests as follows:

* create and activate a virtualenv for the project
* `pip install -r test_requirements`
* `./runtests.sh`

This will run all the unit tests, create a coverage report
(see `htmlcov/index.html`) and also PEP8 check the code (see `pep8.txt`).

Jenkins
-------

If you like to use Jenkins you may like to make use of our build script
`build.sh`. If executed by Jenkins as a build step you can then ingest the
output as follows:

* Cobertura plugin can read `coverage.xml`
* xUnit plugin can read JUnit formatted `nosetests.xml`
* violations plugin: add `pep8.txt` to the pep8 field

.. include:: <isonum.txt>
Copyright |copy| 2012 ReThought Ltd, all rights reserved
