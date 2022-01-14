Installation
============


Try online
----------

You can try out pyOpenMS in your browser. Just navigate to a topic you are interested in
by clicking in the menu bar. Then click on the "Try online with Binder" button.

.. image:: img/binderIntegration.gif

Note that the first start of binder might take a bit. While binder is perfect
for trying pyOpenMS it only offers a limited amount of memory. You should install
the pyOpenMS binaries on your PC for serious data processing.

We recommend to use pyOpenMS in PyCharm as it works well with source code documentation.

Command Line
------------

To :index:`install` pyOpenMS from the command line using the binary wheels, you
can type

.. code-block:: bash

  pip install numpy
  pip install pyopenms


We have binary packages for OSX, Linux and Windows (64 bit only) available from
`PyPI <https://pypi.org/project/pyopenms>`_. Make sure to download
the 64bit Python release for Windows. Currently we only support
Python 3.7, 3.8 and 3.9.

You can install Python first from `here <https://www.python.org/downloads/>`_,
again make sure to download the 64bit release. You can then open a shell and
type the two commands above (on Windows you may potentially have to use
``C:\Python37\Scripts\pip.exe`` in case ``pip`` is not in your system path).

Nightly/ CI wheels
------------------

If you want the newest features you can also install nightly builds of pyOpenMS.

You can either directly download the latest nightly build by executing the commands below.

.. code-block:: bash
  MY_OS="Linux" # or "macOS" or "Windows" (case-sensitive)
  wget https://nightly.link/OpenMS/OpenMS/workflows/pyopenms-wheels/nightly/${MY_OS}-wheels.zip\?status\=completed
  mv ${MY_OS}-wheels.zip\?status=completed ${MY_OS}-wheels.zip
  
Or manually visit the GitHub page that contains the action to build the nightly wheels: https://github.com/OpenMS/OpenMS/actions/workflows/pyopenms-wheels.yml,
click on e.g., the newest nightly build on the top to get access to artefacts and download the corresponding wheel for macOS, Linux, or Windows.

.. image:: img/githubActionWheels.png

Now, unzip the folder and select the supported Python version for your environment.
The supported Python version is denoted as ``cp3X`` in the wheel file name
(e.g. pyopenms_nightly-2.7.0.dev20220111-cp39-cp39-macosx_10_9_x86_64 for python 3.9 and macOS >= 10.9)

Finally, install the package with the following shell command:

.. code-block:: bash

  pip install your-compatible.whl --no-cache-dir

Note that the Github Action page may contain unstable builds and different operating systems might
be in a different state (they even might not be available if the builds for a specific OS did not succeed in a long time).


Source (advanced users)
-----------------------

To install pyOpenMS from :index:`source`, you will first have to compile OpenMS
successfully on your platform of choice and then follow the `building from
source <build_from_source.html>`_ instructions. Note that this may be
non-trivial and *is not recommended* for most users.

Wrap Classes (advanced users)
-----------------------------

In order to wrap new classes in pyOpenMS, read the following `guide
<wrap_classes.html>`_.
