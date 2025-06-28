import sys
import subprocess

if len(sys.argv) != 2:
    sys.exit(1)

pkg = sys.argv[1]
subprocess.check_call([sys.executable, '-m', 'pip', 'install', pkg])
print("\nPackage installed. Now add the app to settings.py > INSTALLED_APPS manually.")