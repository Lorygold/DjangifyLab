import sys
from unittest import mock

import install_app
import pytest


@pytest.fixture
def mock_check_call():
    with mock.patch("subprocess.check_call") as m:
        yield m


@pytest.fixture
def mock_check_output():
    with mock.patch("subprocess.check_output") as m:
        m.return_value = "package1==1.0\npackage2==2.0"
        yield m


@mock.patch("install_app.subprocess.check_output")
@mock.patch("install_app.subprocess.check_call")
def test_uninstall_all(mock_check_call, mock_check_output):
    mock_check_output.return_value = "package1==1.0\npackage2==2.0"

    install_app.uninstall_all()

    mock_check_call.assert_called_with([sys.executable, "-m", "pip", "uninstall", "-y", "package1==1.0", "package2==2.0"])


def test_reinstall_requirements_exists(mock_check_call, tmp_path):
    # Create dummy requirements.txt in temp dir
    req_file = tmp_path / "requirements.txt"
    req_file.write_text("flake8")

    with mock.patch("os.getcwd", return_value=str(tmp_path)):
        install_app.reinstall_requirements()

    mock_check_call.assert_called_with([sys.executable, "-m", "pip", "install", "-r", str(req_file)])


def test_reinstall_requirements_missing(tmp_path):
    with mock.patch("os.getcwd", return_value=str(tmp_path)):
        with pytest.raises(SystemExit):
            install_app.reinstall_requirements()


def test_install_package(mock_check_call):
    install_app.install_package("dummy.tar.gz")
    mock_check_call.assert_called_with([sys.executable, "-m", "pip", "install", "dummy.tar.gz"])


def test_install_from_folder(tmp_path):
    # Simulate directory with .tar.gz and a subfolder
    dummy_pkg = tmp_path / "pkg.tar.gz"
    dummy_pkg.write_text("fake content")

    subdir = tmp_path / "myapp"
    subdir.mkdir()

    with mock.patch("install_app.install_package") as mock_install:
        install_app.install_from_folder(str(tmp_path))
        assert mock_install.call_count == 2
        assert mock_install.call_args_list[0][0][0] == str(dummy_pkg)
        assert mock_install.call_args_list[1][0][0] == str(subdir)


def test_install_from_folder_empty(tmp_path):
    with mock.patch("builtins.print") as mock_print:
        install_app.install_from_folder(str(tmp_path))
        mock_print.assert_any_call(f"No packages found in {str(tmp_path)}")


def test_main_single_package(monkeypatch):
    monkeypatch.setattr(sys, "argv", ["install_app.py", "dummy.tar.gz"])

    with mock.patch("install_app.uninstall_all"), mock.patch("install_app.reinstall_requirements"), mock.patch("install_app.install_package") as mock_install:
        install_app.main()
        mock_install.assert_called_with("dummy.tar.gz")


def test_main_directory(monkeypatch, tmp_path):
    monkeypatch.setattr(sys, "argv", ["install_app.py", str(tmp_path)])

    with mock.patch("install_app.uninstall_all"), mock.patch("install_app.reinstall_requirements"), mock.patch(
        "install_app.install_from_folder"
    ) as mock_folder:
        install_app.main()
        mock_folder.assert_called_with(str(tmp_path))


def test_main_invalid_args(monkeypatch):
    monkeypatch.setattr(sys, "argv", ["install_app.py"])

    with pytest.raises(SystemExit):
        install_app.main()
