#!/usr/bin/env python3
"""Apply the shipped iOS OpenGL patch before compiling Wine components."""
from pathlib import Path
import subprocess

root = Path(__file__).resolve().parents[2]
wine = root / "wine"
patch = root / "patches/wine-opengl-winios.patch"


def apply(*arguments):
    return subprocess.run(
        ["git", "-C", str(wine), "apply", *arguments, str(patch)],
        capture_output=True, text=True,
    )


if not (wine / "configure").is_file():
    raise SystemExit("Wine source is missing. Initialize the wine submodule first.")
if apply("--reverse", "--check").returncode == 0:
    print("Wine iOS OpenGL patch already applied.")
else:
    check = apply("--check")
    if check.returncode:
        raise SystemExit("Cannot apply the Wine iOS OpenGL patch:\n" + check.stderr)
    result = apply()
    if result.returncode:
        raise SystemExit(result.stderr)
    print("Applied Wine iOS OpenGL patch.")
