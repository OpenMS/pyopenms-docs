#!/bin/bash

echo "Start generating notebooks"

failed=0
shopt -s globstar
for FILE in **/*.rst; do
  if [[ $FILE != *"_templates"* ]]; then
    a=(${FILE/./ })
    pandoc ${FILE} -o ${a[0]}.ipynb --resource-path user_guide/ --filter ../pandoc_filters/admonitionfilter.py --filter ../pandoc_filters/code_pandocfilter.py --filter ../pandoc_filters/ignore_pandocfilter.py --filter ../pandoc_filters/transformlinks_pandocfilter.py --filter ../pandoc_filters/transformreferences_pandocfilter.py
    retVal=$?
    if [ $retVal -ne 0 ]; then
      echo "Error generating ${a[0]}.ipynb"
      failed=1
    else
      echo "${a[0]}.ipynb Generated"
    fi
  fi
done

if [ $failed -ne 0 ]; then
  echo "Error generating at least one notebook."
  exit 1
else
  echo "Notebooks generated successfully"
  exit 0
fi
