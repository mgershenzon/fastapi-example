import os

# noinspection PyPackageRequirements
import pytest

from tests.test_structure.test_requirements import assert_req_compiled
from tests.test_structure.test_style import TEST_ROOT


@pytest.mark.slow
def test_dev_requirements_files():
    assert_req_compiled(os.path.join(TEST_ROOT, "dev_requirements.in"), os.path.join(TEST_ROOT, "dev_requirements.txt"))

