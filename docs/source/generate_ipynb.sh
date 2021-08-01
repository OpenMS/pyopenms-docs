#!/bin/bash

echo "Process Started"

for FILE in *.rst; do a=(${FILE/./ }); rst2ipynb ${FILE} -o ${a[0]}.ipynb; echo "${a[0]}.ipynb Generated"; done

echo "Process Completed Successfully"
