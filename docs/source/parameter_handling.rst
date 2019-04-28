Parameter Handling 
==================

Parameter handling in OpenMS and pyOpenMS is usually implemented through inheritance
from ``DefaultParamHandler`` and allow access to parameters through the ``Param`` object. This
means, the classes implement the methods ``getDefaults``, ``getParameters``, ``setParameters``
which allows access to the default parameters, the current parameters and allows to set the
parameters.

The ``Param`` object that is returned can be manipulated through the ``setValue`` and ``getValue``
methods (the ``exists`` method can be used to check for existence of a key). Using the
``getDescription`` method, it is possible to get a help-text for each parameter value in an
interactive session without consulting the documentation.

.. code-block:: python

    from pyopenms import *
    p = Param()
    p.setValue("param1", 4.0, "This is value 1")
    p.setValue("param2", 5.0, "This is value 2")
    print( p[b"param1"] )
    p[b"param1"] += 3 # add three to the parameter value
    print( p[b"param1"] )


The parameters can then be accessed as 

.. code-block:: python

    >>> p.asDict()
    {'param2': 4.0, 'param1': 7.0}
    >>> p.values()
    [4.0, 7.0]
    >>> p.keys()
    ['param1', 'param2']
    >>> p.items()
    [('param1', 7.0), ('param2', 4.0)]
    >>> p.exists("param1")
    True

