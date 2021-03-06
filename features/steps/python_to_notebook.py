import json
import os

from behave import given
from behave import then
from behave import when
from behave.runner import Context

from synbconvert import SynapseNotebookConverter

nth_dict = {"first": 1, "second": 2, "third": 3, "4th": 4}


@given("we have a Python file `{filename}` with the following statements")
@given("we have a simple Python file `{filename}` with the following statements")
def step_impl(context, filename) -> None:  # noqa: F811

    directory = os.path.dirname(f"{context.working_directory}/{filename}")
    if not os.path.exists(directory):
        os.makedirs(directory)
    with open(f"{context.working_directory}/{filename}", "w") as f:
        f.write(context.text)

    # store mentioned file context for later use
    context.files.append(filename)


@when("we transform this file with `synbconvert convert {source_file} {target_file}`.")
@when(
    "we transform the notebook with `synbconvert convert {source_file} {target_file}`."
)
def step_impl(context, source_file, target_file) -> None:  # noqa: F811
    source_file = f"{context.working_directory}/{source_file}"
    target_file = f"{context.working_directory}/{target_file}"

    synapse_notebook_converter = SynapseNotebookConverter()
    synapse_notebook_converter.convert(source_file, target_file)


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


@then("a file `{filename}` should be created, containing a Synapse notebook.")
@then("a file `{filename}` should be overwritten, containing the Synapse notebook.")
def step_impl(context, filename) -> None:  # noqa: F811
    # check existence
    filename = f"{context.working_directory}/{filename}"
    assert os.path.exists(filename), f"The notebook file {filename} does not exist."

    # check if it is a notebook - or, at least a json file with a name attribute ...
    with open(filename, "r") as f:
        notebook = json.load(f)
    assert (
        notebook["name"] is not None
    ), f"The file {filename} is not a valid Synapse notebook."

    # store notebook in context for later use
    context.notebooks.append(notebook)

    context.cells = [cell for cell in context.notebooks[-1]["properties"]["cells"]]


@then("the created notebook should contain one cell.")
def step_impl(context: Context) -> None:  # noqa: F811
    context.execute_steps("Then the notebook should contain 1 cells.")


@then("the notebook should contain {count} cells.")
def step_impl(context, count) -> None:  # noqa: F811
    exspected_count = int(count)
    actual_count = len(context.notebooks[-1]["properties"]["cells"])
    assert (
        actual_count == exspected_count
    ), f"The notebook contains {actual_count} cells. Expected would be {exspected_count}."

    context.cells = [cell for cell in context.notebooks[-1]["properties"]["cells"]]


@then("the {nth} cell should contain")
def step_impl(context: Context, nth: str) -> None:  # noqa: F811
    index = nth_dict[nth] - 1
    assert_cell_content(context, index, context.text)


@then("the cell should contain the content from the input file.")
def step_impl(context) -> None:  # noqa: F811
    filename = f"{context.working_directory}/{context.files[-1]}"

    with open(filename, "r") as f:
        file_content = f.read().strip()

    assert_cell_content(context, -1, file_content)


@then("the {nth} cell should be a {type} cell with the following content")
def step_impl(context, nth: str, type: str):  # noqa: F811
    index = nth_dict[nth] - 1
    expected_type = get_cell_type_from_string(type)
    assert_cell_type(context, index, expected_type)
    assert_cell_content(context, index, context.text)


def get_cell_type_from_string(type_sting: str) -> str:
    if type_sting == "Python":
        cell_type = "code"
    elif type_sting == "Markdown":
        cell_type = "markdown"
    return cell_type


def assert_cell_type(context: Context, index: int, type: str) -> None:
    cell_type = context.cells[index]["cell_type"]
    assert cell_type == type, "The cell type is not correct."


def assert_cell_content(context: Context, index: int, content: str) -> None:
    cell_content = "".join(context.cells[index]["source"])
    assert cell_content == content, "The cell content is not correct."
