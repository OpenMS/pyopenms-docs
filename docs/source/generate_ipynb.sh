#!/bin/bash

echo "Process Started"

shopt -s globstar
for FILE in **/*.rst; do
  if [[ $string != *"_templates"* ]]; then
    a=(${FILE/./ })
    pandoc ${FILE} -o ${a[0]}.ipynb --filter ../pandoc_filters/admonitionfilter.py --filter ../pandoc_filters/code_pandocfilter.py --filter ../pandoc_filters/ignore_pandocfilter.py --filter ../pandoc_filters/transformlinks_pandocfilter.py
    echo "${a[0]}.ipynb Generated"
  fi
done

echo "Process Completed Successfully"
