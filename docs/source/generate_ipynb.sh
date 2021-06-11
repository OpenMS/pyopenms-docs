#!/bin/bash

for FILE in *.rst; do a=(${FILE/./ }); rst2ipynb ${FILE} -o ${a[0]}.ipynb; done
