pyOpenMS Installation
=====================

Binaries
********

To :index:`install` pyOpenMS from the binaries, you can simply type

.. code-block:: bash

  pip install numpy
  pip install pyopenms


We have binary packages for OSX, Linux and Windows (64 bit only) available from
`PyPI <https://pypi.org/project/pyopenms>`_. Note that for Windows, we only
support Python 3.5, 3.6 and 3.7 in their 64 bit versions, therefore make sure
to download the 64bit Python release for Windows. For OSX and Linux, we
additionally also support Python 2.7 as well as Python 3.4 (Linux only).

You can install Python first from `here <https://www.python.org/downloads/>`_,
again make sure to download the 64bit release. You can then open a shell and
type the two commands above (on Windows you may potentially have to use
``C:\Python36\Scripts\pip.exe`` in case ``pip`` is not in your system path).

Source
******

To install pyOpenMS from :index:`source`, you will first have to compile OpenMS
successfully on your platform of choice and then follow the `building from
source <build_from_source.html>`_ instructions. Note that *this is not recommended*.

Wrap Classes
************

In order to wrap new classes in pyOpenMS, read the following `guide
<wrap_classes.html>`_.

