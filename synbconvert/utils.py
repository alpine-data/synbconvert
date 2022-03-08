from typing import Dict, List
from enum import Enum


class CellType(Enum):

    CODE = 'code'
    MARKDOWN = 'markdown'


def cell_begin_marker(cell_type: CellType) -> str:
    if cell_type == CellType.CODE:
        return '# @cell-begin-code\n'
    if cell_type == CellType.MARKDOWN:
        return '# @cell-begin-markdown\n'


def ignore_marker() -> str:
    return '@ignore\n'


def begin_ignore_marker() -> str:
    return '# @begin-ignore\n'


def end_ignore_marker() -> str:
    return '# @end-ignore\n'


def begin_import_marker(import_line: str) -> str:
    return f'# @begin-import: {import_line}\n'


def end_import_marker(import_line: str) -> str:
    return f'# @end-import: {import_line}\n'


def comment_lines(lines: List[str]) -> List[str]:
    lines[0] = f"\"\"\"{lines[0]}"
    lines[-1] = f"{lines[-1]}\"\"\""
    return lines


def uncomment_lines(lines: List[str]) -> List[str]:
    lines[0] = lines[0].lstrip('\"')
    lines[-1] = lines[-1].rstrip('\"')
    lines[0] = lines[0].lstrip('\'')
    lines[-1] = lines[-1].rstrip('\'')
    return lines


def clean_cells(cells: List[Dict]) -> List[Dict]:
    for cell in cells:
        if not cell['source']:
            cells.remove(cell)
        if len(cell['source']) == 1 and cell['source'][0] == '':
            cells.remove(cell)
    return cells
