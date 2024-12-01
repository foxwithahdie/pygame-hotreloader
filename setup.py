"""
Dynamic build script. Installs Python and non-Python packages.
"""

import os

import setuptools
from setuptools import Extension

import pygame

from package_install import install_packages
from scripts.include_lib_paths import SDL2_INCLUDE, PYGAME_INCLUDE, PYTHON_GLOBAL_INCLUDE, \
                              PYGAME_LIB, SDL2_LIB, SDL2_BIN

install_packages()

pygame_lib = os.path.dirname(pygame.base.__file__)

c_extension: Extension = Extension(
    "_hotreload",
    sources=["_hotreload/src/_hotreload.c"],
    include_dirs=[
        "_hotreload/include",
        SDL2_INCLUDE,
        PYGAME_INCLUDE,
        PYTHON_GLOBAL_INCLUDE
    ],
    libraries=[pygame_lib],
    library_dirs=[
        "_hotreload/lib",
        PYGAME_LIB,
        SDL2_LIB
    ],
    language="c",
    runtime_library_dirs=[SDL2_BIN]
    #extra_link_args=
)

with open("README.md", "r+", encoding="utf8") as README:
    long_desc: str = README.read()

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
