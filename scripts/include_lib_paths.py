"""
Include path constants.
"""

import json
import sysconfig
import sys
import os

from package_install import linux_detect_package_manager

JSONConfig = dict[str, list[dict[str, str | list[str]]]]  # json config type


def localize_path(path: str) -> str:
    """Turns the complete path string into a relative path.

    Args:
        path (str): The complete path.

    Returns:
        str: The relative path.
    """
    return "/".join(path.removeprefix(os.getcwd() + os.path.sep).split(os.path.sep))


def convert_path_sep(path: str) -> str:
    """Converts a Windows-style path into a Unix-style path.

    Args:
        path (str): The Windows-style path.

    Returns:
        str: The Unix-style path.
    """
    return "/".join(path.split("\\"))


PYTHON_LIB: str | None = (
    convert_path_sep(
        os.path.join(
            sys.base_prefix,
            "libs",
            f"python{sys.version_info.major}{sys.version_info.minor}.lib",
        )
    )
    if "win32" in sys.platform
    else None
)


PYTHON_GLOBAL_INCLUDE: str = sysconfig.get_path(
    "include", vars={"base": sys.base_prefix}
)
PYTHON_VENV_INCLUDE: str = os.path.join(
    sys.prefix, "include" if "win32" not in sys.platform else "Include"
)
PYTHON_VENV_LIB: str = os.path.join(
    sys.prefix, "lib" if "win32" not in sys.platform else "Lib"
)
PYGAME_INCLUDE: str = os.path.join(
    PYTHON_VENV_INCLUDE,
    "site",
    f"python{sys.version_info.major}.{sys.version_info.minor}",
    "pygame",
)
if "win32" not in sys.platform:
    PYGAME_LIB: str = os.path.join(
        PYTHON_VENV_LIB,
        f"python{sys.version_info.major}.{sys.version_info.minor}",
        "site-packages",
        "pygame",
    )
else:
    PYGAME_LIB: str = os.path.join(PYTHON_VENV_LIB, "site-packages", "pygame")

PYGAME_SECOND_LIB: str | None = None
if "linux" in sys.platform:
    PYGAME_SECOND_LIB = os.path.join(
        PYTHON_VENV_LIB,
        f"python{sys.version_info.major}.{sys.version_info.minor}",
        "site-packages",
        "pygame.libs",
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
elif "darwin" in sys.platform:
    INSTALLED_GLOBALLY = True

if "darwin" in sys.platform:
    SDL2_INCLUDE: str = (
        os.path.join(os.path.sep, "usr", "local", "include", "SDL2")
        if INSTALLED_GLOBALLY
        else os.path.join(
            "dependencies",
            "SDL2",
            "include",
            "SDL2" if "win32" not in sys.platform else "",
        )
    )
else:
    SDL2_INCLUDE: str = (
        os.path.join(os.path.sep, "usr", "include", "SDL2")
        if INSTALLED_GLOBALLY
        else os.path.join(
            "dependencies", "SDL2", "include", "" if "win32" in sys.platform else "SDL2"
        )
    )


LIB_FOLDER: str = "x86_64-linux-gnu"

SDL2_LIB: str = (
    (
        os.path.join(os.path.sep, "usr", "lib", LIB_FOLDER)
        if "linux" in sys.platform
        else os.path.join(os.path.sep, "usr", "local", "lib")
    )
    if INSTALLED_GLOBALLY
    else os.path.join("dependencies", "SDL2", "lib")
    + ((os.path.sep + "x64") if "win32" in sys.platform else "")
)

SDL2_BIN: str = (
    ""
    if INSTALLED_GLOBALLY
    else os.path.join(
        "dependencies", "SDL2", "bin" if "win32" not in sys.platform else "lib"
    )
)

SDL2_LIB_NAME: str = "SDL2.lib"

if __name__ == "__main__":
    print(SDL2_LIB)
    print(SDL2_INCLUDE)
