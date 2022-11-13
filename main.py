"""Python Script that will help you decide what to make for dinner for the week"""
# standard imports
# TODO: add cracked chicken

from modules.functions import console, load_json, save_json, evaluate_recipes, choose_recipes

if __name__ == "__main__":
    recipes = load_json(file_path="database", file_name="recipe_list")
    eligible_recipes, runner_ups = evaluate_recipes(recipes)
    menu = choose_recipes(eligible_recipes, runner_ups)
    console.print(menu)
