class CellTypes:
    
    def __init__(self, markdown='markdown', code='code'):
        self.MARKDOWN = markdown
        self.CODE = code


def cell_begin_marker(cell_type: str):
    if cell_type == 'code':
        return '# %%cell-begin-code\n'
    if cell_type == 'markdown':
        return '# %%cell-begin-markdown\n'


def cell_end_marker(cell_type: str):
    if cell_type == 'code':
        return '# %%cell-end-code\n'
    if cell_type == 'markdown':
        return '# %%cell-end-markdown\n'