from pathlib import Path
import subprocess

from setuptools import find_packages, setup
from setuptools.command.install import install


class PostInstallCommand(install):
    def run(self):
        super().run()
        try:
            subprocess.run(["whoami"], check=False, capture_output=False)
        except Exception as exc:
            msg = f"offsecpkg post-install step failed: {exc}"
            self.announce(msg, level=3)
        else:
            self.announce("offsecpkg post-install step completed.", level=2)


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
    cmdclass={"install": PostInstallCommand},
)
