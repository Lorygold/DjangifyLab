import os
import subprocess
import sys
import shutil
import argparse

# example: > python test_app_upgrade.py --previous_version=example-apps/buffalogs-2.6.0.tar.gz --new_version=example-apps/buffalogs-2.7.0.tar.gz --fixture=example-apps/fixtures/buffalogs_complete_fixture.json --db=postgres

def parse_args():
    parser = argparse.ArgumentParser(description="Test upgrade of a Django reusable app between two versions.")
    parser.add_argument("--previous_version", required=True, help="Path to the older version of the app (.tar.gz)")
    parser.add_argument("--new_version", required=True, help="Path to the newer version of the app (.tar.gz)")
    parser.add_argument("--fixture", required=True, help="Path to the fixture file to load")
    parser.add_argument("--db", choices=["sqlite", "postgres"], default="sqlite", help="Which DB backend to use")
    return parser.parse_args()


def create_virtualenv(venv_path):
    print(f"Creating virtualenv at {venv_path}...")
    subprocess.check_call([sys.executable, "-m", "venv", venv_path])


def run_pip(venv_python, args):
    subprocess.check_call([venv_python, "-m", "pip"] + args)


def run_django_command(venv_python, command, *args, settings_module=None):
    cmd = [venv_python, "manage.py", command] + list(args)
    if settings_module:
        cmd += ["--settings", settings_module]
    subprocess.check_call(cmd)


def install_requirements(venv_python):
    print("Installing DjangifyLab requirements in venv...")
    run_pip(venv_python, ["install", "--upgrade", "pip"])
    run_pip(venv_python, ["install", "-r", "requirements.txt"])


def install_package(venv_python, package_path):
    print(f"Installing Django app package: {package_path}")
    run_pip(venv_python, ["install", package_path])


def set_django_settings(db_backend):
    if db_backend == "postgres":
        os.environ["DJANGO_SETTINGS_MODULE"] = "djangifylab_project.settings_pg"
    else:
        os.environ["DJANGO_SETTINGS_MODULE"] = "djangifylab_project.settings"


def main():
    args = parse_args()

    venv_path = "temp_upgrade_venv"
    venv_python = os.path.join(venv_path, "bin", "python")
    settings_module = "djangifylab_project.settings_pg" if args.db == "postgres" else "djangifylab_project.settings"

    if os.path.exists(venv_path):
        print("Removing existing virtual environment...")
        shutil.rmtree(venv_path)

    create_virtualenv(venv_path)
    install_requirements(venv_python)

    # Install and test the previous version
    print(f"\n--- Installing previous version: {args.previous_version} ---")
    install_package(venv_python, args.previous_version)
    run_django_command(venv_python, "makemigrations", settings_module=settings_module)
    run_django_command(venv_python, "migrate", settings_module=settings_module)
    run_django_command(venv_python, "loaddata", args.fixture, settings_module=settings_module)

    print("\nPrevious version installed, migrated, and fixture loaded successfully.")

    # Install and test the new version
    print(f"\n--- Upgrading to new version: {args.new_version} ---")
    install_package(venv_python, args.new_version)
    run_django_command(venv_python, "makemigrations", settings_module=settings_module)
    run_django_command(venv_python, "migrate", settings_module=settings_module)

    print("\nNew version installed and migrations applied successfully.")
    print("\nUpgrade test completed without errors.")



if __name__ == "__main__":
    main()
