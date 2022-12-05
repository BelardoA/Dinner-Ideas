"""Python Script that will help you decide what to make for dinner for the week"""

# standard imports
import sys
from rich.pretty import pprint
from modules.functions import (
    console,
    load_json,
    evaluate_recipes,
    choose_recipes,
    replace_recipe,
    combine_ingredients,
    get_fast_food,
)

if __name__ == "__main__":
    # set the number of days we want recipes for
    RECIPE_DAYS = 7
    # ask the user if they want to get fast food for Friday
    answer: str = input("Fast food Friday?\nEnter Y/n\n")
    # evaluate the user import
    if answer[0].lower() == "y":
        # user wants fast food fridays, so take away a day from # of days for recipes
        RECIPE_DAYS -= 1
        # set fast food flag to true
        FAST_FOOD = True
    elif answer[0].lower() == "n":
        # set fast food flag to false
        FAST_FOOD = False
    else:
        # incorrect input from user
        console.print("[red]ERROR: Incorrect reply!")
        # exit application with an error
        sys.exit(1)

    # load the recipes from the json file
    recipes = load_json(file_path="database", file_name="recipe_list")
    # evaluate the recipes and save them in eligible_recipes and alternatives in runner_ups
    eligible_recipes, runner_ups = evaluate_recipes(recipes)
    # choose the recipes for the number of days and set up a menu
    menu = choose_recipes(eligible_recipes, runner_ups, recipes, RECIPE_DAYS)
    # combine all ingredients for the recipes
    ingredients = combine_ingredients(menu)
    # if the user wanted fast food, select one from fastfood_list.json
    if FAST_FOOD:
        # choose a fast food item from the fastfood_list
        fast_food_choice = get_fast_food()
        # add the selected fast food item to the menu
        menu.update({fast_food_choice: "fast food Friday!"})
    # menu verification
    while True:
        # print out the menu in the console
        console.rule("[bold red]Menu")
        pprint(list(menu.keys()))
        console.rule("[bold yellow] Confirm menu")
        answer: str = input("Y/n\n")
        if answer == "" or answer[0].lower() == "y":
            break
        answer: str = input("Select meal to replace\n")
        if answer == "":
            break
        else:
            new_item = replace_recipe(
                menu, eligible_recipes, runner_ups, recipes, answer
            )
            menu.pop(answer)
            menu.pop(fast_food_choice)
            menu[new_item.name] = new_item.dict()
            menu.update({fast_food_choice: "fast food Friday!"})
    # print out the ingredients needed for the recipes
    console.rule("[bold red]Ingredients")
    pprint(ingredients)
