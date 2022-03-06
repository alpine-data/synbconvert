Feature: Python to Synapse Notebooks.
    Scenario: "Hello World" example.
        Given we have a simply Python file `input.py` with the following statements:
            """
            import sys
            n = sys.maxsize # number of repetitions
            my_string = "Stop War!"
            print(my_string*n)
            """
        When we transform this file with `nbsynconvert to-notebook input.py nb.json`.
        Then a file `nb.json` should be created, containing a Synapse Notebook.
        And the created notebook should contain one cell.
        And the cell should contain the content from the input file.

    Scenario: Splitting code into cells.
        Given we have a Python file `input.py` with the following statements:
            """
            import sys

            # nb--new-cell

            n = sys.maxsize # number of repetitions
            my_string = "Stop War!"
            print(my_string*n)
            """
        When we transform this file.
        Then the notebook should contain `2` cells.
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

            # nb--new-cell

            # nb--new-cell

            n = sys.maxsize # number of repetitions
            my_string = "Stop War!"
            print(my_string*n)
            """
        When we transform this file.
        Then the notebook should contain only `2` cells.


    Scenario: Cells may contain Markdown
        Given we have a file with the following statements:
            '''
            import sys

            """markdown
            # We stay united with people in Ukraine and Russia
            Fuck off, Putin!
            """
            
            # nb--new-cell

            n = sys.maxsize # number of repetitions
            my_string = "Stop War!"
            print(my_string*n)
            '''
        When we transform this file.
        Then the notebook should contain `3` cells.
        And the first cell should be a Python cell with the following content:
            '''
            import sys
            '''
        And the second cell should be a Markdown cell with the following content:
            '''
            # We stay united with people in Ukraine and Russia
            Fuck off, Putin!
            '''
        And the thor cell should be a Python cell with the following content:
            '''
            n = sys.maxsize # number of repetitions
            my_string = "Stop War!"
            print(my_string*n)
            '''

    Scenario: Markdown may use also single quoted blocks
        Given we have a file with the following statements:
            """
            import sys

            '''markdown
            # We stay united with people in Ukraine and Russia
            Fuck off, Putin!
            '''

            n = sys.maxsize # number of repetitions
            my_string = "Stop War!"
            print(my_string*n)
            """
        When we transform this file.
        Then the notebook should contain `3` cells.
        And the second cell should be a Markdown cell with the following content:
            """
            # We stay united with people in Ukraine and Russia
            Fuck off, Putin!
            """
 