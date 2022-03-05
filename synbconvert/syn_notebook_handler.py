import json
import os
from typing import Dict, List

from synbconvert.utils import *


class SynapseNotebookHandler(object):
    def __init__(self):
        super(SynapseNotebookHandler, self).__init__()
        self.cell_types = CellTypes()

    def read_synapse_notebook(self, file: str) -> List[Dict]:
        with open(file) as f:
            data = json.load(f)
            cells = data["properties"]["cells"]
        return cells

    def write_synapse_notebook(self, file: str, lines):
        cells = []
        hidden = False
        for i, line in enumerate(lines):
            if line.startswith(cell_begin_marker(self.cell_types.CODE)):
                hidden = False
                cell_type = self.cell_types.CODE
                cell_start_index = i + 1
            if line.startswith(cell_begin_marker(self.cell_types.MARKDOWN)):
                hidden = False
                cell_type = self.cell_types.MARKDOWN
                cell_start_index = i + 1
            if line.startswith(cell_begin_ignore_marker()):
                hidden = True
                cell_type = self.cell_types.CODE
                cell_start_index = i + 1
            if line.startswith(cell_end_marker(cell_type)) or line.startswith(
                cell_end_ignore_marker()
            ):
                cell_end_index = i
                if cell_type == self.cell_types.MARKDOWN:
                    cells.append(
                        create_cell(
                            cell_type,
                            uncomment_lines(lines[cell_start_index:cell_end_index]),
                            hidden,
                        )
                    )
                else:
                    cells.append(
                        create_cell(
                            cell_type, lines[cell_start_index:cell_end_index], hidden
                        )
                    )

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


def create_cell(cell_type: str, source: List[str], hidden: bool):
    cell = {"cell_type": cell_type, "source": source}
    cell["metadata"] = create_cell_metadata(hidden)
    return cell


def create_cell_metadata(hidden):
    return {"jupyter": {"source_hidden": hidden, "outputs_hidden": hidden}}


def create_synapse_notebook_template():
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
