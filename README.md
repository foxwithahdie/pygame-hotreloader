# pygame-hotreloader

A hotreloader for Pygame.

This will be a tool used for Pygame developers to be able to hotreload their game.

## v0.0.1:

### Project Setup

Before installing this library, make sure that you have pygame already installed in a virtual environment.
Run:
```
pip install pygame
```

#### Windows

Make sure you have either MSVC or MinGW installed.

Go to the [SDL2 installation page](https://github.com/libsdl-org/SDL/releases) and
install the SDL2 development version that corresponds with your C/C++ compiler.
Drop the zip file that it installs into the `dependencies` folder.

Once you have done this, make sure to run:

```
pip install -e .
```

This should install any necessary packages for Python.

#### MacOS

Make sure that you have [Homebrew](https://brew.sh/) installed before proceeding with installing this library.

#### Linux

Should install all of the necessary packages through your package manager.


### Plans:

- Will keep the main screen available, but the things shown will change. Will display a refresh icon OR will allow for refresh via keybind.
- If there is an error, will either show a red screen displaying the exception OR will crash the program.
- Refresh icon will fade after refresh
- Allow for ability to set it to automatically refresh or manually refresh via keybind
- Runs when a file is changed in all packages in a folder
- Fast

### TODO
    - Determine where SDL2 would be globally installed for different OSes that can globally install SDL2
    - Set up CMake
    - Find ways to transfer your c_cpp_properties.json without pushing it to version control
    - Find way to compile C extension without dynamically linked libraries being in the same directory
    