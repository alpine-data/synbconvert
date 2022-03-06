Feature: Python Includes
    All relative star imports are directly included in the notebook. This allows splitting of large notebooks into multiple files.
    Imported files may also contain markup for notebook generation.

    Scenario: Multiple Python Files
        Given we have a Python file `lib_a.py` with the following statements:
            """
            # This is library a

            # nb--new-cell

            def print_statement():
                print("These are not sanctions. These are 'special financial operations' to support russian economy.")
            """
        And we have a Python file `lib_b.py` with the following statements:
            """
            from .lib_a import *

            # This is library b

            # nb--new-cell

            print_statement()
            """
        And we have a Python file `input.py` with the following statements:
            """
            import io
            from .lib_b import *

            from .lib_a import print_statement() # This is not replaced/ supported

            # nb--new-cell

            # This is the root file
            """
        When we transform this file with `nbsynconvert to-notebook input.py nb.json`.
        Then a file `nb.json` should be created, containing a Synapse Notebook.
        And the first cell should be a Python cell with the following content:
            """
            import io
            """
        And the second cell should be a Python cell with the following content:
            """
            # nb--begin-file './lib_b.py'

            # nb--begin-file './lib_a.py'

            # This is library a
            """
        And the third cell should be a Python cell with the following content:
            """
            def print_statement():
                print("These are not sanctions. These are 'special financial operations' to support russian economy.")
            
            # nb--end-file './lib_a.py'
            """
        And the 4th cell should be a Python cell with the following content:
            """
            # This is library b
            """
        And the 5th cell should be a Python cell with the following content:
            """
            print_statement()

            # nb--end-file './lib_b.py'
            """
        And the 6th cell should be a Python cell with the following content:
            """
            from .lib_a import print_statement() # This is not replaced/ supported
            """
        And the 7th cell should be a Python cell with the following content:
            """
            # This is the root file
            """
        
        When we create a new directory `copy`.
        And we transform the notebook with `nbsynconvert to-python nb.json copy/input.py`.

        Then we expect `copy/input.py` to equal `input.py`.
        And we expect `copy/lib_a.py` to equal `lib_a.py`.
        And we expect `copy/lib_b.py` to equal `lib_b.py`.