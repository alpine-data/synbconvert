import json
import os

from behave import given
from behave import then
from behave import when
from behave.runner import Context

from synbconvert import SynapseNotebookConverter

import python_to_notebook as nb


@given("we have a file with the following statements")
def step_impl(context) -> None:  # noqa: F811
    filename = "input.py"
    with open(f"{context.working_directory}/{filename}", "w") as f:
        f.write(context.text)

    # store mentioned file context for later use
    context.files.append(filename)


@then("the {nth} cell should be hidden.")
def step_impl(context, nth) -> None:  # noqa: F811
    expected_hidden_status = True
    index = nb.nth_dict[nth] - 1
    assert_cell_hidden_status(context, index, expected_hidden_status)


@given("we have a notebook containing a Python cell")
def step_impl(context) -> None:  # noqa: F811
    notebook_name = "input.json"
    text = context.text.strip('\"\"\"')
    exec_text = (f"Given we have a Synapse notebook file with the name `{notebook_name}`\n"
                "And the first cell is a Python cell with the following content\n"
                "'''\n"
                f"{text}"
                "'''")
    context.execute_steps(exec_text)


def assert_cell_hidden_status(context: Context, index: int, hidden_status: bool) -> None:
    source_hidden = context.cells[index]["metadata"]["jupyter"]["source_hidden"]
    outputs_hidden = context.cells[index]["metadata"]["jupyter"]["outputs_hidden"]
    assert source_hidden == hidden_status, "The cell source_hidden status is not correct."
    assert outputs_hidden == hidden_status, "The cell outputs_hidden status is not correct."