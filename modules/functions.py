"""All the functions that make the script work"""
# Standard imports
import collections
import json
import os
import sys
from datetime import datetime, timedelta
from os.path import exists
from random import choice
from typing import Tuple

from rich.console import Console

from models.recipe import Recipe
from models.ingredients import Ingredients

console = Console()
today = datetime.now()


def date_to_str(date: datetime, str_format="%m/%d/%Y") -> str:
    """
    function to convert a datetime object into a string
    """
    return date.strftime(str_format)


def str_to_date(date: str, str_format="%m/%d/%Y") -> datetime:
    """
    function to convert a string into a datetime object, if the date
    is blank, go back 12 days to make the recipe eligible
    """
    # see if the string provided isn't blank
    if date != "":
        date_format = datetime.strptime(date, str_format)
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
            with open(f"{file_path}/{file_name}.json", "r", encoding="utf-8") as file:
                # set data to the loaded json file
                data = json.load(file)
        except FileNotFoundError as err:
            # let the user know the json cannot be found and exit
            console.print(
                f"[red] ERROR: Unable to locate {file_name}.{file_path}.json!", err
            )
            sys.exit(1)
    else:
        # tell the user the directory doesn't exist and exit
        console.print(f"[red] ERROR: {file_path} doesn't exist!")
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
    with open(f"{file_path}/{file_name}.json", "w", encoding="utf-8") as out:
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


def choose_recipes(
    eligible_recipes: dict, runner_ups: dict, all_recipes: dict, days: int
) -> dict:
    """
    function to randomly choose from eligible_recipes, if eligible_recipes
    doesn't contain enough items, it will use runner_ups to fill the remaining recipes
    """
    recipes = []
    chosen_recipes = {}
    # populate recipes list with all possible recipes
    for recipe in eligible_recipes:
        recipes.append(recipe)
    # see if recipes has the # of requested recipes
    if len(recipes) < days:
        for recipe in runner_ups:
            recipes.append(recipe)

    # choose x days of random recipes from the vetted recipes list
    for _ in range(days):
        # choose a recipe
        recipe = choice(recipes)

        # set the chose_recipes dictionary to the recipe information
        chosen_recipes[recipe] = all_recipes[recipe]

        # remove the selected recipe from the list to prevent duplicate recipes
        recipes.pop(recipes.index(recipe))
    # return the chosen recipes
    return chosen_recipes



def replace_recipe(
    menu: dict, eligible_recipes: dict, runner_ups: dict, recipes: dict, item: str
) -> Recipe:
    """
    function to generate a new menu item that is NOT in the current menu
    """
    new_recipe = None
    if menu == eligible_recipes:
        new_recipe = choice(list(runner_ups))
    else:
        while True:
            new_recipe = choice(list(eligible_recipes))
            if new_recipe not in menu and new_recipe is not item:
                break
    return Recipe(
        new_recipe,
        Ingredients(
            [recipes[new_recipe]["ingredients"]], recipes[new_recipe]["last_cooked"]
        ),
    )


def remove_duplicates(dupe_list: list) -> list:
    """
    function to combine duplicates from the provided list
    and returns a count of the duplicate
    """
    # count the items in the provided list
    counted_list = collections.Counter(dupe_list)
    # create a list of the duplicate items
    clean_list = [[i] * j for i, j in counted_list.items()]
    # combine the # of duplicates with the item name
    for item in clean_list:
        index = clean_list.index(item)
        if len(item) > 1:
            clean_list[index] = f"{len(item)}x{item[0]}"
        else:
            clean_list[index] = item[0]
    return clean_list


def combine_ingredients(recipes: dict) -> dict:
    """
    function to combine the ingredients for the provided recipes
    """
    # set up dictionary for each ingredient category
    grocery_list = {"meat": [], "dairy": [], "seasoning": [], "produce": [], "misc": []}
    # iterate through the recipes
    for recipe in recipes:
        # iterate through the ingredients for the recipes
        for ingredient in recipes[recipe]["ingredients"]:
            # iterate through the individual items in the list of ingredients category
            for item in recipes[recipe]["ingredients"][ingredient]:
                # add the item to the grocery_list dictionary
                grocery_list[ingredient].append(item)
    # remove duplicates from the list
    clean_grocery_list = grocery_list
    for item, item_list in grocery_list.items():
        clean_grocery_list[item] = remove_duplicates(item_list)
    # return the grocery list of all the ingredients in the appropriate lists
    return clean_grocery_list


def get_fast_food() -> str:
    """
    function to select a random fast food item from
    the fastfood_list.json file and returns it
    """
    # load the fastfood_list.json file
    fast_food = load_json(file_path="database", file_name="fastfood_list")
    # select a random item from the list of fastfood options
    fast_food_choice = choice(fast_food["fastfood"])
    # return the selection as a string
    return fast_food_choice
