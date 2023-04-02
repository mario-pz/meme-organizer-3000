from datetime import datetime
from os import makedirs, path, rename
from shutil import move
from os import walk, listdir, rmdir
from calendar import monthrange
from typing import Tuple
from sys import argv


def get_use_cases() -> dict[str, Tuple[str, str]]:
    return {
        "jpg": ("images", "img"),
        "png": ("images", "img"),
        "jpeg": ("images", "img"),
        "pdf": ("documents", "doc"),
        "doc": ("documents", "doc"),
        "docx": ("documents", "doc"),
        "ppt": ("documents", "doc"),
        "pptx": ("documents", "doc"),
        "xls": ("documents", "doc"),
        "xlsx": ("documents", "doc"),
        "epub": ("documents", "doc"),
        "mp4": ("videos", "vid"),
        "mov": ("videos", "vid"),
        "zip": ("archives", "arc"),
        "rar": ("archives", "arc"),
        "7z": ("archives", "arc"),
        "tar": ("archives", "arc"),
        "gz": ("archives", "arc"),
        "mp3": ("music", "mus"),
        "wav": ("music", "mus"),
        "flac": ("music", "mus"),
        "txt": ("text", "txt"),
        "rtf": ("text", "txt"),
        "html": ("web", "web"),
        "css": ("web", "web"),
        "js": ("web", "web"),
        "json": ("data", "data"),
        "csv": ("data", "data"),
        "xml": ("data", "data"),
    }


def clean_empty_dirs(directory: str):
    for dir_name in listdir(directory):
        dir_path = path.join(directory, dir_name)
        if path.isdir(dir_path) and not listdir(dir_path):
            print(f"Deleting empty directory: {dir_path}")
            rmdir(dir_path)


def create_tree_structure(root: str) -> None:
    for year in range(2017, datetime.now().year + 1):
        for month in range(1, 13):
            _, days_in_month = monthrange(year, month)
            for day in range(1, days_in_month + 1):
                makedirs(
                    f"{root}/{year}/{month}/{day}/images",
                    exist_ok=True,
                )
                makedirs(
                    f"{root}/{year}/{month}/{day}/videos",
                    exist_ok=True,
                )
                makedirs(
                    f"{root}/{year}/{month}/{day}/documents",
                    exist_ok=True,
                )
                makedirs(
                    f"{root}/{year}/{month}/{day}/other",
                    exist_ok=True,
                )
                makedirs(
                    f"{root}/{year}/{month}/{day}/archives",
                    exist_ok=True,
                )
                makedirs(
                    f"{root}/{year}/{month}/{day}/web",
                    exist_ok=True,
                )
                makedirs(
                    f"{root}/{year}/{month}/{day}/data",
                    exist_ok=True,
                )

                makedirs(
                    f"{root}/{year}/{month}/{day}/music",
                    exist_ok=True,
                )

                makedirs(
                    f"{root}/{year}/{month}/{day}/text",
                    exist_ok=True,
                )


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
    tree_sert_file = path.join(root_directory, "tree-cert.txt")

    if not path.exists(tree_sert_file):
        create_tree_structure(root_directory)
        with open(tree_sert_file, "w") as f:
            f.write("File tree successfully generated.")
    else:
        print("Tree is already created, moving on to organizing")

    for root, _, files in walk(directory):
        if any(d.isdigit() and len(d) == 4 for d in root.split(path.sep)):
            continue  # Skip directories that are named as a year
        for file_name in files:
            file_path = path.join(root, file_name)
            if path.isfile(file_path) and file_name != path.basename(__file__):
                print(f"Moving {file_name} to {root_directory}")
                move_file_to_tree(file_path, root_directory)

    clean_empty_dirs(root_directory)


if __name__ == "__main__":
    if len(argv) > 2:
        main(argv[2])
    else:
        main(".")
