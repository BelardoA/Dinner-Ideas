"""Python Script that will help you decide what to make for dinner for the week"""
# standard imports
# TODO: add save functionality for weekly recipes
# TODO: add option to get fast food x times a week for dinner

from modules.functions import console, load_json, save_json, evaluate_recipes, choose_recipes, combine_ingredients

if __name__ == "__main__":
    recipes = load_json(file_path="database", file_name="recipe_list")
    eligible_recipes, runner_ups = evaluate_recipes(recipes)
    menu = choose_recipes(eligible_recipes, runner_ups, recipes)
    ingredients = combine_ingredients(menu)
    console.print(menu.keys())
    console.print(ingredients)
