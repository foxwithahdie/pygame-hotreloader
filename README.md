# pygame-hotreloader

A hotreloader for Pygame.

This will be a tool used for Pygame developers to be able to hotreload their game.

## v0.0.2:

### Project Setup

This library will ONLY work on CPython. If you have any other Python version that you are willing to add support for, let me know!

#### Windows

Make sure you have either MSVC or MinGW installed.

Go to the [SDL2 installation page](https://github.com/libsdl-org/SDL/releases) and
install the SDL2 development version that corresponds with your C/C++ compiler.
Drop the zip file that it installs into the `dependencies` folder.

Once you have done this, make sure to run:

```
pip install .
```

This should install any necessary packages for Python.

#### MacOS

Make sure that you have [Homebrew](https://brew.sh/) installed before proceeding with installing this library.

#### Linux

Should install all of the necessary packages through your package manager.

### Plans:

- Will keep the main screen available, but the things shown will change. [ ]
- Will display a refresh icon OR will allow for refresh via keybind. [ ]
- If there is an error, will either show a red screen displaying the exception OR will crash the program. [ ]
- Refresh icon will fade after refresh [ x ]
- Runs when a file is changed in all packages in a folder [ ]
- Fast [ ]

### TODO
- Learn how to inject a new dynamic library into a currently running program
- Learn how to run separate sprite code in a currently running pygame game without having to edit the main code
    