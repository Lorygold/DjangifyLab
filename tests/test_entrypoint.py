import importlib.metadata
import os
import shutil
import subprocess
import sys
import tempfile

import entrypoint
import pytest


@pytest.fixture(scope="module")
def temp_dir():
    """Create a temporary directory for testing purposes."""
    dirpath = tempfile.mkdtemp()
    yield dirpath
    shutil.rmtree(dirpath)


def test_uninstall_all():
    # Install a dummy package to test uninstall
    subprocess.check_call([sys.executable, "-m", "pip", "install", "pytest"])
    installed_before = subprocess.check_output([sys.executable, "-m", "pip", "freeze"], text=True)
    assert "pytest" in installed_before

    entrypoint.uninstall_all()

    installed_after = subprocess.check_output([sys.executable, "-m", "pip", "freeze"], text=True)
    assert "pytest" not in installed_after


def test_reinstall_requirements(temp_dir):
    # Create a fake requirements.txt
    req_path = os.path.join(temp_dir, "requirements.txt")
    with open(req_path, "w") as f:
        f.write("requests==2.31.0\n")

    cwd = os.getcwd()
    os.chdir(temp_dir)

    try:
        entrypoint.reinstall_requirements()
        output = subprocess.check_output([sys.executable, "-m", "pip", "freeze"], text=True)
        assert "requests==2.31.0" in output
    finally:
        os.chdir(cwd)


def test_install_package():
    # Test installation of a real .tar.gz package
    package_path = os.path.abspath("example-apps/packages/buffalogs-2.7.0.tar.gz")
    subprocess.check_call([sys.executable, "-m", "pip", "install", package_path])

    assert importlib.metadata.version("buffalogs") == "2.7.0"


def test_install_from_folder():
    # Assumes both .tar.gz files are in example-apps/packages
    folder_path = os.path.abspath("example-apps/packages")
    entrypoint.install_from_folder(folder_path)

    version = importlib.metadata.version("buffalogs")
    assert version in ("2.7.0", "2.8.0")
