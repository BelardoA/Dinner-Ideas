"""All the functions that make the script work"""
# Standard imports
import json
import sys
import os
from random import choice
from typing import Tuple
from os.path import exists
from datetime import datetime, timedelta

from rich.console import Console

console = Console()
today = datetime.now()


def date_to_str(date: datetime, format="%m/%d/%Y") -> str:
    """
    function to convert a datetime object into a string
    """
    return date.strftime(format)


def str_to_date(date: str, format="%m/%d/%Y") -> datetime:
    """
    function to convert a string into a datetime object, if the date
    is blank, go back 12 days to make the recipe eligible
    """
    # see if the string provided isn't blank
    if date != "":
        date_format = datetime.strptime(date, format)
    else:
        # use date of 12 days ago to make the recipe eligible
        date_format = today - timedelta(days=12)
    return date_format


def load_json(file_path: str, file_name: str) -> dict:
    """
    function to load a json and return it as a dictionary
    """
    # check if the file path exists
    if exists(file_path):
        try:
            # try to open the file
            with open(f"{file_path}/{file_name}.json", "r") as file:
                # set data to the loaded json file
                data = json.load(file)
        except FileNotFoundError as err:
            # let the user know the json cannot be found and exit
            console.print(f"[red] ERROR: Unable to locate {file_name}.{file_path}.json!", err)
            sys.exit(1)
    else:
        # tell the user the directory doesn't exist and exit
        console.print(f"[red] ERROR: File path doesn't exist!")
        sys.exit(1)
    # return loaded json file
    return data


def save_json(file_path: str, file_name: str, data: dict) -> None:
    """
    function to save a json file, if the directory
    doesn't exist it will be created
    """
    # create the directory if it doesn't exist
    if not exists(file_path):
        os.mkdir(file_path)
    with open(f"{file_path}/{file_name}.json") as out:
        # save the json file
        json.dump(data, out, indent=4)


def evaluate_recipes(recipes: dict) -> Tuple[dict, dict]:
    """
    function to generate and return a Tuple of dictionaries
    containing recipes from recipe_list.json
    """
    # create dictionary for eligible recipes, random_recipes and runner_ups
    eligible_recipes = {}
    # runner_ups will be used if the random_recipes < 7
    runner_ups = {}

    # get last week's date
    last_week = today - timedelta(days=7)

    # first get all recipes that weren't made last week
    # iterate through the recipes and see if they weren't cooked last week
    for recipe in recipes:
        # convert last_cooked string into a date
        last_cooked = str_to_date(recipes[recipe]["last_cooked"])

        # see if the recipe was cooked more than a week ago
        if last_cooked < last_week or last_cooked == "":
            # add the recipe to eligible_recipes
            eligible_recipes[recipe] = recipes[recipe]
        else:
            runner_ups[recipe] = recipes[recipe]
    # return the eligible_recipes and runner_ups
    return eligible_recipes, runner_ups


def choose_recipes(eligible_recipes: dict, runner_ups: dict) -> dict:
    """
    function to randomly choose from eligible_recipes, if eligible_recipes
    doesn't contain enough items, it will use runner_ups to fill the remaining recipes
    """
    recipes = []
    chosen_recipes = {}
    # populate recipes list with all possible recipes
    # see if eligible_recipes has 7 or more recipes
    if len(eligible_recipes) >= 7:
        for recipe in eligible_recipes:
            recipes.append(recipe)

    for i in range(7):
        recipe = choice(recipes)
        chosen_recipes[recipe] = eligible_recipes[recipe]
        recipes.pop(recipes.index(recipe))
    return chosen_recipes
