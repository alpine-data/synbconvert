from behave import *
from behave.log_capture import capture

import tempfile
import shutil

@capture()
def before_scenario(context, scenario):
    context.working_directory = tempfile.mkdtemp()

    # prepare some lists to store mentioned entities during steps
    context.cells = []
    context.files = []
    context.file_contents = []
    context.notebooks = []

@capture()
def after_scenario(context, scenario):
    shutil.rmtree(context.working_directory)