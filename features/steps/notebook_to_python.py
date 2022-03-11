import json
import os
import readline
from behave import given
from behave import then
from behave import when
from behave.runner import Context

from synbconvert import SynapseNotebookConverter
from synbconvert.syn_notebook_handler import create_cell_metadata, create_synapse_notebook_template


@given("we have a Synapse notebook file with the name `{filename}`")
def step_impl(context, filename) -> None:  # noqa: F811
    with open(f"{context.working_directory}/{filename}", "w") as f:
        json.dump(create_synapse_notebook_template(), f)

    # store mentioned file context for later use
    context.files.append(filename)


@given("the {counter} cell is a Python cell with the following content")
def step_impl(context, counter) -> None:  # noqa: F811
    file = f"{context.working_directory}/{context.files[-1]}"
    append_text_as_cell_to_file(context.text, file, 'code')


@given("the {counter} cell is a Markdown cell with the following content")
def step_impl(context, counter) -> None:  # noqa: F811
    file = f"{context.working_directory}/{context.files[-1]}"
    append_text_as_cell_to_file(context.text, file, 'markdown')


@then("a file `{filename}` should be created.")
def step_impl(context, filename) -> None:  # noqa: F811
    # check existence
    filename = f"{context.working_directory}/{filename}"
    assert os.path.exists(filename), f"The file {filename} does not exist."

    # check if it is a notebook - or, at least a json file with a name attribute ...
    with open(filename, "r") as f:
        file_content = f.readlines()

    # store notebook in context for later use
    context.file_contents.append(file_content)


@then("the file should contain")
@then("the Python file should contain")
def step_impl(context) -> None:  # noqa: F811
    file_content = "".join(context.file_contents[-1])
    assert file_content == context.text, "The file content is not correct."


@when("we transform this notebook file.")
@when("we transform this notebook.")
def step_impl(context: Context) -> None:  # noqa: F811
    python_file = "output.py"

    context.execute_steps(
        f"""
        When we transform this file with `synbconvert convert {context.files[-1]} {python_file}`.
        Then a file `{python_file}` should be created.
        """
    )


def append_text_as_cell_to_file(text: str, file: str, cell_type: str, hidden: bool = False):
    cell: dict = {"cell_type": cell_type, "source": [e + '\n' for e in text.split('\n') if e]}
    cell["metadata"] = create_cell_metadata(True)

    with open(file) as f:
        data = json.load(f)
        data["properties"]["cells"].append(cell)

    with open(file, "w") as f:
        json.dump(data, f)
