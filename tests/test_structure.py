import os
import warnings
from pathlib import Path

import isort
import pytest_ruff

TEST_ROOT = Path(__file__).parent.absolute()
REPO_ROOT = Path(TEST_ROOT).parent.absolute()
CONFIG_PATH = Path(REPO_ROOT, "ruff.toml")

isort_config = isort.Config(line_length=120, known_first_party=["fastapi_example"])


def check_directory_style(path, errors):
    for root, dirs, files in os.walk(os.path.join(path)):
        for f in files:
            if f.endswith(".py"):
                path = os.path.join(root, f)
                try:
                    pytest_ruff.check_file(path)
                except pytest_ruff.RuffError as re:
                    errors.append(re)


def test_pep8():
    errors = []

    check_directory_style(os.path.join(REPO_ROOT, "fastapi_example"), errors)
    check_directory_style(TEST_ROOT, errors)

    msg = "Problem found. For more info run the next command: 'ruff check .'"
    assert str(errors) == "[]", msg


def check_directory_imports(path, diffs):
    for root, dirs, files in os.walk(os.path.join(path)):
        for f in files:
            if f.endswith(".py"):
                path = os.path.join(root, f)
                good = isort.check_file(path, show_diff=True, config=isort_config)
                if not good:
                    diffs.append(path)


def test_import_order():
    import_diffs = []

    check_directory_imports(os.path.join(REPO_ROOT, "fastapi_example"), import_diffs)
    check_directory_imports(TEST_ROOT, import_diffs)

    msg = (
        f"Import order issues found in: {import_diffs}. "
        f"For more info, run the following command: 'isort . --line-length 120 -q --diff'"
    )

    if import_diffs:
        warnings.warn(msg)
