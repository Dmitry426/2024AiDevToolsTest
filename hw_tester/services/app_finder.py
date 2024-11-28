__all__ = "traverse_and_import"

import importlib.util
import logging
import os
import sys
from pathlib import Path
from types import ModuleType

from fastapi import FastAPI

logger = logging.getLogger("fastapi_autotest")


def import_main_module(module_path: str) -> ModuleType:
    """
    Import the main module from the given file path, retrying if ModuleNotFoundError occurs
    by adding parent directories to sys.path.

    :param module_path: The file path to the module (e.g., "main.py").
    :return: The imported module.
    :raises: ImportError if the module cannot be loaded.
    """
    module_path = Path(module_path).resolve()
    current_directory = module_path.parent

    for _ in range(4):
            if str(current_directory) not in sys.path:
                sys.path.insert(0, str(current_directory))
                logger.info(f"Added {current_directory} to sys.path")

            try:
                spec = importlib.util.spec_from_file_location("main", str(module_path))
                if spec and spec.loader:
                    main_module = importlib.util.module_from_spec(spec)
                    spec.loader.exec_module(main_module)
                    return main_module
                else:
                    raise ImportError(f"Could not load module from path: {module_path}")
            except ModuleNotFoundError as e:
                logger.warning(f"ModuleNotFoundError: {e}. Retrying with parent directory...")
                current_directory = current_directory.parent

# pylint: disable=no-else-return,inconsistent-return-statements
def traverse_and_import(directory_path: Path) -> FastAPI:
    """Traverse through given dir and fin Fastapi app
    :param directory_path: Fast api repo path
    :return : Fast api app
    """

    for root, dirs, files in os.walk(directory_path):
        if "venv" in dirs:
            dirs.remove("venv")

        if ".venv" in dirs:
            dirs.remove(".venv")

        if "tests" in dirs:
            dirs.remove("tests")

        for file in files:
            if file == "main.py":
                module_path = os.path.join(root, file)
                logger.error(module_path)
                main_module = import_main_module(module_path)
                if hasattr(main_module, "app"):
                    return main_module.app
                else:
                    logger.error(f"No 'app' object found in {module_path}")
                    raise FileExistsError(f"No 'app' object found in {module_path}")

