import os
import re

from typing import Dict, List

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

        path = os.path.dirname(file)
        new_lines = []
        with open(file) as f:
            lines = f.readlines()
        for line in lines:
            if is_relative_full_import(line):
                filename = f'{line.split(" ")[1][1:]}.py'
                full_path = f'{path}/{filename}'
                new_lines.append(utils.begin_import_marker(full_path))
                # recursively extend the current list by content of relative import
                new_lines.extend(self.read_python_file(full_path))
                new_lines.append(utils.end_import_marker(full_path))
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
        cell_type = get_cell_type(cell)
        cell_content_list = []
        source_lines = cell['source']

        # differentiate between normal cells and ignored content
        if not cell_ignore:
            cell_content_list.append('\n')
            cell_content_list.append(utils.cell_begin_marker(cell_type))
            # markdown content needs to be commented (not executable)
            if cell_type == CellType.MARKDOWN:
                source_lines = utils.comment_lines(source_lines)
            for line in source_lines:
                cell_content_list.append(line)
            # add line break to last line
            if not line.endswith('\n'):
                cell_content_list[-1] = cell_content_list[-1] + '\n'
        else:
            cell_content_list.append('\n')
            cell_content_list.append(utils.begin_ignore_marker())
            # ignored content needs to be uncommented (commented in cell)
            source_lines = utils.uncomment_lines(source_lines)
            # remove ignore tag
            source_lines.pop(0)
            for line in source_lines:
                cell_content_list.append(line)
            # add line break to last line
            if not line.endswith('\n'):
                cell_content_list[-1] = cell_content_list[-1] + '\n'
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

        f = open(file, 'w')
        # remove first line if it contains only a new line
        if lines[0] == '\n': lines.remove(lines[0])

        it = iter(lines)
        for line in it:
            if is_begin_import_line(line):
                import_lines = []
                import_definition = get_import_definition_from_path(line)
                path = os.path.dirname(file)
                file_name = get_file_name_from_import_marker(line)
                if path == '' or path == '.':
                    full_path = f'./{file_name}'
                else:
                    full_path = f'./{path}/{file_name}'
                # collect all lines of the imported file
                for import_line in it:
                    # stop if the correct end import marker is reached
                    if is_end_import_line(import_line) and import_definition == get_import_definition_from_path(import_line):
                        break
                    import_lines.append(import_line)
                f.write(import_definition + '\n')
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

    if cell['cell_type'] == CellType.MARKDOWN.value:
        cell_type = CellType.MARKDOWN
    elif cell['cell_type'] == CellType.CODE.value:
        cell_type = CellType.CODE
    # TODO: handle other cell types

    return cell_type


def get_file_name_from_import_marker(import_marker: str) -> str:
    """
    Determines the file name contained in a import marker.

    :param import_marker: The line which contains the import marker.
    :returns: The file name contained in the import marker.
    """

    begin_import_string = utils.begin_import_marker('')[:-1]
    end_import_string = utils.end_import_marker('')[:-1]
    return os.path.basename(import_marker.replace(begin_import_string, '').replace(end_import_string, '').replace('\n', ''))


def get_import_definition_from_path(path: str) -> str:
    """
    Restores a Python import definition from a given path.

    :param path: The path of the Python file to be imported.
    :returns: The restored Python import definition.
    """

    filename = path.split('/')[-1].replace('.py', '').replace('\n', '')
    import_definition = f'from .{filename} import *'
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

    return bool(re.search('^from \.(\S)+ import \*$', line))


def is_ignored_cell(cell: dict) -> bool:
    """
    Checks if a cell is ignored. A cell is ignored if it contains a ignore marker.

    :param line: The cell to be checked.
    :returns: True if the cell contains a ignore marker and else False.
    """

    if utils.uncomment_lines(cell['source'])[0] == utils.ignore_marker():
        return True
    else:
        return False


def is_begin_import_line(line: str) -> bool:
    """
    Checks if a line contains a begin import marker.

    :param line: The line to be checked.
    :returns: True if the line contains a begin import marker and else False.
    """

    if line.startswith(utils.begin_import_marker('')[:-1]):
        return True
    else:
        return False


def is_end_import_line(line: str) -> bool:
    """
    Checks if a line contains a end import marker.

    :param line: The line to be checked.
    :returns: True if the line contains a end import marker and else False.
    """

    if line.startswith(utils.end_import_marker('')[:-1]):
        return True
    else:
        return False
