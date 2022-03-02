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
            cells = data['properties']['cells']
        return cells

    def write_synapse_notebook(self, file: str, lines):
        cells = []
        for i, line in enumerate(lines):
            if line.startswith(cell_begin_marker(self.cell_types.CODE)):
                cell_type = self.cell_types.CODE
                cell_start_index = i + 1
            if line.startswith(cell_begin_marker(self.cell_types.MARKDOWN)):
                cell_type = self.cell_types.MARKDOWN
                cell_start_index = i + 1
            if line.startswith(cell_end_marker(cell_type)):
                cell_end_index = i
                cells.append(create_cell(cell_type, lines[cell_start_index:cell_end_index]))

        if os.path.isfile(file):
            with open(file) as f:
                data = json.load(f)
                data['properties']['cells'] = cells
            
            with open(file, 'w') as f:
                json.dump(data, f)
        else:
            data = create_synapse_notebook_template()
            data['name'] = os.path.splitext(os.path.basename(file))[0]
            data['properties']['cells'] = cells
            with open(file, 'w') as f:
                json.dump(data, f)


def create_cell(cell_type: str, source: List[str]):
    return {
        'cell_type': cell_type,
        'source': source
    }


def create_synapse_notebook_template():
    return {
        'name': '',
        'properties': {
            'folder': {},
            'nbformat': 0,
            'nbformat_minor': 0,
            'sessionProperties': {},
            'metadata': {},
            'cells': []
        }
    }
