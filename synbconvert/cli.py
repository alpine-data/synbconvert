import click

from synbconvert.synbconvert import SynapseNotebookConverter


@click.group()
def cli() -> None:
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
    if source.endswith(".py") and target.endswith(".json"):
        synapse_notebook_converter.convert_python_file_to_synapse_notebook(
            source, target
        )

    if source.endswith(".json") and target.endswith(".py"):
        synapse_notebook_converter.convert_synapse_notebook_to_python_file(
            source, target
        )


cli.add_command(convert)
