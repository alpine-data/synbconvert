from typing import List
from enum import Enum


class CellType(Enum):

    CODE = 1
    MARKDOWN = 2
    IGNORE = 3


# TODO: Replace cell_type with Enum Type
def cell_begin_marker(cell_type: str):
    print(type(CellType.CODE))
    print("sdfsdf")
    if cell_type == CellType.CODE:
        return '# @cell-begin-code\n'
    if cell_type == CellType.MARKDOWN:
        return '# @cell-begin-markdown\n'
    if cell_type == CellType.IGNORE:
        return '# @cell-begin-ignore\n'


def comment_line(line: str) -> str:
    line = f"# {line}"
    return line


def uncomment_line(line: str) -> str:
    comment_prefix = "# "
    if line.startswith(comment_prefix):
        return line[len(comment_prefix) :]
    else:
        return line


def comment_lines(lines: List[str]) -> List[str]:
    return [comment_line(line) for line in lines]


def uncomment_lines(lines: List[str]) -> List[str]:
    return [uncomment_line(line) for line in lines]
