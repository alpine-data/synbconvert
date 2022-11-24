import os
import re
from typing import Dict
from typing import List

from synbconvert import utils
from synbconvert.utils import CellType


class PythonFileHandler(object):
    """
    This class is responsible for reading and writing Python files.
    """

    def __init__(self) -> None:
        super(PythonFileHandler, self).__init__()

    def read_python_file(self, file: str) -> List[str]:
        """
        Reads a Python file line by line and returns all lines as a List.

        The content of relative imports is also recursively added to the List.
        Added imports:
            from .my_module import *
        Not added imports:
            from any_module import *
            from .my_module import my_method
            from .my_module import MyClass

        :param file: The relative path (dir + file name) of the Python file to be read.
        :returns: The list of all lines which are contained in the Python file.
        """

        new_lines = []
        file_path = os.path.dirname(os.path.relpath(file))
        with open(file) as f:
            lines = f.readlines()
        for line in lines:
            if is_relative_full_import(line):
                import_path = get_file_path_from_import_definition(line)
                # join import path with relative file path

                if import_path.startswith("//"):
                    steps_up = 0
                    for _ in import_path:
                        steps_up += 1

                #    steps_up = [i for i in ]

                if file_path == "":
                    full_path = f".{import_path}"
                else:
                    full_path = f"./{file_path}{import_path}"
                import_path = f".{import_path}"
                new_lines.append(utils.begin_import_marker(import_path))
                # recursively extend the current list by content of relative import
                new_lines.extend(self.read_python_file(full_path))
                new_lines.append(utils.end_import_marker(import_path))
            else:
                new_lines.append(line)
        return new_lines

    def write_python_file(self, file: str, cells: List[Dict]) -> None:
        """
        Writes Synapse notebook cells to a Python file.

        Steps:
            1. Cleaning cells (removing empty cells etc.)
            2. Writing the content of the cells to a List (also adding markers and formatting)
            3. Write lines to Python file (also write to imported files)

        :param file: The relative path (dir + file name) of the Python file to be written.
        :param cells: The List that contains Synapse notebook cells.
        """

        cells = utils.clean_cells(cells)
        lines = []
        for cell in cells:
            lines.extend(self.__cell_content_to_list(cell))
        self.__write_lines(file, lines)

    @staticmethod
    def __cell_content_to_list(cell: Dict) -> List[str]:
        """
        Returns source of a Synapse notebook cell and also adds markers and formatting.

        Examplary structure of a cell Dict:
            {
                "cell_type": "code",
                "source": [
                    "print(\"Hello World\")"
                ],
                "metadata": {
                    "jupyter": {
                        "source_hidden": false,
                        "outputs_hidden": false
                    }
                }
            }

        :param cell: The synapse notebook cell.
        :returns: The source of a Synapse notebook cell including markers and formatting
        """

        cell_ignore = is_ignored_cell(cell)
        cell_hidden = is_hidden_cell(cell)
        cell_type = get_cell_type(cell)
        cell_content_list = []
        source_lines = cell["source"]

        # differentiate between normal cells and ignored content
        if not cell_ignore:
            cell_content_list.append("\n")
            # markdown content needs to be commented (not executable)
            if cell_type == CellType.MARKDOWN:
                source_lines.insert(0, utils.cell_marker(cell_type))
                source_lines = utils.comment_lines(source_lines)
            else:
                cell_content_list.append(utils.cell_marker(cell_type, cell_hidden))
            for line in source_lines:
                cell_content_list.append(line)
            # add line break to last line
            if not line.endswith("\n"):
                cell_content_list[-1] = cell_content_list[-1] + "\n"
        else:
            cell_content_list.append("\n")
            cell_content_list.append(utils.begin_ignore_marker())
            # ignored content needs to be uncommented (commented in cell)
            source_lines = utils.uncomment_lines(source_lines)
            # remove ignore tag
            source_lines.pop(0)
            for line in source_lines:
                cell_content_list.append(line)
            # add line break to last line
            if not line.endswith("\n"):
                cell_content_list[-1] = cell_content_list[-1] + "\n"
            line = utils.end_ignore_marker()
            cell_content_list.append(line)
        return cell_content_list

    def __write_lines(self, file: str, lines: List[str]) -> None:
        """
        Writes the given lines to the Python file. The content of relative imports is also
        recursively written to imported Python files.

        :param file: The relative path (dir + file name) of the Python file to be written.
        :param lines: The List of lines to be written to the Python file.
        """

        file_path = os.path.dirname(os.path.relpath(file))
        if not file_path == "" and not os.path.exists(file_path):
            os.makedirs(file_path)
        f = open(file, "w")
        # remove first line if it contains only a new line
        if lines[0] == "\n":
            lines.remove(lines[0])
        # remove first line if it contains only a nb-cell marker
        if lines[0] == utils.cell_marker(CellType.CODE):
            lines.remove(lines[0])

        it = iter(lines)
        for line in it:
            if is_begin_import_line(line):
                import_lines = []
                import_definition = get_import_definition_from_import_marker(line)
                import_path = get_file_path_from_import_definition(import_definition)
                # join import path with relative file path
                if file_path == "":
                    full_path = f".{import_path}"
                else:
                    full_path = f"./{file_path}{import_path}"
                # collect all lines of the imported file
                for import_line in it:
                    # stop if the correct end import marker is reached
                    if is_end_import_line(
                        import_line
                    ) and import_definition == get_import_definition_from_import_marker(
                        import_line
                    ):
                        break
                    import_lines.append(import_line)
                f.write(import_definition + "\n")
                # recursively write the lines of the imported file
                self.__write_lines(full_path, import_lines)
            else:
                f.write(line)
        f.close()


def get_cell_type(cell: dict) -> CellType:
    """
    Returns the CellType of a cell.

    :param cell: The cell for which the type is to be determined.
    :returns: The CellType of the cell.
    """

    if cell["cell_type"] == CellType.MARKDOWN.value:
        cell_type = CellType.MARKDOWN
    elif cell["cell_type"] == CellType.CODE.value:
        cell_type = CellType.CODE
    # TODO: handle other cell types

    return cell_type


def get_file_path_from_import_definition(import_definition: str) -> str:
    """
    Determines the file path of an imported file from a Python import definition.

    :param import_marker: The line which contains the Python import definition.
    :returns: The file path of the imported file.
    """

    path = import_definition.split(" ")[1].replace(".", "/")
    path = f"{os.path.dirname(path)}"
    if path == "/":
        path = ""
    filename = import_definition.split(" ")[1].split(".")[-1]
    filename = f"{filename}.py"
    import_path = f"{path}/{filename}"
    return import_path


def get_import_definition_from_import_marker(import_marker: str) -> str:
    """
    Restores a Python import definition from a given import marker.

    :param import_marker: The import marker String containing the path to be imported.
    :returns: The restored Python import definition.
    """

    module_path = (
        import_marker.split(" ")[2]
        .replace('"', "")
        .replace("./", "")
        .replace(".py", "")
        .replace("\n", "")
        .replace("/", ".")
    )
    import_definition = f"from .{module_path} import *"
    return import_definition


def is_relative_full_import(line: str) -> bool:
    """
    Checks if a Python import definition is a relative full import.

    Example of a relative full import:
        from .my_module import *
    The following imports are not relative:
        from any_module import *
    The following imports are not full:
        from .my_module import my_method
        from .my_module import MyClass

    :param line: The line to be checked.
    :returns: True if the import definition is a relative full import and else False.
    """

    return bool(re.search(r"^from \.(\S)+ import \*$", line))


def is_ignored_cell(cell: dict) -> bool:
    """
    Checks if a cell is ignored. A cell is ignored if it contains a ignore marker.

    :param line: The cell to be checked.
    :returns: True if the cell contains a ignore marker and else False.
    """

    if utils.uncomment_lines(cell["source"])[0] == utils.ignore_marker():
        return True
    else:
        return False


def is_hidden_cell(cell: dict) -> bool:
    """
    Checks if a cell is hidden.

    :param line: The cell to be checked.
    :returns: True if the cell contains is hidden.
    """

    try:
        if cell["metadata"]["jupyter"]["source_hidden"] is True:
            return True
        else:
            return False
    except KeyError:
        return False


def is_begin_import_line(line: str) -> bool:
    """
    Checks if a line contains a begin import marker.

    :param line: The line to be checked.
    :returns: True if the line contains a begin import marker and else False.
    """

    if line.startswith(utils.begin_import_marker("")[:-3]):
        return True
    else:
        return False


def is_end_import_line(line: str) -> bool:
    """
    Checks if a line contains a end import marker.

    :param line: The line to be checked.
    :returns: True if the line contains a end import marker and else False.
    """

    if line.startswith(utils.end_import_marker("")[:-3]):
        return True
    else:
        return False
