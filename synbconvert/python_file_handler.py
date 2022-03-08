import os
import re

from typing import Dict, List

from synbconvert import utils
from synbconvert.utils import CellType


class PythonFileHandler(object):
    def __init__(self) -> None:
        super(PythonFileHandler, self).__init__()

    def read_python_file(self, file: str) -> List[str]:
        path = os.path.dirname(file)
        new_lines = []
        with open(file) as f:
            lines = f.readlines()
        for line in lines:
            if is_import(line):
                filename = f'{line.split(" ")[1][1:]}.py'
                full_path = f'{path}/{filename}'
                new_lines.append(utils.begin_import_marker(full_path))
                new_lines.extend(self.read_python_file(full_path))
                new_lines.append(utils.end_import_marker(full_path))
            else:
                new_lines.append(line)
        return new_lines

    def write_python_file(self, file: str, cells: List[Dict]) -> None:
        cells = utils.clean_cells(cells)
        lines = self.cells_to_python_stings(cells)
        self.write_lines(file, lines)

    def cells_to_python_stings(self, cells: List[Dict]):
        python_stings = []
        for cell in cells:
            python_stings.extend(self.cell_content_to_list(cell))
        return python_stings

    def cell_content_to_list(self, cell: Dict) -> List[str]:
        ignore_cell = is_ignore_cell(cell)
        cell_type = get_cell_type(cell)
        source_lines = cell['source']
        cell_content_list = []
        if not ignore_cell:
            cell_content_list.append('\n')
            cell_content_list.append(utils.cell_begin_marker(cell_type))
            if cell_type == CellType.MARKDOWN:
                source_lines = utils.comment_lines(source_lines)
            for line in source_lines:
                cell_content_list.append(line)
            if not line.endswith('\n'):
                cell_content_list[-1] = cell_content_list[-1] + '\n'
        else:
            cell_content_list.append('\n')
            cell_content_list.append(utils.begin_ignore_marker())
            source_lines = utils.uncomment_lines(source_lines)
            source_lines.pop(0)
            for line in source_lines:
                cell_content_list.append(line)
            if not line.endswith('\n'):
                cell_content_list[-1] = cell_content_list[-1] + '\n'
            line = utils.end_ignore_marker()
            cell_content_list.append(line)
        return cell_content_list
    
    def write_lines(self, file: str, lines: List[str]):
        if lines[0] == '\n': lines.remove(lines[0])
        it = iter(lines)
        f = open(file, 'w')
        for line in it:
            if is_begin_import_line(line):
                import_lines = []
                import_definition = get_import_definition_from_path(line)
                path = os.path.dirname(file)
                file_name = get_import_file_name(line)
                if path == '' or path == '.':
                    full_path = f'./{file_name}'
                else:
                    full_path = f'./{path}/{file_name}'
                for import_line in it:
                    if is_end_import_line(import_line) and import_definition == get_import_definition_from_path(import_line):
                        break
                    import_lines.append(import_line)
                f.write(import_definition + '\n')
                self.write_lines(full_path, import_lines)
            else:
                f.write(line)
        f.close()


def get_cell_type(cell: dict) -> CellType:
    if cell['cell_type'] == CellType.MARKDOWN.value:
        cell_type = CellType.MARKDOWN
    elif cell['cell_type'] == CellType.CODE.value:
        cell_type = CellType.CODE
    return cell_type


def get_import_file_name(line: str) -> str:
    begin_import_string = utils.begin_import_marker('')[:-1]
    end_import_string = utils.end_import_marker('')[:-1]
    return os.path.basename(line.replace(begin_import_string, '').replace(end_import_string, '').replace('\n', ''))


def get_import_definition_from_path(path: str) -> str:
    filename = path.split('/')[-1].replace('.py', '').replace('\n', '')
    import_definition = f'from .{filename} import *'
    return import_definition


def is_import(line: str) -> bool:
    return bool(re.search('^from \.(\S)+ import \*$', line))


def is_ignore_cell(cell: dict) -> bool:
    if utils.uncomment_lines(cell['source'])[0] == utils.ignore_marker():
        return True
    else:
        return False


def is_begin_import_line(line: str) -> bool:
    if line.startswith(utils.begin_import_marker('')[:-1]):
        return True
    else:
        return False


def is_end_import_line(line: str) -> bool:
    if line.startswith(utils.end_import_marker('')[:-1]):
        return True
    else:
        return False
