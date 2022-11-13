from random import choice
import json
from rich.console import Console
dinner_ideas =

console = Console()


def load_json(file_path: str) -> dict:
    """
    function to load a json and return it as a dictionary
    """
    try:
        with open(file_path, "r") as file:
    except FileNotFoundError:
        console.print()
