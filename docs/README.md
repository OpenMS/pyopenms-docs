pyOpenMS Documentation
======================
The source code for the pyOpenMS documentation lies here. We use sphinx to
build documentation.

Preparation

Install Sphinx (which is a pyton module) and some of its modules/plugins.
We recommend doing this in a [python venv](https://docs.python.org/3/library/venv.html).

    python -m venv c:\path\to\myenv
    # activate it, e.g.
    source <venv>/bin/activate

Once the environment is active, you can install all required python packages using

    pip install -r <pyOpenMS_dir>/docs/requirements.txt


To build the docs run (works on all OS's)

    make html
    
and check validity of links using

    make linkcheck
    



