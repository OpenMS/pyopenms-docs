[![Documentation Status](https://readthedocs.org/projects/pyopenms/badge/?version=latest)](https://pyopenms.readthedocs.io/en/latest/?badge=latest)
[![Build notebooks from master and push to master+ipynb](https://github.com/OpenMS/pyopenms-docs/actions/workflows/build-push-notebooks.yaml/badge.svg)](https://github.com/OpenMS/pyopenms-docs/actions/workflows/build-push-notebooks.yaml)
[![Test code in notebooks](https://github.com/OpenMS/pyopenms-docs/actions/workflows/test-notebooks.yml/badge.svg)](https://github.com/OpenMS/pyopenms-docs/actions/workflows/test-notebooks.yml)

# pyOpenMS Documentation

pyOpenMS are the Python bindings to the OpenMS open-source C++ library for
LC-MS data management and analyses. 
This repository contains documentation, installation instructions, and example code
that show different functions of pyOpenMS.

## Table of Contents

- [Documentation Architecture](#documentation-architecture)
- [Build System](#build-system)
- [Notebook Pipeline](#notebook-pipeline)
- [CI/CD Workflows](#cicd-workflows)
- [Development Guide](#development-guide)
- [Binder Integration](#binder-integration)
- [Troubleshooting](#troubleshooting)


## Documentation Architecture

The pyOpenMS documentation system is built on several interconnected components:

### Core Technologies
- **Sphinx**: Static site generator for documentation (v6.1.0)
- **PyData Sphinx Theme**: Modern, responsive documentation theme
- **Pandoc**: Universal document converter for RST → Jupyter notebook conversion
- **Jupyter**: Interactive notebook environment for examples
- **ReadTheDocs**: Documentation hosting platform

### Repository Structure
```
pyopenms-docs/
├── .github/workflows/       # CI/CD pipelines
├── docs/
│   ├── source/             # RST documentation source files
│   │   ├── _ext/          # Custom Sphinx extensions
│   │   ├── _static/       # Static assets (CSS, JS, images)
│   │   ├── _templates/    # Custom Sphinx templates
│   │   ├── apidocs/       # API documentation configuration
│   │   ├── user_guide/    # User guide RST files
│   │   ├── community/     # Community documentation
│   │   └── conf.py        # Sphinx configuration
│   ├── pandoc_filters/    # Custom filters for RST→notebook conversion
│   ├── Makefile          # Build automation
│   └── requirements.txt   # Documentation dependencies
├── src/                   # Example code and data files
├── environment.yml        # Binder environment configuration
└── postBuild             # Binder post-installation script
```

## Build System

### Local Documentation Build

#### Prerequisites
1. Create and activate a Python virtual environment:
```bash
python -m venv /path/to/myenv
source /path/to/myenv/bin/activate  # Linux/Mac
# or
path\to\myenv\Scripts\activate.bat   # Windows
```

2. Install dependencies:
```bash
cd docs/
pip install -r requirements.txt
```

#### Building HTML Documentation
```bash
cd docs/
make html  # Builds HTML docs in build/html/
```

The build process:
1. Sphinx reads all RST files from `source/`
2. Applies custom extensions and themes
3. Generates API documentation using autodoc
4. Outputs HTML to `build/html/`

#### Generating Jupyter Notebooks
```bash
cd docs/
make doc  # Runs source/generate_ipynb.sh
```

This converts all RST files to Jupyter notebooks using Pandoc with custom filters.

#### Validating Links
```bash
cd docs/
make linkcheck
```

### Sphinx Configuration

Key configuration in `docs/source/conf.py`:
- **Theme**: PyData Sphinx Theme with custom options
- **Extensions**: 
  - `autodoc` & `autosummary`: Automatic API documentation
  - `hoverxref`: Interactive tooltips for glossary terms
  - `sphinx_copybutton`: Code block copy buttons
  - Custom extensions: `chemrole`, `glossary_warnings`
- **Version Management**: Automatic version detection from git branches
- **Custom Assets**: CSS, JavaScript, and logo files

## Notebook Pipeline

### RST to Jupyter Conversion

The notebook generation pipeline converts documentation from RST format to interactive Jupyter notebooks:

1. **Source**: RST files in `docs/source/`
2. **Conversion Tool**: Pandoc with custom filters
3. **Output**: Jupyter notebooks (`.ipynb` files)

#### Conversion Process

The `generate_ipynb.sh` script:
```bash
pandoc ${FILE}.rst -o ${FILE}.ipynb \
  --resource-path user_guide/ \
  --filter ../pandoc_filters/admonitionfilter.py \
  --filter ../pandoc_filters/code_pandocfilter.py \
  --filter ../pandoc_filters/ignore_pandocfilter.py \
  --filter ../pandoc_filters/transformlinks_pandocfilter.py \
  --filter ../pandoc_filters/transformreferences_pandocfilter.py
```

#### Custom Pandoc Filters

Located in `docs/pandoc_filters/`:
- **admonitionfilter.py**: Converts RST admonitions to notebook-friendly format
- **code_pandocfilter.py**: Handles code block formatting and execution cells
- **ignore_pandocfilter.py**: Skips certain RST directives not needed in notebooks
- **transformlinks_pandocfilter.py**: Converts documentation links
- **transformreferences_pandocfilter.py**: Handles cross-references

### Branch Strategy

- **master**: Contains source RST files and documentation
- **master+ipynb**: Auto-generated branch with compiled Jupyter notebooks
  - Created by CI/CD on push to master
  - Used by Binder for interactive environments
  - Prevents cluttering master with generated files

## CI/CD Workflows

All workflows are located in `.github/workflows/`:

### 1. build-push-notebooks.yaml
**Trigger**: Push to master branch  
**Purpose**: Generate Jupyter notebooks and push to master+ipynb branch

**Steps**:
1. Setup Python 3.10 and Pandoc 3.1.2
2. Install dependencies (Jupyter, requirements.txt)
3. Run `make doc` to generate notebooks from RST
4. Commit and force-push to master+ipynb branch

### 2. test-notebooks.yml
**Trigger**: Push to master+ipynb branch or manual  
**Purpose**: Test all generated notebooks for execution errors

**Steps**:
1. Setup Python 3.10
2. Install dependencies
3. Execute all notebooks using `jupyter nbconvert --execute`
4. Report any failed notebooks

### 3. test-pr-sphinx.yml
**Trigger**: Pull requests to master  
**Purpose**: Verify Sphinx documentation builds successfully

**Steps**:
1. Setup Python 3.11
2. Install documentation requirements
3. Optionally install custom pyOpenMS wheel (via workflow input)
4. Build HTML documentation with `make html`

### 4. test-pr.yaml
**Trigger**: Pull requests to master  
**Purpose**: Test notebook generation for changed RST files

**Steps**:
1. Detect changed RST files using tj-actions/changed-files
2. Setup Pandoc 3.1.2
3. Generate notebooks for changed files
4. Execute generated notebooks to verify they work

### 5. code-blocks-linting.yaml
**Trigger**: Pull requests  
**Purpose**: Lint Python code blocks in RST files

**Steps**:
1. Install blacken-docs
2. Run on changed RST files
3. Check for parse errors
4. Suggest formatting fixes via reviewdog

### 6. flake8 test.yml
**Trigger**: Pull requests  
**Purpose**: Python code quality checks

**Steps**:
1. Run flake8 linter
2. Report violations on PR
3. Fail on new violations

## Development Guide

### Adding New Documentation

1. **Create RST file** in appropriate directory:
   - User guides: `docs/source/user_guide/`
   - API docs: `docs/source/apidocs/`
   - Community docs: `docs/source/community/`

2. **Add to table of contents** in `index.rst`:
```rst
.. toctree::
   :maxdepth: 2
   
   your_new_file
```

3. **Include code examples**:
```rst
.. code-block:: python

   import pyopenms as oms
   # Your code here
```

4. **Test locally**:
```bash
cd docs/
make html
# Open build/html/index.html in browser
```

### Testing Notebooks Locally

1. **Generate notebook from RST**:
```bash
cd docs/source/
pandoc your_file.rst -o your_file.ipynb \
  --filter ../pandoc_filters/code_pandocfilter.py
```

2. **Test execution**:
```bash
jupyter nbconvert --to notebook --execute your_file.ipynb
```

### API Documentation

API documentation is auto-generated using Sphinx autodoc:

1. **Configuration**: `docs/source/apidocs/index.rst`
2. **Templates**: `docs/source/_templates/custom-*.rst`
3. **Build**: Automatically included in `make html`

The autosummary extension recursively documents all pyOpenMS modules and classes.

### Custom Sphinx Extensions

Located in `docs/source/_ext/`:
- **chemrole.py**: Adds chemical formula rendering support
- **glossary_warnings.py**: Validates glossary term usage

## Binder Integration

Binder provides interactive Jupyter environments for documentation:

### Configuration Files

1. **environment.yml**: Conda environment specification
   - Python 3.10
   - Required packages via pip

2. **postBuild**: Post-installation script
   - Installs nightly pyOpenMS from custom PyPI
   - Configures Jupyter settings

3. **jupyter_notebook_config.py**: Jupyter configuration

### Usage

Access notebooks via Binder:
- Latest: https://mybinder.org/v2/gh/OpenMS/pyopenms-docs/master+ipynb
- Specific branch: Replace `master+ipynb` with branch name

## Dependencies

### Documentation Build (docs/requirements.txt)
- **Core**: sphinx==6.1.0, pydata_sphinx_theme
- **Extensions**: sphinx-copybutton, sphinx-hoverxref, sphinx-remove-toctrees
- **Utilities**: ipython, snowballstemmer<3
- **pyOpenMS**: From custom PyPI server

### Runtime/Examples (requirements.txt)
- **Visualization**: matplotlib, plotly, bokeh, holoviews
- **Data Science**: pandas, scikit-learn
- **MS-specific**: massql, pyopenms
- **Utilities**: requests, tabulate, adjustText

## Troubleshooting

### Common Issues

#### 1. Notebook Generation Fails
- **Check Pandoc version**: Must be 3.1.2+
- **Verify filters**: Ensure all pandoc_filters/*.py are present
- **RST syntax**: Validate RST with `rst2html`

#### 2. Sphinx Build Errors
- **Clear cache**: `rm -rf docs/build/`
- **Check imports**: Ensure pyOpenMS is installed
- **Version conflicts**: Review requirements.txt versions

#### 3. CI/CD Failures
- **Notebook tests**: Check for missing dependencies
- **Linting**: Run `blacken-docs` locally
- **PR tests**: Ensure RST files are valid

#### 4. Binder Issues
- **Build logs**: Check Binder build output
- **Environment**: Verify environment.yml syntax
- **postBuild**: Ensure script is executable

### Getting Help

- **Issues**: https://github.com/OpenMS/pyopenms-docs/issues
- **Discord**: https://discord.com/invite/4TAGhqJ7s5
- **Documentation**: https://pyopenms.readthedocs.io/

## Contributing

We welcome contributions! Please:
1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Ensure tests pass locally
5. Submit a pull request

All PRs trigger automated testing for documentation build, notebook generation, and code quality.

## License

See [License.txt](License.txt) for licensing information.
