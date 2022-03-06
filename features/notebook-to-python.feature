Feature: Synapse Notebook to Python file.
  
    Scenario: "Hello World" example.
        Given we have a Synapse Notebook file with name `nb.json`
        And the first cell contains Markdown:
            """
            # Peace!
            Could we please stop this insane war?
            """
        And the second is a Python cell with the following content:
            """
            print('Stop Putin!')
            """
        And the third is a Python cell with the following content:
            """
            print('Stop war!')
            """
        When we transform this file with `nbsynconvert to-python nb.json output.py`.
        Then a file `output.py` should be created.
        And the file should contain:
            """
            \"\"\"markdown
            # Peace!
            Could we please stop this insane war?
            \"\"\"

            print('Stop Putin!')

            # nb--new-cell

            print('Stop war!') 
            """

    Scenario: Empty cells should be ignored.
        Given we have a Synapse Notebook
        And the first cell contains Markdown:
            """
            # Peace!
            Could we please stop this insane war?
            """
        And the second cell is an empty Python cell.
        And the third cell contains Python:
            """

            """
        And the 4th cell contains Python:
            """
            print('Stop war!')
            """
        When we transform this notebook file.
        Then the Python file should contain:
            """
            \"\"\"markdown
            # Peace!
            Could we please stop this insane war?
            \"\"\"

            print('Stop Putin!')
            """