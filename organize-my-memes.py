from datetime import datetime
from os import makedirs, path, rename
from shutil import move
from os import walk, listdir, rmdir
from calendar import monthrange
from typing import Tuple
from sys import argv

from toml import load as tload


# Type Helpers
Config = dict[str, Tuple[str, str]]

# Helper functions


def get_config():
    with open("config.toml", "r") as file:
        return tload(file)


def get_use_cases() -> Config:
    return get_config()


def clean_empty_dirs(directory: str):
    for dir_name in listdir(directory):
        dir_path = path.join(directory, dir_name)
        if path.isdir(dir_path) and not listdir(dir_path):
            print(f"Deleting empty directory: {dir_path}")
            rmdir(dir_path)


def create_tree_structure(root: str, config: Config) -> None:
    starting_age: int = config["starting_age"]
    use_cases = config["use_cases"]
    print(use_cases)

    categories: set[str] = set(
        [case["type"] for cases in use_cases.values() for case in cases]
    )

    for year in range(starting_age, datetime.now().year + 1):
        for month in range(1, 13):
            _, days_in_month = monthrange(year, month)
            for day in range(1, days_in_month + 1):
                for category in categories:
                    directory_path = f"{root}/{year}/{month}/{day}/{category}"
                    makedirs(directory_path, exist_ok=True)


def move_file_to_tree(file_path: str, root: str) -> None:
    file_name = path.basename(file_path)
    file_ext = file_path.split(".")[-1]

    folder_map = get_use_cases()

    folder, prefix = folder_map.get(file_ext.lower(), ("other", "opt"))

    if not file_name.startswith(prefix + "-"):
        new_file_name = f"{prefix}-{file_name}"
        new_file_path = path.join(path.dirname(file_path), new_file_name)
        rename(file_path, new_file_path)
    else:
        new_file_path = file_path

    file_date = datetime.fromtimestamp(path.getmtime(new_file_path))

    target_path = (
        f"{root}/{file_date.year}/{file_date.month}/{file_date.day}/{folder}/"
    )
    move(new_file_path, target_path + path.basename(new_file_path))


def main(directory: str) -> None:
    root_directory = directory
    config: Config = get_config()
    tree_sert_file = path.join(root_directory, "tree-cert.txt")

    if not path.exists(tree_sert_file):
        create_tree_structure(root_directory, config)
        with open(tree_sert_file, "w") as f:
            f.write("File tree successfully generated.")
    else:
        print("Tree is already created, moving on to organizing")

    return
    for root, _, files in walk(directory):
        if any(d.isdigit() and len(d) == 4 for d in root.split(path.sep)):
            continue  # Skip directories that are named as a year
        for file_name in files:
            file_path = path.join(root, file_name)
            if (
                path.isfile(file_path)
                and file_name != "config.toml"
                and file_name != path.basename(__file__)
            ):
                print(f"Moving {file_name} to {root_directory}")
                move_file_to_tree(file_path, root_directory)

    clean_empty_dirs(root_directory)


if __name__ == "__main__":
    if len(argv) > 2:
        main(argv[2])
    else:
        main(".")
