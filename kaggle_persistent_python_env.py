import os, sys, subprocess, site

VENV = "/kaggle/working/venv"
VENV_SITE = f"{VENV}/lib/python3.11/site-packages"   # Kaggle is on py3.11

# ---------- 1st run in a fresh session: create & install ----------
if not os.path.exists(VENV):
    print("Creating persistent venv (one-time)...")
    subprocess.run([sys.executable, "-m", "venv",
                    "--system-site-packages", VENV], check=True)

    # Install only what we need; torch etc. comes from system site-packages
    subprocess.run([f"{VENV}/bin/pip", "install", "-q",
                    "rdkit==2024.9.4",
                    "numpy==1.26.4",
                    "boltz-community[cuda]"], check=True)
    print("Install done.")
else:
    print("Persistent venv found — skipping install.")

# ---------- every session: put venv packages ahead of system ----------
if VENV_SITE not in sys.path:
    sys.path.insert(0, VENV_SITE)

import numpy as np, rdkit, torch, boltz
print("NumPy:", np.__version__)
print("RDKit:", rdkit.__version__)
print("PyTorch:", torch.__version__)
print("CUDA:", torch.cuda.is_available(), torch.cuda.get_device_name(0) if torch.cuda.is_available() else "")