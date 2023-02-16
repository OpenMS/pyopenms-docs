Parameter Handling 
==================

Parameter handling in OpenMS and :term:`pyOpenMS` is usually implemented through inheritance
from :py:class:`~.DefaultParamHandler` and allow access to parameters through the :py:class:`~.Param` object. This
means, the classes implement the methods ``getDefaults``, ``getParameters``, ``setParameters``
which allows access to the default parameters, the current parameters and allows to set the
parameters.

The :py:class:`~.Param` object that is returned can be manipulated through the :py:meth:`~.Param.setValue`
and :py:meth:`~.Param.getValue` methods (the ``exists`` method can be used to check for existence of a key). Using the
:py:meth:`~.Param.getDescription` method, it is possible to get a help-text for each parameter value in an
interactive session without consulting the documentation.

.. code-block:: python
    :linenos:

    from pyopenms import *

    p = Param()
    p.setValue("param1", 4.0, "This is value 1")
    p.setValue("param2", 5.0, "This is value 2")
    p.setValue(
        "param3",
        [b"H:+:0.6", b"Na:+:0.2", b"K:+:0.2"],
        "This is value 3 (StringList)",
    )
    print(p[b"param1"])
    p[b"param1"] += 3  # add three to the parameter value
    print(p[b"param1"])
    print(p[b"param3"])


The parameters can then be accessed as 

.. code-block:: pycon

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


The param object can be copy and merge in to other param object as 
 
.. code-block:: python

    # print the key and values pairs stored in a Param object
    def printParamKeyAndValues(p):
        if p.size():
            for i in p.keys():
                print("Key:", i, "Value:", p[i])
        else:
            print("no data availabe")


    new_p = Param()
    if p.empty() == False:  # check p is not empty
        new_p = p  # new deep copy of p generate with name "new_p"

    # we will add 4 more keys to the new_p
    new_p.setValue("param2", 9.0, "This is value 9")
    new_p.setValue("example1", 6.0, "This is value 6")
    new_p.setValue("example2", 8.0, "This is value 8")
    new_p.setValue("example3", 10.0, "This is value 10")

    # names "example1", "example2" , "example3" keys will added to p, but "param2" will update the value
    p.merge(new_p)
    print(" print the key  and values pairs stored in a Param object p ")
    printParamKeyAndValues(p)


In param object the keys values can be remove by key_name or prefix as

.. code-block:: python

    # We now call the remove method with key of the entry we want to delete ("example3")
    new_p.remove("example3")
    print("Key and values pairs after removing the entry with key: example3")
    printParamKeyAndValues(new_p)

    # We now want to delete all keys with prefix "exam"
    new_p.removeAll("exam")
    print(
        "Key and value pairs after removing all entries with keys starting with: exam"
    )
    printParamKeyAndValues(new_p)

    # we can compare Param objects for identical content
    if p == new_p:  # check p is equal to new_p
        new_p.clear()  # Example: delete all keys from new_p

    print("Keys and values after deleting all entries.")
    printParamKeyAndValues(new_p)  # All keys of new_p deleted
