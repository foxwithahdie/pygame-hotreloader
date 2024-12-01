"""
    Script for installing all of the necessary packages outside of pip for project to run.
    Designed for all OSes.
"""

import os
import shutil
import subprocess
import sys
import zipfile
import json

JSONConfigList = list[dict[str, str | list[str]]] # json config list type

def linux_load_package_manager_config(
        config_file: str = "linux_package_managers.json"
    ) -> JSONConfigList:
    """
    Loads the package manager json and its accompanying files from a json to a list of dictionaries.

    Args:
        config_file (str, optional): The configuration file. 
        Defaults to "linux_package_managers.json".

    Raises:
        FileNotFoundError: If the configuration file does not exist inside the folder.

    Returns:
        list[dict[str, str | list[str]]]: The json file converted into a Python object.
        It is a list of dictionaries with each dictionary containing the name of the
        package manager, it's install keyword, and the essential packages needed for
        the project.
    """
    if not os.path.exists(config_file):
        raise FileNotFoundError("Configuration file not found.")
    with open(config_file, "r", encoding="utf8") as file:
        data = json.load(file)
    return data.get("package_managers", [])


def linux_detect_package_manager(
        config_file : str = "linux_package_managers.json"
    ) -> tuple[str, str | None, list[str]] | None:
    """
    Finds the first available linux distribution package manager and its
    corresponding install keyword.

    Args:
        config_file (str, optional): The file containing popular 
        Linux distribution package manager and its install keyword(s). 
        Defaults to "linux_package_managers.json".

    Returns:
        tuple[str, str | None, list[str]]: Returns the first available
        Linux distribution package manager, its install keyword, if it exists,
        and its required packages.
    """
    package_managers: JSONConfigList = linux_load_package_manager_config(config_file)

    for manager in package_managers:
        if shutil.which(manager["name"]):
            return manager["name"], \
                   manager["install"] if manager["install"] != "" else None, \
                   manager["essential_packages"]

def linux_installation() -> list[str]:
    """
    Installs the required packages on Linux distributions.

    Returns:
        list[str]: The list of packages that were installed.
    """
    package_manager, install_kw, packages = linux_detect_package_manager()
    if install_kw is not None:
        subprocess.call(['sudo', package_manager, install_kw, *packages])
    else:
        subprocess.call(['sudo', package_manager, *packages])

    if not any("sdl" in pkg.lower() for pkg in packages):
        if shutil.which("flatpak"):
            subprocess.call(["flatpak", "install", "flathub", "org.libsdl.SDL2"])
        elif shutil.which("snap"):
            subprocess.call(["snap", "install", "sdl2"])
        else:
            subprocess.call(["git", "clone", "https://github.com/libsdl-org/SDL.git",
                            "-b", "SDL2"])
            subprocess.call(["cd", "SDL"])
            subprocess.call(["mkdir", "build"])
            subprocess.call(["cd", "build"])
            subprocess.call(os.path.join("..", "configure"))
            subprocess.call(["make"])
            subprocess.call(["sudo", "make", "install"])

    return packages


def macos_installation() -> list[str]:
    """
    Installs the required packages on MacOS.

    Returns:
        list[str]: The list of packages that were installed.
    """
    packages: list[str] = ["sdl2"]
    try:
        check_x_code_installation: subprocess.CompletedProcess[str] = \
            subprocess.run(['xcode-select', '-p'], capture_output=True,
                            text=True, check=True)
        if check_x_code_installation:
            try:
                subprocess.run(["clang", "--version"], check=True)
            except subprocess.CalledProcessError as _:
                subprocess.call("brew", "install", "clang")
    except (subprocess.CalledProcessError, FileNotFoundError) as _:
        print("Installing X-Code Command Line Tools. This may take a while...")
        subprocess.call(["xcode-select", "--install"])
    subprocess.call(["brew", "install", *packages])

    return packages


def windows_installation() -> list[str]:
    """
    Installs the required packages on Windows.

    Returns:
        list[str]: The list of packages that were installed.
    """
    packages: list[str] = ["SDL2"]
    dependencies_folder = os.listdir("dependencies")
    sdl2_zip = dependencies_folder[0]
    mingw = "mingw" in sdl2_zip
    with zipfile.ZipFile(os.path.join("dependencies", sdl2_zip), "a") as zip_file:
        zip_file.extractall("dependencies")
    dependencies_folder = os.listdir("dependencies")
    sdl_folder = ""
    for file in dependencies_folder:
        if os.path.isdir(os.path.join("dependencies", file)):
            sdl_folder = os.path.join("dependencies", file)
            break
    if mingw:
        sdl2_sources = os.path.join(sdl_folder, "x86_64-w64-mingw32")
        shutil.move(sdl2_sources, "dependencies")
        os.rename(os.path.join("dependencies", "x86_64-w64-mingw32"),
                os.path.join("dependencies", "SDL2"))
    else:
        subprocess.call(["mkdir", os.path.join("dependencies", "SDL2")])
        shutil.move(os.path.join(sdl_folder, "cmake"),
                    os.path.join("dependencies", "SDL2"))
        shutil.move(os.path.join(sdl_folder, "docs"),
                    os.path.join("dependencies", "SDL2"))
        shutil.move(os.path.join(sdl_folder, "include"),
                    os.path.join("dependencies", "SDL2"))
        shutil.move(os.path.join(sdl_folder, "lib"),
                    os.path.join("dependencies", "SDL2"))

    os.remove(os.path.join("dependencies", sdl2_zip))

    return packages


def install_packages() -> None:
    """
    Installs all the necessary packages depending on your OS.
    """
    try:
        packages: list[str] = []
        with open("installed.txt", "x+", encoding="utf8") as f:
            if 'linux' in sys.platform:
                packages = linux_installation()
            elif 'darwin' in sys.platform:
                packages = macos_installation()
            elif 'win32' in sys.platform:
                packages = windows_installation()

            f.write("Installed" + ", ".join(packages))

    except FileExistsError as _:
        print("Already installed.")


if __name__ == "__main__":
    install_packages()
    print("Packages installed.")
