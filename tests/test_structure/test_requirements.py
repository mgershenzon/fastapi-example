import os
import subprocess
import tempfile

import pytest

from tests.test_structure.test_style import REPO_ROOT


def filter_comments(file_content):
    return "\n".join(
        line for line in file_content.splitlines() if not line.lstrip().startswith("#")
    )


def assert_req_compiled(req_in_path, expected_dependencies_file_path):
    with tempfile.NamedTemporaryFile('w+', delete=False) as temp_req_txt_file:
        temp_req_txt_file.write("")
        temp_req_txt_file.flush()  # Ensure the content is written to disk

        try:
            subprocess.run(
                ['pip-compile', req_in_path, '-o', temp_req_txt_file.name],
                check=True,
                capture_output=True,
                text=True)

        except subprocess.CalledProcessError as e:
            print(f"An error occurred while running pip-compile: {e}")
            assert False, f"Error while running test!! {e}"

        with open(temp_req_txt_file.name, 'r') as read_file:
            temp_file_content = read_file.read()

        with open(expected_dependencies_file_path, 'r') as real_req_txt_file:
            real_file_content = real_req_txt_file.read()

        assert filter_comments(real_file_content) == filter_comments(temp_file_content)


@pytest.mark.slow
def test_requirements_files():
    assert_req_compiled(os.path.join(REPO_ROOT, "requirements.in"), os.path.join(REPO_ROOT, "requirements.txt"))

