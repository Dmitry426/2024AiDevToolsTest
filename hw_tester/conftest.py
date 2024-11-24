import logging
from functools import lru_cache
from pathlib import Path
from typing import Dict

import pytest
import yaml
from fastapi.testclient import TestClient

from hse_fastapi_autotest.services.finders.app_finder import traverse_and_import

logging.basicConfig(level=logging.INFO)

logger = logging.getLogger("fastapi_autotest")


def pytest_addoption(parser):
    parser.addoption("--repo_url", action="store", help="Git repository URL")
    parser.addoption(
        "--tested_app_dir",
        action="store",
        default="temp_repos",
        help="Tested app directory " "destination",
    )



@pytest.fixture(scope="session")
def test_directory(git_repo):
    """Fixture to define the test directory based on the loaded Git repository."""
    return Path(git_repo.working_dir)


@pytest.fixture(scope="module")
def client(test_directory) -> TestClient:
    """Fast api test client"""
    app = traverse_and_import(test_directory)
    yield TestClient(app)




