"""All the functions that make the script work"""
# Standard imports
import json
import os
import sys
from datetime import datetime, timedelta
from os.path import exists
from random import choice
from typing import Tuple

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


def choose_recipes(eligible_recipes: dict, runner_ups: dict, all_recipes: dict) -> dict:
    """
    function to randomly choose from eligible_recipes, if eligible_recipes
    doesn't contain enough items, it will use runner_ups to fill the remaining recipes
    """
    recipes = []
    chosen_recipes = {}
    # populate recipes list with all possible recipes
    for recipe in eligible_recipes:
        recipes.append(recipe)
    # see if recipes has at least 7 recipes
    if len(recipes) < 7:
        for recipe in runner_ups:
            recipes.append(recipe)

    # choose 7 random recipes from the vetted recipes list
    for i in range(7):
        # choose a recipe
        recipe = choice(recipes)

        # set the chose_recipes dictionary to the recipe information
        chosen_recipes[recipe] = all_recipes[recipe]

        # remove the selected recipe from the list to prevent duplicate recipes
        recipes.pop(recipes.index(recipe))
    # return the chosen recipes
    return chosen_recipes


def combine_ingredients(recipes: dict) -> dict:
    """
    function to combine the ingredients for the provided recipes
    """
    grocery_list = {
        "meat": [],
        "dairy": [],
        "seasoning": [],
        "produce": [],
        "misc": []
    }
    for recipe in recipes:
        for ingredient in recipes[recipe]["ingredients"]:
            for item in recipes[recipe]["ingredients"][ingredient]:
                grocery_list[ingredient].append(item)
    return grocery_list
