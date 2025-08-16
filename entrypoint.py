import argparse
import os
import re
import subprocess
import sys

from tabulate import tabulate


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


def run_django_command(*args):
    cmd = [sys.executable, "manage.py"] + list(args)
    subprocess.check_call(cmd)


def run_upgrade(previous, new, fixture):
    print("Starting upgrade test...")
    reinstall_requirements()
    os.environ["DJANGO_SETTINGS_MODULE"] = "djangifylab_project.settings"

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

def extract_version(filename):
    match = re.search(r'(\d+\.\d+\.\d+)', filename)
    return match.group(1) if match else None


def run_matrix(packages_dir, fixture):
    print(f"📊 Running upgrade compatibility matrix in {packages_dir} with fixture {fixture}")
    os.makedirs("/app/logs", exist_ok=True)

    pkgs = [os.path.join(packages_dir, p) for p in os.listdir(packages_dir)
            if p.endswith((".tar.gz", ".whl"))]
    pkgs_versions = sorted(((extract_version(p), p) for p in pkgs if extract_version(p)),
                           key=lambda x: list(map(int, x[0].split("."))))

    versions = [v for v, _ in pkgs_versions]
    matrix = []

    for src_version, src_path in pkgs_versions:
        row = []
        for dst_version, dst_path in pkgs_versions:
            if src_version == dst_version:
                row.append(" ")
                continue
            try:
                uninstall_all()
                run_upgrade(src_path, dst_path, fixture)
                row.append("YES")
            except subprocess.CalledProcessError:
                row.append("NO")
        matrix.append(row)

    # Results printed on the console
    print("\nUpgrade Compatibility Matrix:\n")
    table_str = tabulate(matrix, headers=versions, showindex=versions, tablefmt="grid")
    print(table_str)

    # save markdown file with results
    md_table = tabulate(matrix, headers=versions, showindex=versions, tablefmt="github")
    md_content = (
        "# Upgrade Compatibility Matrix\n\n"
        f"Fixture used: `{fixture}`\n\n"
        f"Packages folder: `{packages_dir}`\n\n"
        f"{md_table}\n"
    )

    output_file = "upgrade_logs/compatibility_matrix.md"
    with open(output_file, "w") as f:
        f.write(md_content)

    print(f"\n Compatibility matrix saved to {output_file}")



def main():
    # Installation example: > python entrypoint.py --mode=install --target=example-apps/packages/buffalogs-2.7.0.tar.gz
    # Upgrade example: > python entrypoint.py --mode=upgrade --previous_version=example-apps/packages/buffalogs-2.7.0.tar.gz --new_version=example-apps/packages/buffalogs-2.8.0.tar.gz --fixture=example-apps/fixtures/buffalogs_complete_fixtures.json
    # Versions compatibility example: > python entrypoint.py --mode matrix --packages /app/packages --fixture /app/fixtures/buffalogs_complete_fixture.json
    parser = argparse.ArgumentParser(description="Unified entrypoint for DjangifyLab tasks")
    parser.add_argument("--mode", choices=["install", "upgrade", "matrix"], required=True)
    parser.add_argument("--target", help="Package or folder path for install mode")
    parser.add_argument("--previous_version", help="Path to previous .tar.gz")
    parser.add_argument("--new_version", help="Path to new .tar.gz")
    parser.add_argument("--fixture", help="Fixture JSON path")
    parser.add_argument("--packages", help="Folder containing multiple versions for matrix mode")

    args = parser.parse_args()

    uninstall_all()
    reinstall_requirements()

    if args.mode == "install":
        if args.target:
            if os.path.isdir(args.target):
                install_from_folder(args.target)
            else:
                install_package(args.target)
    elif args.mode == "upgrade":
        if not (args.previous_version and args.new_version and args.fixture):
            print("ERROR: --previous_version, --new_version, and --fixture are required for upgrade mode.")
            sys.exit(1)
        run_upgrade(args.previous_version, args.new_version, args.fixture)
    elif args.mode == "matrix":
        if not (args.packages and args.fixture):
            print("ERROR: --packages and --fixture are required for matrix mode.")
            sys.exit(1)
        run_matrix(args.packages, args.fixture)


if __name__ == "__main__":
    main()
