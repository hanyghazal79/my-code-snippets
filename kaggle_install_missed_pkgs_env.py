import sys
import subprocess
import importlib.util
from pathlib import Path

# 1. Define the persistent environment directory (must be under /kaggle/working)
#    Ensure notebook persistence is set to "Files only" or "Variables and Files"
#    in Notebook options so this directory survives across sessions.
ENV_DIR = Path("/kaggle/working/persistent_env")
ENV_DIR.mkdir(parents=True, exist_ok=True)

# 2. Ensure the persistent directory is on sys.path so packages installed
#    in a previous session are importable immediately.
if str(ENV_DIR) not in sys.path:
    sys.path.insert(0, str(ENV_DIR))

def install_if_missing(package: str, target_dir: Path = ENV_DIR) -> None:
    """
    Install a package into the target directory only if it is not already importable.
    This makes the cell idempotent: running it multiple times will not reinstall
    already-present packages.
    """
    # Check if the package is already available (either from system or from
    # a previous persistent install).
    if importlib.util.find_spec(package) is not None:
        print(f"[skip] {package} is already available.")
        return

    print(f"[install] {package} -> {target_dir}")
    # Install into the persistent directory. pip will also resolve dependencies
    # and place them in the same target directory.
    subprocess.check_call(
        [
            sys.executable,
            "-m",
            "pip",
            "install",
            "--target",
            str(target_dir),
            "--upgrade",          # optional: ensures latest compatible version
            "--no-cache-dir",     # avoids filling /root/.cache
            package,
        ]
    )

# 3. List of dependencies you need. Add or remove as needed.
REQUIRED_PACKAGES = [
    "cowsay",          # example
    # "opensmile",
    # "some-other-package==1.2.3",
]

# 4. Install only the missing ones.
for pkg in REQUIRED_PACKAGES:
    install_if_missing(pkg)

print("\nPersistent environment ready at:", ENV_DIR)