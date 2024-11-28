"""
Include path constants.
"""
import json
import sysconfig
import sys
import os

from linux_pkgm_detection import linux_detect_package_manager

JSONConfig = dict[str, list[dict[str, str | list[str]]]] # json config type

PYTHON_GLOBAL_INCLUDE: str = sysconfig.get_path("include", vars={"base": sys.base_prefix})
PYTHON_VENV_INCLUDE: str = os.path.join(sys.prefix,
                                        "include" if "win32" not in sys.platform else "Include"
                                    )
PYTHON_VENV_LIB: str = os.path.join(sys.prefix,
                                    "lib" if "win32" not in sys.platform else "Lib"
                                  )
PYGAME_INCLUDE: str = os.path.join(PYTHON_VENV_INCLUDE,
                              "site",
                              f"python{sys.version_info.major}.{sys.version_info.minor}",
                              "pygame"
                            )
if "win32" not in sys.platform:
    PYGAME_LIB: str = os.path.join(PYTHON_VENV_LIB,
                                f"python{sys.version_info.major}.{sys.version_info.minor}",
                                "site-packages",
                                "pygame"
                            )
else:
    PYGAME_LIB: str = os.path.join(PYTHON_VENV_LIB,
                                "site-packages",
                                "pygame"
                            )
if "linux" in sys.platform:
    PYGAME_SECOND_LIB: str = os.path.join(PYTHON_VENV_LIB,
                                       f"python{sys.version_info.major}.{sys.version_info.minor}",
                                        "site-packages",
                                        "pygame.libs"
                                    )
INSTALLED_GLOBALLY: bool = False

if "linux" in sys.platform:
    current_package_manager = linux_detect_package_manager()[0]
    with open("linux_package_managers.json", "r", encoding="utf8") as pkgms:
        package_managers: JSONConfig = json.load(pkgms)

    for package_manager in package_managers["package_managers"]:
        if package_manager["name"] == current_package_manager:
            for package in package_manager["essential_packages"]:
                if "sdl2" in package.lower():
                    INSTALLED_GLOBALLY = True


SDL2_INCLUDE: str = os.path.join(os.path.sep, "usr", "include", "SDL2") \
                    if INSTALLED_GLOBALLY \
                    else os.path.join("dependencies", "SDL2", "include", "SDL2")

LIB_FOLDER: str = "x86_64-linux-gnu"

SDL2_LIB: str = os.path.join(os.path.sep, "usr", "lib", LIB_FOLDER) \
                if INSTALLED_GLOBALLY \
                else os.path.join("dependencies", "SDL2", "lib")
