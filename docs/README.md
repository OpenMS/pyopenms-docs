pyOpenMS Documentation
======================

Preparation
install Sphinx (which is a pyton module) and some of its modules/plugins.
We recommend doing this in a [python venv](https://docs.python.org/3/library/venv.html).

```
  pip install -U sphinx
  pip install sphinx-hoverxref
  pip install sphinx_copybutton
  pip install sphinx_remove_toctrees
  pip install pydata_sphinx_theme
  ## use the latest pyOpenMS (or build your own from source)
  pip install --index-url https://pypi.cs.uni-tuebingen.de/simple/ pyopenms
```


The source code for the pyOpenMS documentation lies here. We use sphinx to
build documentation and to build you can run 

    sphinx-build <pyOpenMS_dir>/docs/source/ build/

On a linux system, you can also use the provided Makefile and run 

    make html



