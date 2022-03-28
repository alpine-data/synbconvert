import click

from synbconvert.synbconvert import SynapseNotebookConverter


@click.group()
def cli() -> None:
    """
    Defines the click group.
    """

@click.command()
@click.option('--source', help='The path to the file to be converted.')
@click.option('--target', help='The path of the resulting file.')
def convert(source: str, target: str) -> None:
    """
    Command for converting Python files to Synapse notebooks and vice versa.
    """

    synapse_notebook_converter = SynapseNotebookConverter()
    if source.endswith(".py") and target.endswith(".json"):
        synapse_notebook_converter.convert_python_file_to_synapse_notebook(
            source, target
        )

    if source.endswith(".json") and target.endswith(".py"):
        synapse_notebook_converter.convert_synapse_notebook_to_python_file(
            source, target
        )


cli.add_command(convert)
