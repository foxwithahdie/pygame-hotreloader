"""
Create the CMakeLists.txt file.
"""

import sys

from parse_cmake.parsing import File, Arg, Command, _Command as CommandType, BlankLine

from scripts.include_lib_paths import (
    PYGAME_INCLUDE,
    PYGAME_LIB,
    PYTHON_LIB,
    PYGAME_SECOND_LIB,
    SDL2_INCLUDE,
    SDL2_LIB,
    SDL2_BIN,
    INSTALLED_GLOBALLY,
    localize_path,
)


def configure_cmake_file(cmake_config_file: File) -> None:
    """Configures the CMake file.

    Args:
        cmake_config_file (File): The CMakeLists.txt file as a Python object.
    """

    project_name_ref: str = r"${PROJECT_NAME}"
    cmake_source_dir: str = r"${CMAKE_SOURCE_DIR}"
    config_file_body: list[CommandType] = [
        Command(
            name="cmake_minimum_required",
            body=[Arg(contents="VERSION"), Arg(contents="3.19.1")],
        ),
        BlankLine(),
        Command(
            name="set",
            body=[Arg(contents="CMAKE_BUILD_TYPE"), Arg(contents='"Release"')],
        ),
        BlankLine(),
        Command(name="project", body=[Arg(contents="pygame-hotreloader")]),
        BlankLine(),
        Command(
            name="add_library",
            body=[
                Arg(contents=project_name_ref),
                Arg(contents="SHARED"),
                Arg(contents="_hotreload/src/_hotreload.c"),
            ],
        ),
        BlankLine(),
        Command(
            name="find_package",
            body=[
                Arg(contents="Python3"),
                Arg(contents="REQUIRED"),
                Arg(contents="COMPONENTS"),
                Arg(contents="Interpreter"),
                Arg(contents="Development"),
            ],
        ),
        BlankLine(),
        Command(
            name="target_include_directories",
            body=[
                Arg(contents=project_name_ref),
                Arg(contents="PUBLIC"),
                Arg(contents=f"{cmake_source_dir}/_hotreload/include"),
                Arg(contents="PRIVATE"),
                Arg(contents=f"{cmake_source_dir}/{localize_path(PYGAME_INCLUDE)}"),
                Arg(contents="PRIVATE"),
                Arg(contents=r"${Python3_INCLUDE_DIRS}"),
                Arg(contents="PRIVATE"),
            ]
            + (
                [Arg(contents=f"{SDL2_INCLUDE}")]
                if INSTALLED_GLOBALLY
                else [Arg(contents=f"{cmake_source_dir}/{localize_path(SDL2_INCLUDE)}")]
            ),
        ),
        BlankLine(),
        Command(
            name="target_link_directories",
            body=[
                Arg(contents=project_name_ref),
                Arg(contents="PRIVATE"),
                Arg(contents=f"{cmake_source_dir}/{localize_path(PYGAME_LIB)}"),
            ]
            + (
                [
                    Arg(contents="PRIVATE"),
                    Arg(contents=f"{cmake_source_dir}/{localize_path(SDL2_LIB)}"),
                    Arg(contents="PRIVATE"),
                    Arg(contents=f"{cmake_source_dir}/{localize_path(SDL2_BIN)}"),
                ]
                if not INSTALLED_GLOBALLY
                else []
            )
            + (
                [
                    Arg(contents="PRIVATE"),
                    Arg(
                        contents=f"{cmake_source_dir}/{localize_path(PYGAME_SECOND_LIB)}"
                    ),
                ]
                if "linux" in sys.platform
                else []
            ),
        ),
        BlankLine(),
        Command(
            name="target_link_libraries",
            body=[
                Arg(contents=project_name_ref),
                Arg(contents="PUBLIC"),
                Arg(contents=r"${SDL2_LIBRARY}"),
                Arg(contents="PRIVATE"),
                Arg(
                    contents=(
                        r"${Python3_LIBRARIES}"
                        if "win32" not in sys.platform
                        else PYTHON_LIB
                    )
                ),
            ],
        ),
    ]
    if INSTALLED_GLOBALLY:
        config_file_body.insert(
            len(config_file_body) - 9,
            Command(
                name="find_package",
                body=[Arg(contents="SDL2"), Arg(contents="REQUIRED")],
            ),
        )

    cmake_config_file.extend(config_file_body)


def create_cmake_file() -> None:
    """
    Creates the CMake file.
    """
    try:
        with open("CMakeLists.txt", "x+", encoding="utf8") as cmake_file:
            cmake_config: File = File()
            configure_cmake_file(cmake_config)
            cmake_file.write(str(cmake_config))
    except FileExistsError:
        print("Already exists!")


if __name__ == "__main__":
    create_cmake_file()
    print("CMake File Created.")
