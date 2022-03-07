from typing import Dict, List, TextIO

from synbconvert import utils
from synbconvert.utils import CellType


class PythonFileHandler(object):
    def __init__(self) -> None:
        super(PythonFileHandler, self).__init__()

    def read_python_file(self, file: str) -> List[str]:
        with open(file) as f:
            lines = f.readlines()
        return lines

    # def read_python_file(self, file: str):
    #     path = os.path.dirname(file)
    #     new_list = []
    #     with open(file) as f:
    #         lines = f.readlines()
    #         # new_list.append(line)
    #     for line in lines:
    #         if line.startswith('from .'):
    #             filename = f'{line.split(" ")[1][1:]}.py'
    #             self.read_python_file(f'{path}/{filename}')
    #             # print(self.read_python_file(f'{path}/{filename}'))
    #             # new_lines = insert_into_list(new_lines, self.read_python_file(f'{path}/{filename}'), i)
    #             # print(self.new_list)
    #         else:
    #             self.new_list.append(line)
    #     # lines = self.new_list
    #     return new_list

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
        f.write(utils.cell_begin_marker(cell_type))
        for line in source_lines:
            if cell_type == CellType.IGNORE:
                f.write(utils.uncomment_line(line))
            elif cell_type == CellType.MARKDOWN:
                f.write(utils.comment_line(line))
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


def insert_into_list(source_list: List[str], target_list: List[str], pos: int):
    for i in range(len(target_list)):
        source_list.insert(i + pos, target_list[i])
    return source_list
