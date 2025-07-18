import sys
import subprocess
import os

if len(sys.argv) != 2:
    print("Usage: python install_clean.py <package_name>")
    sys.exit(1)

pkg = sys.argv[1]

# Step 1: Get installed packages
installed = subprocess.check_output(
    [sys.executable, "-m", "pip", "freeze"],
    text=True
).splitlines()

# Step 2: Uninstall all packages
if installed:
    print("Uninstalling existing packages...")
    subprocess.check_call(
        [sys.executable, "-m", "pip", "uninstall", "-y"] + installed
    )

# Step 3: Reinstall DjangifyLab requirements
requirements_path = os.path.join(os.getcwd(), "requirements.txt")
if not os.path.isfile(requirements_path):
    print("requirements.txt not found in current directory.")
    sys.exit(1)

print("Installing DjangifyLab requirements...")
subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", requirements_path])

# Step 4: Install the given package/app
print(f"Installing app package: {pkg}")
subprocess.check_call([sys.executable, "-m", "pip", "install", pkg])

print("\nPackage installed successfully.")
print("Now add the app to `settings.py > INSTALLED_APPS` manually.")
