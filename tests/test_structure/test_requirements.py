import asyncio
import os
import subprocess
import tempfile
from typing import Any, Coroutine

# noinspection PyPackageRequirements
import pytest

from tests.test_structure.test_style import REPO_ROOT


async def read_file(file_path: str) -> str:
    with open(file_path, 'r') as file:
        content = await asyncio.to_thread(file.read)
        return content


async def read_file_co(file_path_co: Coroutine[Any, Any, str]) -> str:
    file_path = await file_path_co
    with open(file_path, 'r') as file:
        content = await asyncio.to_thread(file.read)
        return content


async def compile_to_temp(req_in_path) -> str:
    with tempfile.NamedTemporaryFile('w+', delete=False) as temp_req_txt_file:
        temp_req_txt_file.write("")
        temp_req_txt_file.flush()  # Ensure the content is written to disk

        try:
            cmd = ['pip-compile',
                   req_in_path,
                   '-o',
                   temp_req_txt_file.name,
                   '--no-annotate']
            subprocess.run(
                cmd,
                check=True,
                capture_output=True,
                text=True)

            return temp_req_txt_file.name

        except Exception as e:
            print(f"An error occurred while running pip-compile: {e}")
            assert False, f"Error while running test!! To debug, try running: '{' '.join(cmd)}'. Exception: '{e}'"
    # reading_temp_file = async_read_file(temp_req_txt_file.name)
    # return reading_temp_file


def filter_comments(file_content):
    return "\n".join(
        line.split('#')[0].strip() for line in file_content.splitlines() if not line.lstrip().startswith("#")
    )


async def assert_req_compiled(req_in_path, expected_dependencies_file_path):

    reading_real_txt_file = read_file(expected_dependencies_file_path)
    reading_req_in_file = read_file(req_in_path)

    missing = []

    real_txt_file_content = await reading_real_txt_file
    real_txt = filter_comments(real_txt_file_content)
    req_in_file_content = await reading_req_in_file

    for line in req_in_file_content.split("\n"):
        if line not in real_txt:
            if not line.startswith("-r"):
                mod_line = line.replace("_", "-")  # We don't care about the convention, both are the same
                if mod_line not in real_txt_file_content:
                    missing.append(line)

    if missing:
        reading_temp_file = read_file_co(compile_to_temp(req_in_path))
        temp_file_content = await reading_temp_file
        temp_txt = filter_comments(temp_file_content)
        assert (real_txt == temp_txt), f"Only minor changes allowed, but next dependencies are missing{missing}"


@pytest.mark.slow
def test_requirements_files():
    asyncio.run(assert_req_compiled(os.path.join(REPO_ROOT, "requirements.in"), os.path.join(REPO_ROOT, "requirements.txt")))
