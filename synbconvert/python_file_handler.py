from typing import Dict, List
from synbconvert.utils import *


class PythonFileHandler(object):
    def __init__(self):
        super(PythonFileHandler, self).__init__()
        self.cell_types = CellTypes()

    def read_python_file(self, file: str):
        with open(file) as f:
            lines = f.readlines()
        return lines

    def write_python_file(self, file: str, cells: List[Dict]) -> None:
        f = open(file, 'w')
        for cell in cells:
            if cell['cell_type'] == self.cell_types.MARKDOWN:
                self.write_markdown(f, cell, self.cell_types.MARKDOWN)
            if cell['cell_type'] == self.cell_types.CODE:
                self.write_code(f, cell, self.cell_types.CODE)
        f.close()

    def write_code(self, f, cell: Dict, cell_type: str) -> None:
        source_lines = cell['source']
        f.write(cell_begin_marker(cell_type))
        for line in source_lines:
            f.write(line)
        if not line.endswith('\n'):
            f.write('\n')
        f.write(cell_end_marker(cell_type))
    
    def write_markdown(self, f, cell: Dict, cell_type: str) -> None:
        source_lines = cell['source']
        f.write(cell_begin_marker(cell_type))
        for line in source_lines:
            f.write(comment_line(line))
        if not line.endswith('\n'):
            f.write('\n')
        f.write(cell_end_marker(cell_type))


def comment_line(line: str):
    line = f'# {line}'
    return line
