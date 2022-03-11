Feature: Synapse Notebook to Python file.
  
    Scenario: "Hello World" example.
        Given we have a Synapse notebook file with the name `input.json`
        And the first cell is a Markdown cell with the following content:
            """
            # Peace!
            Could we please stop this insane war?
            """
        And the second cell is a Python cell with the following content:
            """
            print('Stop Putin!')
            """
        And the third cell is a Python cell with the following content:
            """
            print('Stop war!')
            """
        When we transform this file with `synbconvert convert input.json output.py`.
        Then a file `output.py` should be created.
        And the file should contain:
            '''
            """nb--markdown
            # Peace!
            Could we please stop this insane war?
            """

            # nb--cell
            print('Stop Putin!')

            # nb--cell
            print('Stop war!')

            '''

    Scenario: Empty cells should be ignored.
        Given we have a Synapse notebook file with the name `input.json`
        And the first cell is a Markdown cell with the following content:
            """
            # Peace!
            Could we please stop this insane war?
            """
        And the second cell is a Python cell with the following content:
            """
            print('Stop Putin!')
            """
        And the third cell is a Python cell with the following content:
            """

            """
        And the fourth cell is a Python cell with the following content:
            """
            print('Stop war!')
            """
        When we transform this notebook file.
        Then the file should contain:
            '''
            """nb--markdown
            # Peace!
            Could we please stop this insane war?
            """

            # nb--cell
            print('Stop Putin!')

            # nb--cell
            print('Stop war!')

            '''