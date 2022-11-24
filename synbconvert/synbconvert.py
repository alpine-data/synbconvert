from typing import Any
from typing import Optional

from synbconvert.python_file_handler import PythonFileHandler
from synbconvert.syn_notebook_handler import SynapseNotebookHandler


class SynapseNotebookConverter(SynapseNotebookHandler, PythonFileHandler):
    """
    This class is responsible for converting Python files to Synapse notebooks and vice versa.
    """

    def __init__(self) -> None:
        super(SynapseNotebookConverter, self).__init__()

    def convert_synapse_notebook_to_python_file(
        self, notebook_file: str, python_file: str
    ) -> None:
        """
        Converts a Synapse notebook into a Python file.

        :param notebook_file: The Synapse notebook to be converted.
        :param python_file: The path of the resulting Python file.
        """

        cells = self.read_synapse_notebook(notebook_file)
        self.write_python_file(python_file, cells)

    def convert_python_file_to_synapse_notebook(
        self,
        python_file: str,
        notebook_file: str,
        folder: Optional[str] = None,
        **kwargs: Any
    ) -> None:
        """
        Converts a Python file into a Synapse notebook.

        :param python_file: The Python file to be converted.
        :param notebook_file: The path of the resulting Synapse notebook.
        :param folder: The path name of the synapse folder property of a Synapse resource.
        """

        lines = self.read_python_file(python_file)
        self.write_synapse_notebook(notebook_file, lines, folder, **kwargs)

    def convert(self, source: str, target: str, folder: Optional[str] = None) -> None:
        """
        Converts a source file into a target file.

        :param source: The file to be converted.
        :param target: The path of the resulting file.
        :param folder: The path name of the synapse folder property of a Synapse resource.
        """
        if source.endswith(".py") and target.endswith(".json"):
            self.convert_python_file_to_synapse_notebook(source, target, folder)

        if source.endswith(".json") and target.endswith(".py"):
            self.convert_synapse_notebook_to_python_file(source, target)
