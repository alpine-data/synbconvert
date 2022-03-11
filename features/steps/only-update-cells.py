import json
import os

from behave import given
from behave import then
from behave import when
from behave.runner import Context

from synbconvert import SynapseNotebookConverter


@given("we have an exising Synapse notebook `{filename}` including `{example_path}`.")
def step_impl(context, filename, example_path) -> None:  # noqa: F811
    with open(example_path) as f:
        create_synapse_notebook_template = json.load(f)

    with open(f"{context.working_directory}/{filename}", "w") as f:
        json.dump(create_synapse_notebook_template, f)


@then("the spark.autotune.trackingId of the notebook should be `{expected_id}`.")
def step_impl(context, expected_id) -> None:  # noqa: F811
    id = context.notebooks[-1]["properties"]["sessionProperties"]["conf"]["spark.autotune.trackingId"]
    assert expected_id == id
