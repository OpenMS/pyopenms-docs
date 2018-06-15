pyOpenMS Installation
=====================

Binaries
********

To :index:`install` pyOpenMS from the binaries, you can simply type

.. code-block:: bash

  pip install numpy
  pip install pyopenms


We have binary packages for OSX, Linux and Windows (64 bit only).


Source
******

To install pyOpenMS from :index:`source`, you will first have to compile OpenMS
successfully on your platform of choice. Please follow the `official
documenation <http://ftp.mi.fu-berlin.de/pub/OpenMS/release-documentation/html/index.html>`_
in order to compile OpenMS for your platform and have a look at the specific
`pyOpenMS 
documenation <http://ftp.mi.fu-berlin.de/pub/OpenMS/release-documentation/html/pyOpenMS.html>`_.
In order to compile pyOpenMS you then have to configure with 

.. code-block:: bash

    cmake -DPYOPENMS=ON /path/to/OpenMS

which will add `pyopenms` as as make target and you can build pyOpenMS with

.. code-block:: bash

    make pyopenms

Wrap Classes
************

In order to wrap new classes in pyOpenMS, read the following `guide
<wrap_classes.html>`_.
