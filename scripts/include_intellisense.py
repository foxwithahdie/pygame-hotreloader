"""
Script for editing c_cpp_properties.json for proper Intellisense in Visual Studio Code.
"""

import sys
import os
import json

from scripts.include_lib_paths import PYTHON_GLOBAL_INCLUDE, PYTHON_VENV_INCLUDE, \
                                      PYGAME_INCLUDE, SDL2_INCLUDE

# import constants to have variable intellisense, works on windows

JSONConfig = dict[str, list[dict[str, str | list[str]]] | int] # json config type with version


def vscode_format(file_path: str) -> str:
    """
    Converts path separators into Visual Studio Code's
    default variable `${/}`.

    Args:
        file_path (str): The file path string.

    Returns:
        str: The file path string, edited with
        the converted path separators.
    """
    return r"${/}".join(file_path.split(os.path.sep))


workspace_folder_variable: str = r"${workspaceFolder}"

python_venv_include = PYTHON_VENV_INCLUDE.replace(os.getcwd(), workspace_folder_variable)
pygame_include = PYGAME_INCLUDE.replace(os.getcwd(), workspace_folder_variable)

FILENAME = os.path.join(".vscode", "c_cpp_properties.json")


def include_intellisense() -> None:
    """
    Adds intellisense to Visual Studio Code's c_cpp_properties.json file according to your paths.
    """
    with open(FILENAME, "r", encoding="utf8") as props:
        c_cpp_properties: JSONConfig = json.load(props)

    index: int = -1
    for platform in c_cpp_properties["configurations"]:
        if sys.platform in platform["name"].lower() or \
            (platform["name"].lower() == "macos" and "darwin" in sys.platform):
            index = c_cpp_properties["configurations"].index(platform)

    c_cpp_properties["configurations"][index]["includePath"] = [
            r"${workspaceFolder}${/}**",
            vscode_format(PYTHON_GLOBAL_INCLUDE),
            vscode_format(python_venv_include),
            vscode_format(pygame_include),
            vscode_format(os.path.join(workspace_folder_variable, SDL2_INCLUDE))
        ]

    with open(FILENAME, "w", encoding="utf8") as props:
        json.dump(c_cpp_properties, props, indent=4)

    print("edited c_cpp_properties.json")


if __name__ == "__main__":
    include_intellisense()
