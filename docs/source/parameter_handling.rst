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
    p.setValue("param3", [b"H:+:0.6",b"Na:+:0.2",b"K:+:0.2"], "This is value 3 (StringList)")
    print( p[b"param1"] )
    p[b"param1"] += 3 # add three to the parameter value
    print( p[b"param1"] )
    print( p[b"param3"] )


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
    
    
.. code-block:: python
 
    # print all data inside Param
    def printAll(x):
      if (x.size()):
        for i in x.keys():
          print("Key: ", i, "Value: ", x[i])

      else :
          print("no data availabe")


    new_p = Param()
    if (p.empty() == False): #check p is not empty
      new_p = p               #new soft copy of p generate with name "p"

    #adding 3 more keys with different names
    new_p.setValue("param2", 9.0, "This is value 9")
    new_p.setValue("example1", 6.0, "This is value 6")
    new_p.setValue("example2", 8.0, "This is value 8")
    new_p.setValue("example3", 10.0, "This is value 10")

    #new_p merge in p, p will update same key entries
    p.merge(new_p)
    print(" print All inside p after merge new_p ")
    printAll(p) #print all data 
    
    

.. code-block:: python
 
    print(" print All inside new_p ")
    printAll(new_p) #print all data

    new_p.remove("example3")
    print(" print All inside new_p  after remove function ")
    printAll(new_p) #print all data

    new_p.removeAll("exam")
    print(" print All inside new_p  after remove all with prefix exam ")
    printAll(new_p) #print all data

    if (p == new_p):
      new_p.clear() #clear all entries
    print(" print All inside new_p  after clear function ")
    printAll(new_p) #print all data
