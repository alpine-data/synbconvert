Feature: Python to Synapse Notebooks.
    Scenario: "Hello World" example.
        Given we have a simple Python file `input.py` with the following statements:
            """
            import sys
            n = sys.maxsize # number of repetitions
            my_string = "Stop War!"
            print(my_string*n)
            """
        When we transform this file with `synbconvert convert input.py output.json`.
        Then a file `output.json` should be created, containing a Synapse notebook.
        And the created notebook should contain one cell.
        And the cell should contain the content from the input file.

    Scenario: Splitting code into cells.
        Given we have a Python file `input.py` with the following statements:
            """
            import sys

            # nb--cell
            n = sys.maxsize # number of repetitions
            my_string = "Stop War!"
            print(my_string*n)
            """
        When we transform this file.
        Then the notebook should contain 2 cells.
        And the first cell should contain:
            """
            import sys
            """
        And the second cell should contain:
            """
            n = sys.maxsize # number of repetitions
            my_string = "Stop War!"
            print(my_string*n)
            """

    Scenario: Empty cells should be avoided.
        Given we have a Python file `input.py` with the following statements:
            """
            import sys

            # nb--cell

            # nb--cell
            n = sys.maxsize # number of repetitions
            my_string = "Stop War!"
            print(my_string*n)
            """
        When we transform this file.
        Then the notebook should contain 2 cells.


    Scenario: Cells may contain Markdown
        Given we have a Python file `input.py` with the following statements:
            '''
            import sys

            """nb--markdown
            # We stay united with people in Ukraine and Russia
            Fuck off, Putin!
            """
            
            # nb--cell
            n = sys.maxsize # number of repetitions
            my_string = "Stop War!"
            print(my_string*n)
            '''
        When we transform this file.
        Then the notebook should contain 3 cells.
        And the first cell should be a Python cell with the following content:
            '''
            import sys
            '''
        And the second cell should be a Markdown cell with the following content:
            '''
            # We stay united with people in Ukraine and Russia
            Fuck off, Putin!
            '''
        And the third cell should be a Python cell with the following content:
            '''
            n = sys.maxsize # number of repetitions
            my_string = "Stop War!"
            print(my_string*n)
            '''

    Scenario: Markdown may use also single quoted blocks
        Given we have a Python file `input.py` with the following statements:
            """
            import sys

            '''nb--markdown
            # We stay united with people in Ukraine and Russia
            Fuck off, Putin!
            '''

            # nb--cell
            n = sys.maxsize # number of repetitions
            my_string = "Stop War!"
            print(my_string*n)
            """
        When we transform this file.
        Then the notebook should contain 3 cells.
        And the second cell should be a Markdown cell with the following content:
            """
            # We stay united with people in Ukraine and Russia
            Fuck off, Putin!
            """
 