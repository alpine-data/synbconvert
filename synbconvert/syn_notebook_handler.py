import json
import os

from typing import Dict, List

from synbconvert import utils
from synbconvert.utils import CellType


class SynapseNotebookHandler(object):
    def __init__(self) -> None:
        super(SynapseNotebookHandler, self).__init__()

    def read_synapse_notebook(self, file: str) -> List[Dict]:
        with open(file) as f:
            data = json.load(f)
            cells = data["properties"]["cells"]
        return cells

    def write_synapse_notebook(self, file: str, lines: List[str]) -> None:
        cells = self.create_cells(lines)
        cells = utils.clean_cells(cells)

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

    def create_cells(self, lines: List[str]):
        cells = []
        cell_type = CellType.CODE
        hidden = False
        cell_start_index = 0
        for i, line in enumerate(lines):
            if (line.startswith(utils.cell_begin_marker(CellType.CODE)) or
                line.startswith(utils.cell_begin_marker(CellType.MARKDOWN)) or
                line.startswith(utils.begin_ignore_marker()) or
                line.startswith(utils.end_ignore_marker())):
                cell_end_index = i
                if i > 0:
                    cells.append(self.create_cell(cell_type, lines[cell_start_index:cell_end_index], hidden))
                cell_start_index = i + 1
                cell_type = get_cell_type_from_marker(line)
                hidden = get_cell_hidden_state_from_marker(line)
        # last cell
        cell_end_index = i + 1
        cells.append(self.create_cell(cell_type, lines[cell_start_index:cell_end_index], hidden))
        return cells

    def create_cell(self, cell_type: CellType, source: List[str], hidden: bool, import_cell: bool = False) -> dict:
        source = self.clean_source(source)
        if cell_type == CellType.MARKDOWN:
            source = utils.uncomment_lines(source)
        if hidden == True:
            source.insert(0, utils.ignore_marker())
            source = utils.comment_lines(source)
        cell: dict = {
            "cell_type": cell_type.value, 
            "source": source
        }
        cell["metadata"] = create_cell_metadata(hidden)
        return cell


    def clean_source(self, source: List[str]) -> List[str]:
        # remove leading new lines
        for i in range(len(source)):
            if source[i] == '\n':
                continue
            else:
                break
        # remove ending new lines
        for j in range(len(source)):
            if source[::-1][j] == '\n':
                continue
            else:
                break
        if i != 0 or j != 0:
            source = source[i:-j]
        # remove new line in last line
        if source:
            source[-1] = source[-1].rstrip('\n')
        return source


def create_cell_metadata(hidden: bool) -> dict:
    return {
        "jupyter": {
            "source_hidden": hidden, 
            "outputs_hidden": hidden
        }
    }


def get_cell_type_from_marker(marker: str) -> CellType:
    if marker.startswith(utils.cell_begin_marker(CellType.MARKDOWN)):
        cell_type = CellType.MARKDOWN
    else:
        cell_type = CellType.CODE
    return cell_type


def get_cell_hidden_state_from_marker(marker: str) -> bool:
    if marker.startswith(utils.begin_ignore_marker()):
        hidden = True
    else:
        hidden = False
    return hidden


def create_synapse_notebook_template() -> dict:
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
