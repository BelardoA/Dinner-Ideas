import json
import sys
import os
from os.path import exists

from rich.console import Console

console = Console()


def load_json(file_path: str, file_name: str) -> dict:
    """
    function to load a json and return it as a dictionary
    """
    data = {}
    if exists(file_path):
        try:
            with open(f"{file_path}/{file_name}.json", "r") as file:
                data = json.load(file)
        except FileNotFoundError as err:
            console.print(f"[red] ERROR: Unable to locate {file_name}.{file_path}.json!", err)
            sys.exit(1)
    else:
        console.print(f"[red] ERROR: File path doesn't exist!")
        sys.exit(1)
    return data


def save_json(file_path: str, file_name: str, data: dict) -> None:
    """
    function to save a json file, if the directory
    doesn't exist it will be created
    """
    if not exists(file_path):
        os.mkdir(file_path)
    with open(f"{file_path}/{file_name}.json") as out:
        json.dump(data, out, indent=4)
