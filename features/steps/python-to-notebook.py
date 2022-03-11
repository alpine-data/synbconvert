import json
import os

from behave import given
from behave import then
from behave import when
from behave.runner import Context

from synbconvert import SynapseNotebookConverter


@given("we have a Python file `{filename}` with the following statements")
@given("we have a simple Python file `{filename}` with the following statements")
def step_impl(context, filename) -> None:  # noqa: F811
    with open(f"{context.working_directory}/{filename}", "w") as f:
        f.write(context.text)

    # store mentioned file context for later use
    context.files.append(filename)


@when(
    "we transform this file with `synbconvert convert {source_file} {target_file}`."
)
def step_impl(context, source_file, target_file) -> None:  # noqa: F811
    source_file = f"{context.working_directory}/{source_file}"
    target_file = f"{context.working_directory}/{target_file}"

    converter = SynapseNotebookConverter()

    if source_file.endswith(".py") and target_file.endswith(".json"):
        converter.convert_python_file_to_synapse_notebook(
            source_file, target_file
        )

    if source_file.endswith(".json") and target_file.endswith(".py"):
        converter.convert_synapse_notebook_to_python_file(
            source_file, target_file
        )


@when("we transform this Python file.")
@when("we transform this file.")
def step_impl(context: Context) -> None:  # noqa: F811
    notebook_file = "output.json"

    context.execute_steps(
        f"""
        When we transform this file with `synbconvert convert {context.files[-1]} {notebook_file}`.
        Then a file `{notebook_file}` should be created, containing a Synapse Notebook.
        """
    )


@then("a file `{filename}` should be created, containing a Synapse Notebook.")
def step_impl(context, filename) -> None:  # noqa: F811
    # check existence
    filename = f"{context.working_directory}/{filename}"
    assert os.path.exists(filename), f"The notebook file {filename} does not exist."

    # check if it is a notebook - or, at least a json file with a name attribute ...
    with open(filename, "r") as f:
        notebook = json.load(f)
    assert notebook["name"] is not None, f"The file {filename} is not a valid Synapse notebook."

    # store notebook in context for later use
    context.notebooks.append(notebook)


@then("the created notebook should contain one cell.")
def step_impl(context: Context) -> None:  # noqa: F811
    context.execute_steps("Then the notebook should contain 1 cells.")


@then("the notebook should contain {count} cells.")
def step_impl(context, count) -> None:  # noqa: F811
    exspected_count = int(count)
    actual_count = len(context.notebooks[-1]["properties"]["cells"])
    assert actual_count == exspected_count, f"The notebook contains {actual_count} cells. Expected would be {exspected_count}."

    context.cells = [
        cell for cell in context.notebooks[-1]["properties"]["cells"]
    ]


@then("the first cell should contain")
def step_impl(context: Context) -> None:  # noqa: F811dsf
    assert_cell_content(context, -2, context.text)


@then("the second cell should contain")
def step_impl(context) -> None:  # noqa: F811
    assert_cell_content(context, -1, context.text)


@then("the cell should contain the content from the input file.")
def step_impl(context) -> None:  # noqa: F811
    filename = f"{context.working_directory}/{context.files[-1]}"

    with open(filename, "r") as f:
        file_content = f.read().strip()

    assert_cell_content(context, -1, file_content)


@then("the first cell should be a {type} cell with the following content")
def step_impl(context, type: str):
    expected_type = get_cell_type_from_string(type)
    assert_cell_type(context, -3, expected_type)
    assert_cell_content(context, -3, context.text)


@then("the second cell should be a {type} cell with the following content")
def step_impl(context, type: str):
    expected_type = get_cell_type_from_string(type)
    assert_cell_type(context, -2, expected_type)
    assert_cell_content(context, -2, context.text)


@then("the third cell should be a {type} cell with the following content")
def step_impl(context, type: str):
    expected_type = get_cell_type_from_string(type)
    assert_cell_type(context, -1, expected_type)
    assert_cell_content(context, -1, context.text)


def get_cell_type_from_string(type_sting: str) -> str:
    if type_sting == "Python":
        cell_type = "code"
    elif type_sting == "Markdown":
        cell_type = "markdown"
    return cell_type


def assert_cell_type(context: Context, index: int, type: str) -> None:
    cell_type = context.cells[index]["cell_type"]
    # TODO: write assert statement
    assert cell_type == type, "The cell type is not correct."


def assert_cell_content(context: Context, index: int, content: str) -> None:
    cell_content = "".join(context.cells[index]["source"])
    print(cell_content)
    # TODO: write assert statement
    assert cell_content == content, "The cell content is not correct."
