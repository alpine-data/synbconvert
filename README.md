# Synapse Notebook Converter

A simple command-line-tool an Python SDK to convert Python files to Synapse notebooks and vice versa.

## Usage

To convert a Python file to a valid Synapse notebook, the Python file can be augmented with different markers. If no marker is used, the content of the Python file is interpreted as a single code cell.

**Defining Code Cells**

Code cells are denoted by `# nb--cell` markers. All lines below the marker until the next marker are added to a code cell in the Synapse notebook. The lines above the fist marker are also added to a code cell.

```python
import foo.bar

# nb--cell
print("first cell logic")

# nb--cell
print("second cell logic")
```

**Exclude Lines**

To exclude lines from beeing executed in the Synapse notebook, enclose them in an opening `# nb--ignore-begin` and closing `# nb--ignore-end` marker.

```python
# nb--ignore-begin
print("this code will not be executed in the notebook")
# nb--ignore-end
```

**Markdown**

Markdown is not executed in the Python file but should be shown as formatted text in the Synapse notebook. To define markdown cells, use a docsting comment with a `nb--markdown` marker. 

```python
"""nb--markdown
## Markdown Heading
These lines are not executed in the Python file,
but shown as markdown in the Synapse notebook. 
"""
```

**Include Files**

By converting, the content of imported modules is included in the Synapse notebook (works only with full relative imports). When converting the notebook back to a Python file, relatively imported modules are also written.

```python
# these imports are included in the notebook
from .some_module import *
from .some_package.some_module import *
from .some_package.some_sub_package.some_module import *

# these imports are not included in the notebook
from some_module import *               # not relative
from .some_module import some_method    # not full
from .some_module import SomeClass      # not full
```

## Python SDK
The Python SDK can be used as follows:

```python
import synbconverter as nc

# convert from Python file to Synapse notebook
convert_python_file_to_synapse_notebook(python_file='./some_python.py', notebook_file='./notebooks/some_notebook.json')

# convert from Synapse notebook to Python file
convert_synapse_notebook_to_python_file(notebook_file='./notebooks/some_notebook.json', python_file='./some_python.py''')
```

## CLI
The easy CLI can be used as follows:

```console
$ synbconvert convert <your_source_file_path> <your_target_file_path>
cd
```

## Development

`synbconvert` uses [Poetry](https://python-poetry.org/) for dependency management and is packaged with [PyInstaller](https://pyinstaller.readthedocs.io/en/stable/). The minimal requirements for a developer workspace are [Conda](https://docs.conda.io/en/latest/miniconda.html) and [Poetry](https://python-poetry.org/docs/#installation).

```console
$ git clone git@github.com:alpine-data/synbconvert.git
$ cd synbconvert
$ conda create -p ./env python=3.9
$ conda activate ./env

$ poetry install
```

For testing we use [Python Behave](https://behave.readthedocs.io/en/stable/index.html). To run the tests, use `poe test` command. Code formatting and static code analysis can be executed with `poe style`.
