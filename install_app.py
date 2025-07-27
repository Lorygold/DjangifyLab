import os
import subprocess
import sys


def uninstall_all():
    """Uninstall all the packages in the venv to clean the environment"""
    installed = subprocess.check_output([sys.executable, "-m", "pip", "freeze"], text=True).splitlines()

    if installed:
        print("Uninstalling existing packages...")
        subprocess.check_call([sys.executable, "-m", "pip", "uninstall", "-y"] + installed)


def reinstall_requirements():
    """Install the requirements.txt packages needed by the DjangifyLab itself"""
    requirements_path = os.path.join(os.getcwd(), "requirements.txt")
    if not os.path.isfile(requirements_path):
        print("requirements.txt not found in current directory.")
        sys.exit(1)

    print("Installing DjangifyLab requirements...")
    subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", requirements_path])


def install_package(path: str) -> None:
    """Install the single Django reusable app defined in the command
    Example: > python install_app.py buffalogs-2.7.0.tar.gz
    """
    print(f"Installing app: {path}")
    subprocess.check_call([sys.executable, "-m", "pip", "install", path])


def install_from_folder(folder_path: str) -> None:
    """Install all the Django reusable apps in the folder indicated
    Example: > python install_app.py example_apps/
    """
    if not os.path.isdir(folder_path):
        print("Error: {folder_path} is not a valid directory.")
        sys.exit(1)

    entries = os.listdir(folder_path)
    if not entries:
        print(f"No packages found in {folder_path}")
        return

    for item in entries:
        full_path = os.path.join(folder_path, item)
        if os.path.isdir(full_path) or item.endswith((".tar.gz", ".whl")):
            install_package(full_path)


def main():
    if len(sys.argv) != 2:
        print("Usage: python install_app.py <package_name_or_directory>")
        sys.exit(1)

    target = sys.argv[1]

    uninstall_all()
    reinstall_requirements()

    if os.path.isdir(target):
        install_from_folder(target)
    else:
        install_package(target)

    print("\nApp(s) installed successfully.")
    print("Remember to manually add the installed app(s) to `INSTALLED_APPS` if needed.")


if __name__ == "__main__":
    main()
