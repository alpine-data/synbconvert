import json
import os
from typing import Dict
from typing import List

from synbconvert import utils
from synbconvert.utils import CellType


class SynapseNotebookHandler(object):
    """
    This class is responsible for reading and writing Synapse notebooks.
    """

    def __init__(self) -> None:
        super(SynapseNotebookHandler, self).__init__()

    def read_synapse_notebook(self, file: str) -> List[Dict]:
        """
        Reads cells from a Synapse notebook. Notebook metadata is ignored.

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

        :param file: The relative path (dir + file name) of the Synapse notebook to be read.
        :returns: The list of all cells which are contained in the Synapse notebook.
        """

        with open(file) as f:
            data = json.load(f)
            cells = data["properties"]["cells"]
        return cells

    def write_synapse_notebook(self, file: str, lines: List[str]) -> None:
        """
        Writes lines from a Python file to a Synapse notebook.

        Steps:
            1. Create cells from lines (based on markers).
            2. Cleaning cells (removing empty cells etc.)
            3. Write lines to a new or existing Synapse notebook.

        :param file: The relative path (dir + file name) of the Synapse notebook to be written.
        :param lines: The List that contains lines from a Python file.
        """

        cells = self.__create_cells(lines)
        cells = utils.clean_cells(cells)

        # write cells to existing notebook if the notebook already exists
        if os.path.isfile(file):
            with open(file) as f:
                data = json.load(f)
                data["properties"]["cells"] = cells

            with open(file, "w") as f:
                json.dump(data, f)
        else:
            data = create_synapse_notebook_template()
            data["name"] = os.path.splitext(os.path.basename(file))[0]
            data["properties"]["cells"] = cells
            with open(file, "w") as f:
                json.dump(data, f)

    def __create_cells(self, lines: List[str]) -> List[Dict]:
        """
        Creates Synapse notebook cells from a List of lines. The List of lines should contain markers.

        :param lines: The List that contains lines from a Python file.
        :returns: The List of Synapse notebook cells.
        """

        # initial cell stats
        cells = []
        cell_type = CellType.CODE
        hidden = False
        cell_start_index = 0

        for i, line in enumerate(lines):
            if (
                line.startswith(utils.cell_marker(CellType.CODE))
                or utils.cell_marker(CellType.MARKDOWN) in line
                or line.startswith(utils.begin_ignore_marker())
                or line.startswith(utils.end_ignore_marker())
            ):
                cell_end_index = i
                # ignore first line marker
                if i > 0:
                    cells.append(
                        self.__create_cell(
                            cell_type, lines[cell_start_index:cell_end_index], hidden
                        )
                    )
                cell_start_index = i + 1
                cell_type = get_cell_type_from_marker(line)
                hidden = get_cell_hidden_state_from_marker(line)
        # append last cell
        cell_end_index = i + 1
        cells.append(
            self.__create_cell(
                cell_type, lines[cell_start_index:cell_end_index], hidden
            )
        )
        return cells

    @staticmethod
    def __create_cell(cell_type: CellType, source: List[str], hidden: bool) -> dict:
        """
        Creates a Synapse notebook cell from a List of lines that defines the cell.

        :param cell_type: The CellType of the cell.
        :param source: The source content of the cell.
        :param hidden: The flag that determines whether a cell is hidden or not.
        :returns: The Synapse notebook cell.
        """

        source = clean_source(source)
        if cell_type == CellType.MARKDOWN:
            # markdown needs to be uncommented in the cell
            source = utils.uncomment_lines(source)
            source = clean_source(source)
        if hidden:
            # ignore marker needs to be added in the cell
            source.insert(0, utils.ignore_marker())
            source = utils.comment_lines(source)
        cell: dict = {"cell_type": cell_type.value, "source": source}
        cell["metadata"] = create_cell_metadata(hidden)
        return cell


def clean_source(source: List[str]) -> List[str]:
    """
    Cleans the source content of a Synapse notebook cell.

    :param source: The source content of the cell.
    :returns: The cleaned source content of the cell.
    """

    # remove leading new lines
    for i in range(len(source)):
        if source[i] == "\n" or source[i] == "":
            continue
        else:
            break
    source = source[i:]

    # remove ending new lines
    for j in range(len(source)):
        if source[::-1][j] == "\n" or source[::-1][j] == "":
            continue
        else:
            break

    if i != 0 or j != 0:
        if j > 0:
            source = source[i:-j]
        else:
            source = source[i:]

    # remove new line in last line
    if source:
        source[-1] = source[-1].rstrip("\n")
    return source


def create_cell_metadata(hidden: bool) -> dict:
    """
    Creates the metadata Dict of a Synapse notebook cell.

    :param hidden: The flag that determines whether a cell is hidden or not.
    :returns: The metadata Dict of a Synapse notebook cell.
    """

    return {"jupyter": {"source_hidden": hidden, "outputs_hidden": hidden}}


def get_cell_type_from_marker(marker: str) -> CellType:
    """
    Determines the CellType of a cell marker.

    :param marker: The marker to be examined.
    :returns: The CellType of the cell marker.
    """

    if utils.cell_marker(CellType.MARKDOWN) in marker:
        cell_type = CellType.MARKDOWN
    else:
        cell_type = CellType.CODE
    return cell_type


def get_cell_hidden_state_from_marker(marker: str) -> bool:
    """
    Determines whether a cell marker reflects a hidden property or not.

    :param marker: The marker to be examined.
    :returns: The determined hidden state.
    """

    if marker.startswith(utils.begin_ignore_marker()):
        hidden = True
    else:
        hidden = False
    return hidden


def create_synapse_notebook_template() -> dict:
    """
    Creates the base Dict of a Synapse notebook.

    :returns: The base Dict of a Synapse notebook.
    """

    return {
        "name": "",
        "properties": {
            "nbformat": 4,
            "nbformat_minor": 2,
            "sessionProperties": {
                "driverMemory": "28g",
                "driverCores": 4,
                "executorMemory": "28g",
                "executorCores": 4,
                "numExecutors": 2,
                "conf": {
                    "spark.dynamicAllocation.enabled": "false",
                    "spark.dynamicAllocation.minExecutors": "2",
                    "spark.dynamicAllocation.maxExecutors": "2",
                    "spark.autotune.trackingId": "",
                },
            },
            "metadata": {
                "saveOutput": True,
                "enableDebugMode": False,
                "kernelspec": {"name": "synapse_pyspark", "display_name": "python"},
                "language_info": {"name": "python"},
                "sessionKeepAliveTimeout": 30,
            },
            "cells": [],
        },
    }
