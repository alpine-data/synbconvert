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
