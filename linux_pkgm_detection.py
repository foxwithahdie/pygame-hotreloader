"""
Functions for package manager detection.
"""
import json
import os
import shutil

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
