from typing import Dict, List, TextIO

from synbconvert.utils import *


class PythonFileHandler(object):
    def __init__(self) -> None:
        super(PythonFileHandler, self).__init__()

    def read_python_file(self, file: str) -> List[str]:
        with open(file) as f:
            lines = f.readlines()
        return lines

    def write_python_file(self, file: str, cells: List[dict]) -> None:
        f = open(file, "w")
        for cell in cells:
            if cell['cell_type'] == CellType.MARKDOWN.value:
                cell_type = CellType.MARKDOWN
            elif cell['cell_type'] == CellType.CODE.value:
                if get_cell_hidden_state(cell):
                    cell_type = CellType.IGNORE
                else:
                    cell_type = CellType.CODE
            self.write_cell_content(f, cell, cell_type)
        f.close()

    def write_cell_content(self, f: TextIO, cell: Dict, cell_type: str) -> None:
        source_lines = cell['source']
        f.write(cell_begin_marker(cell_type))
        for line in source_lines:
            if cell_type == CellType.IGNORE:
                f.write(uncomment_line(line))
            elif cell_type == CellType.MARKDOWN:
                f.write(comment_line(line))
            elif cell_type == CellType.CODE:
                f.write(line)
        if not line.endswith('\n'):
            f.write('\n')
        f.write('\n')

def get_cell_hidden_state(cell: dict) -> bool:
    try:
        hidden = cell["metadata"]["jupyter"]["source_hidden"]
    except KeyError:
        hidden = False
    return hidden
