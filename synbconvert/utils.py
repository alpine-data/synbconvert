from enum import Enum
from typing import Dict
from typing import List


class CellType(Enum):
    """
    Cell types enumeration.
    """

    CODE = "code"
    MARKDOWN = "markdown"


def cell_marker(cell_type: CellType = CellType.CODE, hidden: bool = False) -> str:
    """
    Creates a cell begin marker based on the type of the cell.

    :param cell_type: The type of a cell.
    :returns: The cell type specific cell begin marker.
    """

    if cell_type == CellType.CODE and hidden is False:
        marker = "# nb--cell\n"
    elif cell_type == CellType.CODE and hidden is True:
        marker = "# nb--hidden\n"
    elif cell_type == CellType.MARKDOWN:
        marker = "nb--markdown\n"
    return marker
    # TODO: include other cell types


def ignore_marker() -> str:
    """
    Creates an ignore marker.

    :returns: The ignore marker.
    """

    return "nb--ignore\n"


def begin_ignore_marker() -> str:
    """
    Creates an begin ignore marker.

    :returns: The begin ignore marker.
    """

    return "# nb--ignore-begin\n"


def end_ignore_marker() -> str:
    """
    Creates an end ignore marker.

    :returns: The end ignore marker.
    """

    return "# nb--ignore-end\n"


def begin_import_marker(import_file: str) -> str:
    """
    Creates an begin import marker based on the import file path.

    :param import_file: The path of the import file.
    :returns: The begin import marker.
    """

    return f'# nb--import-begin "{import_file}"\n'


def end_import_marker(import_file: str) -> str:
    """
    Creates an end import marker based on the import file path.

    :param import_file: The path of the import file.
    :returns: The end import marker.
    """

    return f'# nb--import-end "{import_file}"\n'


def comment_lines(lines: List[str]) -> List[str]:
    """
    Adds a multi line comment to a List of source lines.

    :param lines: The source lines to be commented.
    :returns: The commented List of of source lines.
    """

    lines[0] = f'"""{lines[0]}'
    if not lines[-1].endswith("\n"):
        lines[-1] += "\n"
    lines[-1] = f'{lines[-1]}"""'
    return lines


def uncomment_lines(lines: List[str]) -> List[str]:
    """
    Removes a multi line comment from a List of source lines.

    :param lines: The source lines to be uncommented.
    :returns: The uncommented List of of source lines.
    """

    lines[0] = lines[0].lstrip('"')
    lines[-1] = lines[-1].rstrip('"')
    lines[0] = lines[0].lstrip("'")
    lines[-1] = lines[-1].rstrip("'")
    return lines


def clean_cells(cells: List[Dict]) -> List[Dict]:
    """
    Removes empty Synapse notebook cells from a List of cells.

    :param cells: The List of Synapse notebook cells to be cleaned.
    :returns: The cleaned List of Synapse notebook cells.
    """

    for cell in cells:
        if not cell["source"]:
            cells.remove(cell)
        if len(cell["source"]) == 1 and cell["source"][0] == "":
            cells.remove(cell)
    return cells
