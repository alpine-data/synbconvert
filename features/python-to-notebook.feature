Feature: Transform a python files to a notebook.

  Scenario: "Hello World" example.
     Given we have a simply python file `input.py` with the following statements:
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
    Given we have a python file `input.py` with the following statements:
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
    Given we have a python file `input.py` with the following statements:
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

  Scenario: Empty cells should be avoided.
    Given we have a python file `input.py` with the following statements:
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

  Scenario: Empty cells should not be avoided 
    Given we have a python file `input.py` with the following statements:
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

 