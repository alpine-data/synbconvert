from typing import List


class CellTypes:
    
    def __init__(self, markdown='markdown', code='code'):
        self.MARKDOWN = markdown
        self.CODE = code


def cell_begin_marker(cell_type: str):
    if cell_type == 'code':
        return '# @cell-begin-code\n'
    if cell_type == 'markdown':
        return '# @cell-begin-markdown\n'


def cell_end_marker(cell_type: str):
    if cell_type == 'code':
        return '# @cell-end-code\n'
    if cell_type == 'markdown':
        return '# @cell-end-markdown\n'


def cell_begin_ignore_marker():
    return '# @cell-begin-ignore\n'


def cell_end_ignore_marker():
    return '# @cell-end-ignore\n'


def comment_line(line: str):
    line = f'# {line}'
    return line


def uncomment_line(line: str):
    comment_prefix = '# '
    if line.startswith(comment_prefix):
        return line[len(comment_prefix):]
    else:
        return line


def comment_lines(lines: List[str]):
    return [comment_line(line) for line in lines]


def uncomment_lines(lines: List[str]):
    return [uncomment_line(line) for line in lines]
