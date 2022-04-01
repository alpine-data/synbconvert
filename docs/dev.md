## Install from source

`synbconvert` uses [Poetry](https://python-poetry.org/) for dependency management and is packaged with [PyInstaller](https://pyinstaller.readthedocs.io/en/stable/). The minimal requirements for a developer workspace are [Conda](https://docs.conda.io/en/latest/miniconda.html) and [Poetry](https://python-poetry.org/docs/#installation). To install from source:

```console
$ git clone git@github.com:alpine-data/synbconvert.git
$ cd synbconvert
$ conda create -p ./env python=3.9
$ conda activate ./env

$ poetry install
```

## Testing

For testing we use [Python Behave](https://behave.readthedocs.io/en/stable/index.html). To run the tests, use the `poe test` command. 

## Code quality

Code formatting and static code analysis can be executed with `poe style`.

<br>