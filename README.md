[![Documentation Status](https://readthedocs.org/projects/pyopenms/badge/?version=latest)](https://pyopenms.readthedocs.io/en/latest/?badge=latest)
[![Build notebooks from master and push to master+ipynb](https://github.com/OpenMS/pyopenms-docs/actions/workflows/build-push-notebooks.yaml/badge.svg)](https://github.com/OpenMS/pyopenms-docs/actions/workflows/build-push-notebooks.yaml)
[![Test code in notebooks](https://github.com/OpenMS/pyopenms-docs/actions/workflows/test-notebooks.yml/badge.svg)](https://github.com/OpenMS/pyopenms-docs/actions/workflows/test-notebooks.yml)

pyOpenMS Documentation
======================

pyOpenMS are the Python bindings to the OpenMS open-source C++ library for
LC-MS data management and analyses. The Python bindings cover a large part of
the OpenMS API to enable rapid algorithm development and workflow development.
pyOpenMS supports the Proteomics Standard Initiative (PSI) formats for MS data. 

This repository contains documentation, installation instructions, and example code
that show different functions of pyOpenMS.

Installation
=============

Installation is best done through [PyPI](https://pypi.python.org/pypi/pyopenms)
(the Python package index) where binary packages are provided for the release
versions of OpenMS, covering Linux/Mac/Windows. Alternatively, it is available on (bio)conda.

For the brave nightly build can be found at [our local PyPI server](https://pypi.cs.uni-tuebingen.de/).

Documentation
=============
The readthedocs pyOpenMS documentation is generated from the master branch of this repository, see [docs/README.md](docs/README.md)

The generated documentation is available here: https://pyopenms.readthedocs.io/en/latest/

Jupyter Notebooks
=============
Are created by CI and stored in master+ipynb to not clutter the master branch.

Binder integration
=============
Binder uses the Jupyter Notebooks in master+ipynb. The conda environment is described in environment.yml, the post-build event installs the nightly pyopenms wheel. Currently, only environment.yml is used by binder. Note: You can test a branch "jpfeuffer-patch-6" using https://notebooks.gesis.org/binder/v2/gh/OpenMS/pyopenms-docs/jpfeuffer-patch-6 
