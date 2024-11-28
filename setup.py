"""
Dynamic build script. Installs Python and non-Python packages.
"""

import os

import setuptools
from setuptools import Extension

import pygame

from package_install import install_packages

install_packages()

pygame_lib = os.path.dirname(pygame.base.__file__)

c_extension: Extension = Extension(
    "pygame_hotreloader.c_extensions.c_extension",
    sources=["c_extensions/src/hot_reload.c"],
    include_dirs=["c_extensions/include"],
    libraries=[pygame_lib],
    library_dirs=["c_extensions/lib"]
)

long_desc: str

with open("README.md", "r+", encoding="utf8") as README:
    long_desc = README.read()

setuptools.setup(
    name="pygame_hotreloader",
    version="0.0.1",
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
    install_requires=["watchdog", "pygame>=2.6.0"],
    extras_require={"dev": ["mypy"]},
    python_requires=">=3.9"
)
