from typing import List


class CellTypes:
    def __init__(self, markdown: str = "markdown", code: str = "code"):
        self.MARKDOWN = markdown
        self.CODE = code


# TODO: Replace cell_type with Enum Type
def cell_begin_marker(cell_type: str) -> str:
    if cell_type == "code":
        return "# @cell-begin-code\n"
    elif cell_type == "markdown":
        return "# @cell-begin-markdown\n"
    else:
        raise Exception("unknown cell type")


# TODO: Replace cell_type with Enum Type
def cell_end_marker(cell_type: str) -> str:
    if cell_type == "code":
        return "# @cell-end-code\n"
    elif cell_type == "markdown":
        return "# @cell-end-markdown\n"
    else:
        raise Exception("unknown cell type")


def cell_begin_ignore_marker() -> str:
    return "# @cell-begin-ignore\n"


def cell_end_ignore_marker() -> str:
    return "# @cell-end-ignore\n"


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
