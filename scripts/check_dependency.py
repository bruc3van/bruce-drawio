#!/usr/bin/env python3
"""
Draw.io dependency check script (cross-platform: Windows / macOS / Linux)
"""
import subprocess
import sys
import os
import platform
import shutil


def get_platform():
    """Return normalized platform name."""
    s = platform.system().lower()
    if s == "darwin":
        return "mac"
    if s == "windows":
        return "win"
    return "linux"


def find_drawio():
    """Locate the draw.io CLI executable. Returns path or None."""
    plat = get_platform()

    if plat == "mac":
        candidates = [
            "/Applications/draw.io.app/Contents/MacOS/draw.io",
            "/Applications/draw.io.app/Contents/MacOS/drawio",
            os.path.expanduser("~/Applications/draw.io.app/Contents/MacOS/draw.io"),
        ]
    elif plat == "win":
        program_dirs = [
            os.environ.get("PROGRAMFILES", r"C:\Program Files"),
            os.environ.get("PROGRAMFILES(X86)", r"C:\Program Files (x86)"),
            os.environ.get("LOCALAPPDATA", ""),
        ]
        candidates = []
        for d in program_dirs:
            if d:
                candidates.append(os.path.join(d, "draw.io", "draw.io.exe"))
        # Also check user-scoped install
        appdata = os.environ.get("LOCALAPPDATA", "")
        if appdata:
            candidates.append(os.path.join(appdata, "Programs", "draw.io", "draw.io.exe"))
    else:
        candidates = [
            "/usr/bin/drawio",
            "/usr/local/bin/drawio",
            "/snap/bin/drawio",
            os.path.expanduser("~/.local/bin/drawio"),
        ]

    # Check explicit candidates first
    for path in candidates:
        if os.path.isfile(path) and os.access(path, os.X_OK if plat != "win" else os.F_OK):
            return path

    # Fallback: check PATH
    which = shutil.which("draw.io") or shutil.which("drawio")
    if which:
        return which

    return None


def install_drawio():
    """Attempt to install draw.io using the platform package manager."""
    plat = get_platform()

    if plat == "mac":
        if not shutil.which("brew"):
            print("Homebrew not found. Install draw.io manually: https://github.com/jgraph/drawio-desktop/releases")
            return None
        print("Installing draw.io via Homebrew...")
        cmd = ["brew", "install", "--cask", "drawio"]
    elif plat == "win":
        if shutil.which("winget"):
            print("Installing draw.io via winget...")
            cmd = ["winget", "install", "--id", "JGraph.Draw", "--accept-source-agreements", "--accept-package-agreements"]
        elif shutil.which("choco"):
            print("Installing draw.io via Chocolatey...")
            cmd = ["choco", "install", "drawio", "-y"]
        else:
            print("No package manager found (winget/choco).")
            print("Download manually: https://github.com/jgraph/drawio-desktop/releases")
            return None
    else:
        if shutil.which("snap"):
            print("Installing draw.io via snap...")
            cmd = ["snap", "install", "drawio"]
        else:
            print("Download manually: https://github.com/jgraph/drawio-desktop/releases")
            return None

    try:
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=300)
        if result.returncode == 0:
            print("draw.io installed successfully.")
            return find_drawio()
        else:
            print(f"Installation failed: {result.stderr.strip()}")
            return None
    except subprocess.TimeoutExpired:
        print("Installation timed out.")
        return None
    except Exception as e:
        print(f"Installation error: {e}")
        return None


def get_export_command(drawio_path):
    """Return a sample export command for the current platform."""
    plat = get_platform()
    if plat == "win":
        return f'"{drawio_path}" -x -f png -o output.png diagram.drawio'
    return f"{drawio_path} -x -f png -o output.png diagram.drawio"


def main():
    drawio_path = find_drawio()

    if drawio_path:
        print(f"draw.io found: {drawio_path}")
        print(f"Platform: {get_platform()}")
        print(f"Export example: {get_export_command(drawio_path)}")
        return 0

    print("draw.io not found. Attempting install...")
    drawio_path = install_drawio()
    if drawio_path:
        print(f"draw.io ready: {drawio_path}")
        print(f"Export example: {get_export_command(drawio_path)}")
        return 0

    print("Auto-install failed.")
    print("Manual install: https://github.com/jgraph/drawio-desktop/releases")
    return 1


if __name__ == "__main__":
    sys.exit(main())
