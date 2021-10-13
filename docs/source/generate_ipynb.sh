#!/bin/bash

echo "Process Started"

for FILE in *.rst; do a=(${FILE/./ }); pandoc ${FILE} -o ${a[0]}.ipynb --filter ../pandoc_filters/code_pandocfilter.py --filter ../pandoc_filters/ignore_pandocfilter.py --filter ../pandoc_filters/transformlinks_pandocfilter.py; echo "${a[0]}.ipynb Generated"; done

echo "Process Completed Successfully"
