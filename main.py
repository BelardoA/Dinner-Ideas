from modules.functions import console, load_json, save_json

if __name__ == "__main__":
    recipes = load_json(file_path="database", file_name="recipe_list")
    console.print(recipes)
