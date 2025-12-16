#!/usr/bin/env python
"""
Script to install pyopenms with the version specified in conf.py
This is used by ReadTheDocs build process to ensure the correct version is installed.
"""
import subprocess
import sys
import re
from pathlib import Path

def get_version_from_conf():
    """Extract version from docs/source/conf.py"""
    conf_path = Path(__file__).parent.resolve() / "source" / "conf.py"
    
    with open(conf_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Look for version = u'X.Y.Z' pattern (with word boundary to be more specific)
    match = re.search(r"\bversion\s*=\s*u?['\"]([^'\"]+)['\"]", content)
    
    if match:
        version = match.group(1)
        print(f"Found version in conf.py: {version}")
        return version
    else:
        raise ValueError("Could not find version in conf.py")

def install_pyopenms(version):
    """Install pyopenms with specific version"""
    print(f"Installing pyopenms=={version}")
    
    # Use the extra index URL for pyopenms
    subprocess.check_call([
        sys.executable, "-m", "pip", "install",
        "--extra-index-url", "https://pypi.cs.uni-tuebingen.de/simple/",
        f"pyopenms=={version}"
    ])
    
    print(f"Successfully installed pyopenms=={version}")

if __name__ == "__main__":
    try:
        version = get_version_from_conf()
        install_pyopenms(version)
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)
