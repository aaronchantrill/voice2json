# -*- mode: python -*-
import os
import site
from pathlib import Path

from PyInstaller.utils.hooks import copy_metadata

block_cipher = None

prefix = Path("/usr/lib/voice2json")

site_dirs = site.getsitepackages()
lib_dir = prefix / "lib"
for lib_python_dir in lib_dir.glob("python*"):
    site_dir = lib_python_dir / "site-packages"
    if site_dir.is_dir():
        site_dirs.append(site_dir)

# Look for compiled artifacts
artifacts = ["_webrtcvad.*.so"]
found_artifacts = {}
for site_dir in site_dirs:
    site_dir = Path(site_dir)
    for artifact in artifacts:
        artifact_paths = list(site_dir.glob(artifact))
        if artifact_paths:
            found_artifacts[artifact] = artifact_paths[0]
            continue

missing_artifacts = set(artifacts) - set(found_artifacts)
assert not missing_artifacts, missing_artifacts

a = Analysis(
    [Path.cwd() / "__main__.py"],
    pathex=["."],
    binaries=[(p, ".") for p in found_artifacts.values()],
    datas=copy_metadata("webrtcvad"),
    hiddenimports=["networkx"],
    hookspath=[],
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)
pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)
exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name="voice2json",
    debug=False,
    bootloader_ignore_signals=False,
    strip=True,
    upx=True,
    console=True,
)
coll = COLLECT(
    exe, a.binaries, a.zipfiles, a.datas, strip=True, upx=True, name="voice2json"
)
