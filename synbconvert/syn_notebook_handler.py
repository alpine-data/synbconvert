import json
import os
from typing import Any
from typing import Dict
from typing import List
from typing import Optional

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

    def write_synapse_notebook(
        self,
        file: str,
        lines: List[str],
        folder: Optional[str] = None,
        **kwargs: Any,
    ) -> None:
        """
        Writes lines from a Python file to a Synapse notebook.

        Steps:
            1. Create cells from lines (based on markers).
            2. Cleaning cells (removing empty cells etc.)
            3. Write lines to a new or existing Synapse notebook.

        :param file: The relative path (dir + file name) of the Synapse notebook to be written.
        :param lines: The List that contains lines from a Python file.
        :param folder: The path name of the synapse folder property of a Synapse resource.
        """

        cells = self.__create_cells(lines)
        cells = utils.clean_cells(cells)

        # write cells to existing notebook if the notebook already exists
        if os.path.isfile(file):
            with open(file) as f:
                data = json.load(f)
                data["properties"]["cells"] = cells
                if folder is not None:
                    data["properties"]["folder"] = {"name": folder}

                if kwargs is not None:

                    for k, v in kwargs.items():
                        if k in data["properties"]["sessionProperties"]:
                            data["properties"]["sessionProperties"][k] = v
                        elif k in data["properties"]["metadata"]:
                            data["properties"]["metadata"][k] = v
                        elif k == "dynamicAllocationEnabled":
                            data["properties"]["sessionProperties"]["conf"][
                                "spark.dynamicAllocation.enabled"
                            ] = v
                        elif k == "dynamicAllocationMinExecutors":
                            data["properties"]["sessionProperties"]["conf"][
                                "spark.dynamicAllocation.minExecutors"
                            ] = v
                        elif k == "dynamicAllocationMaxExecutors":
                            data["properties"]["sessionProperties"]["conf"][
                                "spark.dynamicAllocation.maxExecutors"
                            ] = v
                        elif k == "targetSparkConfigurationName":
                            data["properties"]["targetSparkConfiguration"] = {
                                "referenceName": v,
                                "type": "SparkConfigurationReference",
                            }
                            data["properties"]["metadata"][
                                "targetSparkConfiguration"
                            ] = v

            with open(file, "w") as f:
                json.dump(data, f, indent=4)
        else:
            data = create_synapse_notebook_template(**kwargs)  # typ
            data["name"] = os.path.splitext(os.path.basename(file))[0]
            data["properties"]["cells"] = cells
            if folder is not None:
                data["properties"]["folder"] = {"name": folder}
            with open(file, "w") as f:
                json.dump(data, f, indent=4)

    def __create_cells(self, lines: List[str]) -> List[Dict]:
        """
        Creates Synapse notebook cells from a List of lines. The List of lines should contain markers.

        :param lines: The List that contains lines from a Python file.
        :returns: The List of Synapse notebook cells.
        """

        # initial cell stats
        cells = []
        cell_type = CellType.CODE
        ignore = False
        hidden = False
        cell_start_index = 0

        for i, line in enumerate(lines):
            if (
                line.startswith(utils.cell_marker(CellType.CODE))
                or line.startswith(utils.cell_marker(CellType.CODE, hidden=True))
                or utils.cell_marker(CellType.MARKDOWN) in line
                or line.startswith(utils.begin_ignore_marker())
                or line.startswith(utils.end_ignore_marker())
                or (line.startswith('"""') and cell_type == CellType.MARKDOWN)
            ):
                cell_end_index = i
                cells.append(
                    self.__create_cell(
                        cell_type,
                        lines[cell_start_index:cell_end_index],
                        ignore,
                        hidden,
                    )
                )
                cell_start_index = i + 1
                cell_type = get_cell_type_from_marker(line)
                ignore = get_cell_ignore_state_from_marker(line)
                hidden = get_cell_hidden_state_from_marker(line)
        # append last cell
        cell_end_index = i + 1
        cells.append(
            self.__create_cell(
                cell_type, lines[cell_start_index:cell_end_index], ignore, hidden
            )
        )
        return cells

    @staticmethod
    def __create_cell(
        cell_type: CellType, source: List[str], ignore: bool, hidden: bool
    ) -> dict:
        """
        Creates a Synapse notebook cell from a List of lines that defines the cell.

        :param cell_type: The CellType of the cell.
        :param source: The source content of the cell.
        :param ignore: The flag that determines whether a cell is ignored or not.
        :returns: The Synapse notebook cell.
        """

        source = clean_source(source)
        if cell_type == CellType.MARKDOWN:
            # markdown needs to be uncommented in the cell
            source = utils.uncomment_lines(source)
            source = clean_source(source)
        if ignore:
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
    source = list([line.rstrip() for line in source])
    source = "\n".join(source).strip().split("\n")
    source = list([f"{line}\n" for line in source])

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


def get_cell_ignore_state_from_marker(marker: str) -> bool:
    """
    Determines whether a cell marker reflects a ignore property or not.

    :param marker: The marker to be examined.
    :returns: The determined ignore state.
    """

    if marker.startswith(utils.begin_ignore_marker()):
        ignore = True
    else:
        ignore = False
    return ignore


def get_cell_hidden_state_from_marker(marker: str) -> bool:
    """
    Determines whether a cell marker reflects a hidden property or not.

    :param marker: The marker to be examined.
    :returns: The determined hidden state.
    """

    if marker.startswith(
        utils.cell_marker(CellType.CODE, hidden=True)
    ) or marker.startswith(utils.begin_ignore_marker()):
        hidden = True
    else:
        hidden = False
    return hidden


def create_synapse_notebook_template(
    enableDebugMode: bool = False,
    dynamicAllocationEnabled: str = "false",
    numExecutors: int = 2,
    dynamicAllocationMinExecutors: Optional[int] = None,
    dynamicAllocationMaxExecutors: Optional[int] = None,
    sessionKeepAliveTimeout: int = 30,
    runAsWorkspaceSystemIdentity: bool = False,
    targetSparkConfigurationName: Optional[str] = None,
) -> dict:
    """
    Creates the base Dict of a Synapse notebook.

    :returns: The base Dict of a Synapse notebook.
    """

    if (
        dynamicAllocationEnabled == "false"
        or (dynamicAllocationMinExecutors is None)
        or (dynamicAllocationMaxExecutors is None)
    ):
        dynamicAllocationMinExecutors = numExecutors
        dynamicAllocationMaxExecutors = numExecutors

    result: dict = {
        "name": "",
        "properties": {
            "nbformat": 4,
            "nbformat_minor": 2,
            "bigDataPool": {"referenceName": "poolS", "type": "BigDataPoolReference"},
            "sessionProperties": {
                "driverMemory": "28g",
                "driverCores": 4,
                "executorMemory": "28g",
                "executorCores": 4,
                "numExecutors": numExecutors,
                "runAsWorkspaceSystemIdentity": runAsWorkspaceSystemIdentity,
                "conf": {
                    "spark.dynamicAllocation.enabled": dynamicAllocationEnabled,
                    "spark.dynamicAllocation.minExecutors": dynamicAllocationMinExecutors,
                    "spark.dynamicAllocation.maxExecutors": dynamicAllocationMaxExecutors,
                    "spark.autotune.trackingId": "",
                },
            },
            "metadata": {
                "saveOutput": True,
                "enableDebugMode": enableDebugMode,
                "kernelspec": {"name": "synapse_pyspark", "display_name": "python"},
                "language_info": {"name": "python"},
                "sessionKeepAliveTimeout": sessionKeepAliveTimeout,
            },
            "cells": [],
        },
    }

    if targetSparkConfigurationName:
        result["properties"]["targetSparkConfiguration"] = {
            "referenceName": targetSparkConfigurationName,
            "type": "SparkConfigurationReference",
        }

        result["properties"]["metadata"][
            "targetSparkConfiguration"
        ] = targetSparkConfigurationName

    return result
