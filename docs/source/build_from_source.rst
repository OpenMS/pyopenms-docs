Build from Source
==================

To install :term:`pyOpenMS` from :index:`source`, you will first have to compile OpenMS
successfully on your platform of choice (note that for MS Windows you will need
to match your compiler and Python version). Please follow the `official
documentation
<https://abibuilder.cs.uni-tuebingen.de/archive/openms/Documentation/release/latest/html/index.html>`_
in order to compile OpenMS for your platform. Next you will need to install the
following software packages

On Microsoft Windows: you need the 64 bit C++ compiler from Visual Studio 2015
to compile the newest :term:`pyOpenMS` for Python 3.5, 3.6 or 3.7. This is important,
else you get a clib that is different than the one used for building the Python
executable, and :term:`pyOpenMS` will crash on import. The OpenMS wiki has `detailed information
<https://github.com/OpenMS/OpenMS/wiki/Build-pyOpenMS-on-Windows>`_ 
on building pyOpenMS on Windows.

You can install all necessary Python packages on which :term:`pyOpenMS`
depends through

.. code-block:: bash

    pip install -U setuptools
    pip install -U pip
    pip install -U autowrap
    pip install -U nose
    pip install -U numpy
    pip install -U wheel

Depending on your systems setup, it may make sense to do this inside a virtual environment

.. code-block:: bash

    virtualenv pyopenms_venv
    source pyopenms_venv/bin/activate


Next, configure OpenMS with :term:`pyOpenMS`: execute ``cmake`` as usual, but with
parameters ``DPYOPENMS=ON``. Also, if using virtualenv or using a specific
Python version, add ``-DPYTHON_EXECUTABLE:FILEPATH=/path/to/python`` to ensure
that the correct Python executable is used. Compiling :term:`pyOpenMS` can use a lot of
memory and take some time, however you can reduce the memory consumption by
breaking up the compilation into multiple units and compiling in parallel, for
example ``-DPY_NUM_THREADS=2 -DPY_NUM_MODULES=4`` will build 4 modules with 2
threads. You can then configure :term:`pyOpenMS`:

.. code-block:: bash

    cmake -DPYOPENMS=ON
    make pyopenms

Build :term:`pyOpenMS` (now there should be :term:`pyOpenMS` specific build targets).
Afterwards, test that all went well by running the tests:

.. code-block:: bash

    ctest -R pyopenms

Which should execute all the tests and return with all tests passing.

Further Questions
*****************

In case the above instructions did not work, please refer to the `Wiki Page
<https://github.com/OpenMS/OpenMS/wiki/pyOpenMS>`_, contact the development
team on github or send an email to the OpenMS mailing list.
