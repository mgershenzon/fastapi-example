import os
from pathlib import Path

import pycodestyle

TEST_ROOT = Path(__file__).parent.absolute()
REPO_ROOT = Path(TEST_ROOT).parent.absolute()
CONFIG_PATH = Path(REPO_ROOT, "pycodestyle")


def test_pep8():
    style = pycodestyle.StyleGuide(quiet=False, config_file=CONFIG_PATH)
    for root, dirs, files in os.walk(os.path.join(REPO_ROOT, "fastapi_example")):
        python_files = [os.path.join(root, f) for f in files if f.endswith(".py")]
        style.check_files(python_files)
    for root, dirs, files in os.walk(TEST_ROOT):
        python_files = [os.path.join(root, f) for f in files if f.endswith(".py")]
        style.check_files(python_files)
    n = style.check_files().total_errors
    assert n == 0
