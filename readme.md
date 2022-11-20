## Dinner Ideas
 
Simple script that will tell you what to make for dinner for the week and will tell you the ingredients needed as well.


Simply run main.py and answer whether you want to have fast food for one day of the week.


### Prerequisites
- Install the dependencies with `pip install -r requiremens.txt`
- Populate `fastfood_list.json` with fast food options
  - Example format:
  ```
  {
    "fastfood": [
      "Chic-fil-A",
      "Pizza",
      "Chinese"]
  }
  ```
- Populate `recipe_list.json` with your recipes and ingredients needed for them
  - Example format:
  ```
  {
    "shrimp scampi": {
      "ingredients": {
        "meat": ["large shrimp"],
        "dairy": ["butter"],
        "seasoning": ["salt", "pepper", "garlic powder"],
        "produce": ["garlic", "parsley", "lemon"],
        "misc": ["olive oil", "dry white wine"]
      },
      "last_cooked": ""
    }
  }
  ```