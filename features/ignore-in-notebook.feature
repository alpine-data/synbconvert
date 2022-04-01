Feature: Ignore lines from Python file in Notebook
    In some cases the Python file requires additional command which are not required in the notebook. The notebook should contain these lines, but not active (commented).

    Scenario: Ignore lines from Python file
        Given we have a file with the following statements:
            '''
            # nb--ignore-begin
            import sys
            # nb--ignore-end

            n = sys.maxsize # number of repetitions
            my_string = "Stop War!"
            print(my_string*n)
            '''

        When we transform this file.
        Then the notebook should contain 2 cells.
        And the first cell should contain:
            '''
            """nb--ignore
            import sys
            """
            '''
        And the first cell should be hidden.
        And the second cell should contain:
            '''
            n = sys.maxsize # number of repetitions
            my_string = "Stop War!"
            print(my_string*n)
            '''

    Scenario: Multiple ignored cells
        Given we have a file with the following statements:
            '''
            n = sys.maxsize # number of repetitions
            my_string = "Stop War!"
            print(my_string*n)

            # nb--ignore-begin
            import foo
            # nb--ignore-end

            # nb--ignore-begin
            import bar
            # nb--ignore-end

            print("do not ignore war!")
            '''

        When we transform this file.
        Then the notebook should contain 4 cells.
        And the first cell should contain:
            '''
            n = sys.maxsize # number of repetitions
            my_string = "Stop War!"
            print(my_string*n)
            '''
        And the second cell should contain:
            '''
            """nb--ignore
            import foo
            """
            '''
        And the second cell should be hidden.
        And the third cell should contain:
            '''
            """nb--ignore
            import bar
            """
            '''
        And the third cell should be hidden.
        And the 4th cell should contain:
            '''
            print("do not ignore war!")
            '''

    Scenario: Ignored lines from Notebook should be included in Python file.
        Given we have a notebook containing a Python cell:
            '''
            """nb--ignore
            import sys
            """
            '''
        When we transform this notebook.
        Then the Python file should contain:
            '''
            # nb--ignore-begin
            import sys
            # nb--ignore-end
            
            '''
