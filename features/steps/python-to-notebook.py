import json
import os

from behave import given
from behave import then
from behave import when
from behave.runner import Context

from synbconvert import SynapseNotebookConverter


@given("we have a Python file `{filename}` with the following statements")
@given("we have a simply Python file `{filename}` with the following statements")
def step_impl(context, filename) -> None:  # noqa: F811
    with open(f"{context.working_directory}/{filename}", "w") as f:
        f.write(context.text)

    # store mentioned file context for later use
    context.files.append(filename)


@when(
    "we transform this file with `nbsynconvert to-notebook {source_file} {target_file}`."
)
def step_impl(context, source_file, target_file) -> None:  # noqa: F811
    source_file = f"{context.working_directory}/{source_file}"
    target_file = f"{context.working_directory}/{target_file}"

    converter = SynapseNotebookConverter()
    converter.convert_python_file_to_synapse_notebook(source_file, target_file)


@when("we transform this file.")
def step_impl(context: Context) -> None:  # noqa: F811
    notebook_file = "nb.json"

    context.execute_steps(
        f"""
        When we transform this file with `nbsynconvert to-notebook {context.files[-1]} {notebook_file}`.
        Then a file `{notebook_file}` should be created, containing a Synapse Notebook.
    """
    )


@then("a file `{filename}` should be created, containing a Synapse Notebook.")
def step_impl(context, filename) -> None:  # noqa: F811
    # check existence
    filename = f"{context.working_directory}/{filename}"
    assert os.path.exists(filename)

    # check if it is a notebook - or, at least a json file with a name attribute ...
    with open(filename, "r") as f:
        notebook = json.load(f)
    assert notebook["name"] is not None

    # store notebook in context for later use
    context.notebooks.append(notebook)


@then("the created notebook should contain one cell.")
def step_impl(context: Context) -> None:  # noqa: F811
    context.execute_steps("Then the notebook should contain 1 cells.")


@then("the notebook should contain only `{count}` cells.")
@then("the notebook should contain `{count}` cells.")
def step_impl(context, count) -> None:  # noqa: F811
    assert len(context.notebooks[-1]["properties"]["cells"]) == int(count)

    context.cells = [
        "".join(cell.source) for cell in context.notebooks[-1]["properties"]["cells"]
    ]


@then("the first cell should contain")
def step_impl(context: Context) -> None:  # noqa: F811
    assert_cell_content(context, 0, context.text)


@then("the second cell should contain")
def step_impl(context) -> None:  # noqa: F811
    assert_cell_content(context, 1, context.text)


@then("the cell should contain the content from the input file.")
def step_impl(context) -> None:  # noqa: F811
    filename = f"{context.working_directory}/{context.files[-1]}"

    with open(filename, "r") as f:
        file_content = f.read().strip()

    assert_cell_content(context, 0, file_content)


def assert_cell_content(context: Context, index: int, content: str) -> None:
    cell_content = context.cells[int(index) - 1]
    assert cell_content == content
