import scripts.create_cmake_file
import scripts.include_intellisense


def main() -> None:
    scripts.create_cmake_file.create_cmake_file()
    scripts.include_intellisense.include_intellisense()


if __name__ == "__main__":
    main()
