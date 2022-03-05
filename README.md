# Synapse Notebook Converter

A simple command-line-tool an Python SDK to convert Python files to Synapse Notebooks and vice versa.

## Usage

To convert a Python File to a valid Synapse Notebook, the Python file can contain various Marker comments to

```python
import foo.bar

# ---

print("First Cell Logic")

# ---

print("Second Cell Logic")
```

Speciel Functions:

**Exclude Lines**

```python
# @nb-exclude-begin
print("This code will not)
# @nb-exclude-ende
```

**Markdown**

```python
# @nb-md-begin
# Hello World!
Lorem Ipsum doloir sit amet.
# @nb-md-end
```

**Include Files**

```python
from .some_python import *
```

This will be inserted in the notebook.

## Python SDK

```
import synbconverter as nb

nb.convert_to_nb(source_file = './some_python.py', target_file = './notebooks/some_notebook.json')
nb.convert_to_python(source_file = './notebooks/some_notebook.json', target_file = './some_python.py')
```

## CLI

```bash
synbconvert to-python --source-file '...' --target-file '...'
synbconvert to-notebook --source-file '...' --target-file '...'
```

# Development

`synbconvert` uses [Poetry](https://python-poetry.org/) for dependency management and is packaged with [PyInstaller](https://www.pyinstaller.org/). The minimal requirements for a developer workspace are [Conda](https://docs.conda.io/en/latest/miniconda.html) and [Poetry](https://python-poetry.org/docs/#installation).

```
$ git clone git@github.com:alpine-data/synbconvert.git
$ cd synbconvert
$ conda create -p ./env python=3.8
$ conda activate ./env

$ poetry install
```

For testing we use [Python Behave](https://behave.readthedocs.io/en/stable/index.html). To run the tests, use `poe test` command. Code formatting and static code analysis can be executed with `poe style`.
