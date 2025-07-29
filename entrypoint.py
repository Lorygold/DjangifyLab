import argparse
import os
import subprocess
import sys


def uninstall_all():
    print("Uninstalling all packages...")
    installed = subprocess.check_output([sys.executable, "-m", "pip", "freeze"], text=True).splitlines()
    if installed:
        subprocess.check_call([sys.executable, "-m", "pip", "uninstall", "-y"] + installed)


def reinstall_requirements():
    print("Reinstalling base requirements...")
    if not os.path.isfile("requirements.txt"):
        print("ERROR: requirements.txt not found.")
        sys.exit(1)
    subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])


def install_package(path: str):
    print(f"Installing app: {path}")
    subprocess.check_call([sys.executable, "-m", "pip", "install", path])


def install_from_folder(folder_path: str):
    print(f"Installing all packages from: {folder_path}")
    for item in os.listdir(folder_path):
        full_path = os.path.join(folder_path, item)
        if os.path.isdir(full_path) or item.endswith((".tar.gz", ".whl")):
            install_package(full_path)


def run_django_command(*args, settings_module="djangifylab_project.settings_pg"):
    cmd = [sys.executable, "manage.py"] + list(args) + ["--settings", settings_module]
    subprocess.check_call(cmd)


def run_upgrade(previous, new, fixture, db_engine):
    print("Starting upgrade test...")
    reinstall_requirements()
    os.environ["DJANGO_SETTINGS_MODULE"] = "djangifylab_project.settings_pg" if db_engine == "postgres" else "djangifylab_project.settings"

    # Install previous
    install_package(previous)
    run_django_command("makemigrations")
    run_django_command("migrate")
    run_django_command("loaddata", fixture)

    # Install new version
    install_package(new)
    run_django_command("makemigrations")
    run_django_command("migrate")

    print("Upgrade test completed successfully.")


def main():
    # Installation example: > python entrypoint.py --mode=install --target=example-apps/packages/buffalogs-2.7.0.tar.gz --db=postgres
    # Upgrade example: > (djangifylab) lorygold@lorygold-T15:~/Projects/Personal/DjangifyLab$ python entrypoint.py --mode=upgrade --previous_version=example-apps/packages/buffalogs-2.7.0.tar.gz --new_version=example-apps/packages/buffalogs-2.8.0.tar.gz --fixture=example-apps/fixtures/buffalogs_complete_fixtures.json --db=postgres
    parser = argparse.ArgumentParser(description="Unified entrypoint for DjangifyLab tasks")
    parser.add_argument("--mode", choices=["install", "upgrade"], required=True)
    parser.add_argument("--target", help="Package or folder path for install mode")
    parser.add_argument("--previous_version", help="Path to previous .tar.gz")
    parser.add_argument("--new_version", help="Path to new .tar.gz")
    parser.add_argument("--fixture", help="Fixture JSON path")
    parser.add_argument("--db", choices=["sqlite", "postgres"], default="sqlite")
    args = parser.parse_args()

    if args.mode == "install":
        uninstall_all()
        reinstall_requirements()
        if args.target:
            if os.path.isdir(args.target):
                install_from_folder(args.target)
            else:
                install_package(args.target)
    elif args.mode == "upgrade":
        if not (args.previous_version and args.new_version and args.fixture):
            print("ERROR: --previous_version, --new_version, and --fixture are required for upgrade mode.")
            sys.exit(1)
        run_upgrade(args.previous_version, args.new_version, args.fixture, args.db)


if __name__ == "__main__":
    main()
