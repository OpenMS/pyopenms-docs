Pyopenms in R
===============

Install the "reticulate" R package
**********************************

In order to use all pyopenms functionalities in R, we suggest to use the "reticulate" R package.

A thorough documentation is available at: https://rstudio.github.io/reticulate/

.. code-block:: R

    install.packages("reticulate")

Import pyopenms in R
********************

Installation of pyopenms is a requirement as well, but after loading the "reticulate" library you should be able to import pyopenms into R

.. code-block:: R

    library(reticulate)
    import("pyopenms", convert = FALSE)

This should now give you access to all of pyopenms in R. Importantly the convert option
has to be set to FALSE, since type conversions such as 64bit integers will cause a problem.

You should now be able to interact with the OpenMS library and, for example, read and write mzML files:

.. code-block:: R

    library(reticulate)
    ropenms=import("pyopenms", convert = FALSE)
    exp = ropenms$MSExperiment()
    ropenms$MzMLFile()$store("testfile.mzML", exp)

which will create an empty mzML file called `testfile.mzML`.

Getting help
************

Using the "reticulate" R package provides a way to access the pyopenms information 
about the available functions and methods. We can inspect individual pyOpenMS objects 
through the ``py_help`` function or the autocompletion funcionality of RStudio:

.. code-block:: R

    library(reticulate)
    ropenms=import("pyopenms", convert = FALSE)
    idXML=ropenms$IdXMLFile
    py_help(idXML)

    Help on class IdXMLFile in module pyopenms.pyopenms_4:

   class IdXMLFile(__builtin__.object)
    |  Methods defined here:
    |  
    |  __init__(...)
    |      Cython signature: void IdXMLFile()
    |  
    |  load(...)
    |      Cython signature: void load(String filename, libcpp_vector[ProteinIdentification] & protein_ids, libcpp_vector[PeptideIdentification] & peptide_ids)
    [...]

    idXML=ropenms$IdXMLFile()
    idXML$...load... (autocompletion)

    (possibly screenshot)

    Cython signature: void load(String filename, libcpp_vector[ProteinIdentification] & protein_ids, libcpp_vector[PeptideIdentification] & peptide_ids)

    In this case the idXML$load function requires:
       - a filename as string
       - an empty vector for pyopenms.ProteinIdentification objects
       - an empty vector for pyopenms.PeptideIdentification objects

    Creating an empty R list() unfortunately is not equal to the empty python list []

    Therefore in this case we need to use the "reticulate" r_to_py() function:

    f="/OpenMS/OpenMS/share/OpenMS/examples/BSA/BSA1_OMSSA.idXML"
    pepids=r_to_py([])
    protids=r_to_py([])

    --> idXML$load(f, pepids, protids)

In order to get more information about the wrapped functions, we can also 
consult the `pyOpenMS manual <http://proteomics.ethz.ch/pyOpenMS_Manual.pdf>`_ 
which references to all wrapped functions.

First look at data
******************

File reading
^^^^^^^^^^^^

pyOpenMS supports a variety of different files through the implementations in
OpenMS. In order to read mass spectrometric data, we can download the `mzML
example file <http://proteowizard.sourceforge.net/example_data/tiny.pwiz.1.1.mzML>`_

.. code-block:: python

    from urllib.request import urlretrieve
    # from urllib import urlretrieve  # use this code for Python 2.x
    from pyopenms import *
    urlretrieve ("http://proteowizard.sourceforge.net/example_data/tiny.pwiz.1.1.mzML", "tiny.pwiz.1.1.mzML")
    exp = MSExperiment()
    MzMLFile().load("tiny.pwiz.1.1.mzML", exp)

which will load the content of the "tiny.pwiz.1.1.mzML" file into the ``exp``
variable of type ``MSExperiment``.
We can now inspect the properties of this object:

.. code-block:: python

    >>> help(exp)
    Help on MSExperiment object:

    class MSExperiment(__builtin__.object)
     |  Methods defined here:
     ...
     |  getNrChromatograms(...)
     |      Cython signature: size_t getNrChromatograms()
     |
     |  getNrSpectra(...)
     |      Cython signature: size_t getNrSpectra()
     |
     ...


which indicates that the variable ``exp`` has (among others) the functions
``getNrSpectra`` and ``getNrChromatograms``. We can now try these functions:

.. code-block:: python

    >>> exp.getNrSpectra()
    4
    >>> exp.getNrChromatograms()
    2

and indeed we see that we get information about the underlying MS data. We can
iterate through the spectra as follows:


Iteration
^^^^^^^^^

.. code-block:: python

    >>> for spec in exp:
    ...   print ("MS Level:", spec.getMSLevel())
    ...
    MS Level: 1
    MS Level: 2
    MS Level: 1
    MS Level: 1

This iterates through all available spectra, we can also access spectra through the ``[]`` operator:

.. code-block:: python

    >>> print ("MS Level:", exp[1].getMSLevel())
    MS Level: 2

Note that ``spec[1]`` will access the *second* spectrum (arrays start at
``0``). We can access the raw peaks through ``get_peaks()``:

.. code-block:: python

    >>> spec = exp[1]
    >>> mz, i = spec.get_peaks()
    >>> sum(i)
    110

Which will access the data using a numpy array, storing the *m/z* information
in the ``mz`` vector and the intensity in the ``i`` vector. Alternatively, we
can also iterate over individual peak objects as follows (this tends to be
slower):

.. code-block:: python

    >>> for peak in spec:
    ...   print (peak.getIntensity())
    ...
    20.0
    18.0
    16.0
    14.0
    12.0
    10.0
    8.0
    6.0
    4.0
    2.0

TIC calculation
^^^^^^^^^^^^^^^


With this information, we can now calculate a total ion current (TIC) using the
following function:

.. code-block:: python
   :linenos:

    def calcTIC(exp):
        tic = 0
        for spec in exp:
            if spec.getMSLevel() == 1:
                mz, i = spec.get_peaks()
                tic += sum(i)
        return tic

To calculate a TIC we would now call the function:

.. code-block:: python
   :linenos:

    >>> calcTIC(exp)
    240.0
    >>> sum([sum(s.get_peaks()[1]) for s in exp if s.getMSLevel() == 1])
    240.0

Note how one can compute the same property using list comprehensions in Python (see the third line above).

