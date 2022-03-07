Feature: Only update cells
    If a Synapse Notebook already exists. Only the cells should be updated, all other configurations stay the same.

    Scenario: "Hello World" example with existing file.
        Given we have a simply Python file `input.py` with the following statements:
            """
            import sys
            n = sys.maxsize # number of repetitions
            my_string = "Stop War!"
            print(my_string*n)
            """
        And we have an exising Synapse Notebook `nb.json` including `examples/sample_notebook.json`. 
        When we transform this file with `nbsynconvert to-notebook input.py nb.json`.
        Then a file `nb.json` should be overwritten, containing the Synapse Notebook.
        And the created notebook should contain one cell.
        And the cell should contain the content from the input file.
        And the spark.autotune.trackingId of the notebook should be `70856775-808584737833`.