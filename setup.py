"""
Dynamic build script. Installs Python and non-Python packages.
"""

import sys
import os

import setuptools
from setuptools import Extension

sys.path.insert(0, os.path.dirname(__file__))

import package_install
from scripts.include_lib_paths import (
    SDL2_INCLUDE,
    PYGAME_INCLUDE,
    PYTHON_GLOBAL_INCLUDE,
    PYGAME_LIB,
    SDL2_LIB,
    PYGAME_SECOND_LIB,
    SDL2_LIB_NAME,
    convert_path_sep,
)

package_install.install_packages()

c_extension: Extension = Extension(
    "_hotreload",
    sources=["_hotreload/src/_hotreload.c"],
    include_dirs=[
        os.path.join("_hotreload", "include"),
        SDL2_INCLUDE,
        PYGAME_INCLUDE,
        PYTHON_GLOBAL_INCLUDE,
    ],
    libraries=["SDL2"],
    library_dirs=[PYGAME_LIB, SDL2_LIB]
    + ([PYGAME_SECOND_LIB] if "linux" in sys.platform else []),
    extra_link_args=[f"{convert_path_sep(SDL2_LIB)}/{SDL2_LIB_NAME}"],
    language="c",
)

with open("README.md", "r+", encoding="utf8") as README:
    long_desc: str = README.read()

setuptools.setup(
    name="pygame_hotreloader",
    version="0.0.2",
    description="A hotreloader for Pygame.",
    long_description=long_desc,
    long_description_content_type="text/markdown",
    author="ram",
    author_email="ramzey.burdette2005@gmail.com",
    url="https://github.com/foxwithahdie/pygame-hotreloader",
    license="MIT",
    ext_modules=[c_extension],
    packages=["pygame_hotreloader"],
    package_dir={"": "src"},
    include_package_data=True,
    package_data={"pygame_hotreloader.resources.images": ["*.png"]},
    install_requires=["watchdog", "pygame>=2.6.0", "parse_cmake", "numpy"],
    extras_require={"dev": ["mypy"]},
    python_requires=">=3.9",
)
