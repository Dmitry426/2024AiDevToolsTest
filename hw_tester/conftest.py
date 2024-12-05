import logging
from pathlib import Path

import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient

from .settings import PROJECT_ROOT
from .services.app_finder import traverse_and_import

logging.basicConfig(level=logging.INFO)

logger = logging.getLogger(__name__)


def pytest_addoption(parser):
    parser.addoption("--repo_url", action="store", help="Git repository URL")
    parser.addoption(
        "--tested_app_dir",
        action="store",
        default="temp_repos",
        help="Tested app directory " "destination",
    )


@pytest.fixture(scope="session")
def test_directory():
    """Fixture to define the test directory based on the loaded Git repository."""
    return Path(PROJECT_ROOT.parent)


@pytest.fixture(scope="session")
def client(test_directory) -> TestClient:
    """Async FastAPI test client fixture."""
    # Dynamically import and initialize the app
    app: FastAPI = traverse_and_import(test_directory)
    yield TestClient(app)
