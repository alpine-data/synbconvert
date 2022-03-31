import click

from synbconvert.synbconvert import SynapseNotebookConverter


@click.group()
def synbconvert() -> None:
    """
    Defines the click group.
    """


@click.command()
@click.argument("source")
@click.argument("target")
def convert(source: str, target: str) -> None:
    """
    Defines the click command for converting Python files to Synapse notebooks and vice versa.

    :param source: The file to be converted.
    :param target: The path of the resulting file.
    """

    synapse_notebook_converter = SynapseNotebookConverter()
    synapse_notebook_converter.convert(source, target)


synbconvert.add_command(convert)
