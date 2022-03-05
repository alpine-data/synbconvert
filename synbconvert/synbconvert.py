from synbconvert.python_file_handler import PythonFileHandler
from synbconvert.syn_notebook_handler import SynapseNotebookHandler


class SynapseNotebookConverter(SynapseNotebookHandler, PythonFileHandler):
    def __init__(self):
        super(SynapseNotebookConverter, self).__init__()

    def convert_synapse_notebook_to_python_file(
        self, notebook_file: str, python_file: str
    ):
        cells = self.read_synapse_notebook(notebook_file)
        self.write_python_file(python_file, cells)

    def convert_python_file_to_synapse_notebook(
        self, python_file: str, notebook_file: str
    ):
        lines = self.read_python_file(python_file)
        self.write_synapse_notebook(notebook_file, lines)
