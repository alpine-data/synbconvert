import json
import os

from behave import given
from behave import then
from behave import when
from behave.runner import Context

from synbconvert import SynapseNotebookConverter


@when("we create a new directory `{dir_name}`.")
def step_impl(context, dir_name) -> None:  # noqa: F811
    dir_path = f"{context.working_directory}/{dir_name}"
    os.mkdir(dir_path)


@then("we expect `{output}` to equal `{input}`.")
def step_impl(context, output, input) -> None:  # noqa: F811
    input_path = f"{context.working_directory}/{input}"
    output_path = f"{context.working_directory}/{output}"
    
    with open(input_path) as f:
        input_lines = f.readlines()

    with open(output_path) as f:
        output_lines = f.readlines()

    print(input_lines)
    print(output_lines)
    
    assert input_lines == output_lines, "The files do not match."
