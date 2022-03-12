Feature: Python Includes
    All relative star imports are directly included in the notebook. This allows splitting of large notebooks into multiple files.
    Imported files may also contain markup for notebook generation.

    Scenario: Multiple Python Files
        Given we have a Python file `lib_a.py` with the following statements:
            """
            # This is library a

            # nb--cell
            def print_statement():
                print("These are not sanctions. These are 'special financial operations' to support russian economy.")
            
            """
        And we have a Python file `lib_b.py` with the following statements:
            """
            from .lib_a import *

            # This is library b

            # nb--cell
            print_statement()

            """
        And we have a Python file `input.py` with the following statements:
            """
            import io
            from .lib_b import *

            from .lib_a import print_statement() # This is not replaced/ supported

            # nb--cell
            # This is the root file
            
            """
        When we transform this file with `synbconvert convert input.py nb.json`.
        Then a file `nb.json` should be created, containing a Synapse notebook.
        And the first cell should be a Python cell with the following content:
            """
            import io
            # nb--import-begin "./lib_b.py"
            # nb--import-begin "./lib_a.py"
            # This is library a
            """
        And the second cell should be a Python cell with the following content:
            """
            def print_statement():
                print("These are not sanctions. These are 'special financial operations' to support russian economy.")
            # nb--import-end "./lib_a.py"

            # This is library b
            """
        And the third cell should be a Python cell with the following content:
            """
            print_statement()
            # nb--import-end "./lib_b.py"

            from .lib_a import print_statement() # This is not replaced/ supported
            """
        And the 4th cell should be a Python cell with the following content:
            """
            # This is the root file
            """
        
        When we create a new directory `copy`.
        And we transform the notebook with `synbconvert convert nb.json copy/input.py`.

        Then we expect `copy/input.py` to equal `input.py`.
        And we expect `copy/lib_a.py` to equal `lib_a.py`.
        And we expect `copy/lib_b.py` to equal `lib_b.py`.

    Scenario: Imports from subfolders
        Given we have a Python file `subfolder/lib_a.py` with the following statements:
            """
            # This is library a

            # nb--cell
            def print_statement():
                print("These are not sanctions. These are 'special financial operations' to support russian economy.")
            
            """
        And we have a Python file `lib_b.py` with the following statements:
            """
            from .subfolder.lib_a import *

            # This is library b

            # nb--cell
            print_statement()

            """
        And we have a Python file `input.py` with the following statements:
            """
            import io
            from .lib_b import *

            from .lib_a import print_statement() # This is not replaced/ supported

            # nb--cell
            # This is the root file
            
            """
        When we transform this file with `synbconvert convert input.py nb.json`.
        Then a file `nb.json` should be created, containing a Synapse notebook.
        And the first cell should be a Python cell with the following content:
            """
            import io
            # nb--import-begin "./lib_b.py"
            # nb--import-begin "./subfolder/lib_a.py"
            # This is library a
            """
        And the second cell should be a Python cell with the following content:
            """
            def print_statement():
                print("These are not sanctions. These are 'special financial operations' to support russian economy.")
            # nb--import-end "./subfolder/lib_a.py"

            # This is library b
            """
        And the third cell should be a Python cell with the following content:
            """
            print_statement()
            # nb--import-end "./lib_b.py"

            from .lib_a import print_statement() # This is not replaced/ supported
            """
        And the 4th cell should be a Python cell with the following content:
            """
            # This is the root file
            """
        
        When we create a new directory `copy`.
        And we transform the notebook with `synbconvert convert nb.json copy/input.py`.

        Then we expect `copy/input.py` to equal `input.py`.
        And we expect `copy/subfolder/lib_a.py` to equal `subfolder/lib_a.py`.
        And we expect `copy/lib_b.py` to equal `lib_b.py`.