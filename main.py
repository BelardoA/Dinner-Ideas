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
    answer: str = input("Fast food Friday?\nEnter Y/n: ")
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
        # get a list of menu items
        menu_list = {}
        menu_items = list(menu.keys())
        for item in menu_items:
            menu_list[menu_items.index(item)] = item
        # print out the menu in the console
        console.rule("[bold red]Menu")
        pprint(menu_list)
        console.rule("[bold yellow] Confirm menu")
        answer: str = input("\nWould you like to make any changes?\nEnter Y/n: ")
        if answer == "" or answer[0].lower() == "n":
            break
        # ask user which menu item they would like to replace
        answer: str = input("Enter menu number or item you'd like to replace: ")
        # check if answer is in the menu items, user can enter number or menu item
        if answer in menu_items:
            # answer was a string of menu item, replace that item
            new_item = replace_recipe(
                menu=menu,
                eligible_recipes=eligible_recipes,
                runner_ups=runner_ups,
                recipes=recipes,
                item=answer,
            )
        elif int(answer) < len(menu_items):
            # answer was # of menu item, replace that item
            answer = menu_items[int(answer)]
            new_item = replace_recipe(
                menu=menu,
                eligible_recipes=eligible_recipes,
                runner_ups=runner_ups,
                recipes=recipes,
                item=answer,
            )
        else:
            console.print("[red]ERROR: Invalid selection!")
            sys.exit(1)
        menu.pop(answer)
        menu[new_item.name] = new_item.dict()
    # print confirmed menu
    console.rule("[bold red]Menu")
    pprint(menu_list)
    # print out the ingredients needed for the recipes
    console.rule("[bold red]Ingredients")
    pprint(ingredients)
