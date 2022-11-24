import click

from synbconvert.synbconvert import SynapseNotebookConverter


@click.group()
def synbconvert() -> None:
    """
    Defines the click group.
    """


@click.command()
@click.option("--source", help="The path to the file to be converted.")
@click.option("--target", help="The path of the resulting file.")
def convert(source: str, target: str) -> None:
    """
    Command for converting Python files to Synapse notebooks and vice versa.
    """

    synapse_notebook_converter = SynapseNotebookConverter()
    synapse_notebook_converter.convert(source, target)


synbconvert.add_command(convert)
