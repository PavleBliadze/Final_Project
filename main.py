import json

class Ingredient:
    def __init__(self, name, quantity):
        self.name = name
        self.quantity = quantity

    def display_ingredient(self):
        return f"{self.quantity} of {self.name}"

    def __str__(self):
        return self.display_ingredient()

class Recipe:
    def __init__(self, name, country, ingredients=None, instructions=''):
        if ingredients is None:
            ingredients = []
        self.name = name
        self.country = country
        self.ingredients = ingredients
        self.instructions = instructions

    def update_recipe(self, name=None, country=None, ingredients=None, instructions=None):
        if name:
            self.name = name
        if country:
            self.country = country
        if ingredients is not None:
            self.ingredients = ingredients
        if instructions:
            self.instructions = instructions

    def display_recipe(self):
        ingredients_list = "\n".join([str(ingredient) for ingredient in self.ingredients])
        return (f"Ingredients:\n{ingredients_list}\n"
                f"Instructions: {self.instructions}")

    def __str__(self):
        return f"{self.name} ({self.country})"

class Country:
    def __init__(self, name):
        self.name = name
        self.dishes = []

    def add_dish(self, recipe):
        self.dishes.append(recipe)

    def remove_dish(self, recipe):
        self.dishes.remove(recipe)

    def get_dish(self, dish_name):
        for dish in self.dishes:
            if dish.name == dish_name:
                return dish
        return None

    def display_dishes(self):
        return [dish.name for dish in self.dishes]

class RecipeManager:
    def __init__(self):
        self.recipes = []
        self.countries = {}

    def add_recipe(self, recipe):
        self.recipes.append(recipe)
        if recipe.country not in self.countries:
            self.countries[recipe.country] = Country(recipe.country)
        self.countries[recipe.country].add_dish(recipe)

    def update_recipe(self, name, country, new_name=None, new_country=None, new_ingredients=None, new_instructions=None):
        try:
            recipe = self.view_recipe(country, name)
            if recipe:
                old_country = recipe.country
                if new_name:
                    recipe.name = new_name
                if new_country and old_country != new_country:
                    self.countries[old_country].remove_dish(recipe)
                    if new_country not in self.countries:
                        self.countries[new_country] = Country(new_country)
                    self.countries[new_country].add_dish(recipe)
                    recipe.country = new_country
                if new_ingredients is not None:
                    recipe.ingredients = new_ingredients
                if new_instructions:
                    recipe.instructions = new_instructions
                return recipe
        except Exception as e:
            print(f"Error updating recipe: {e}")
        return None

    def delete_recipe(self, name, country):
        try:
            recipe = self.view_recipe(country, name)
            if recipe:
                self.recipes.remove(recipe)
                self.countries[recipe.country].remove_dish(recipe)
                if not self.countries[recipe.country].dishes:
                    del self.countries[recipe.country]
                return recipe
        except Exception as e:
            print(f"Error deleting recipe: {e}")
        return None

    def view_recipe(self, country_name, dish_name):
        try:
            if country_name in self.countries:
                return self.countries[country_name].get_dish(dish_name)
        except Exception as e:
            print(f"Error viewing recipe: {e}")
        return None

    def save_to_file(self, filename):
        data = [
            {
                "name": recipe.name,
                "country": recipe.country,
                "ingredients": [{"name": ing.name, "quantity": ing.quantity} for ing in recipe.ingredients],
                "instructions": recipe.instructions
            }
            for recipe in self.recipes
        ]
        try:
            with open(filename, 'w') as file:
                json.dump(data, file, indent=4)
        except Exception as e:
            print(f"Error saving to file: {e}")

    def load_from_file(self, filename):
        try:
            with open(filename, 'r') as file:
                data = json.load(file)
                self.recipes = []
                self.countries = {}
                for item in data:
                    ingredients = [Ingredient(ing["name"], ing["quantity"]) for ing in item["ingredients"]]
                    recipe = Recipe(item["name"], item["country"], ingredients, item["instructions"])
                    self.add_recipe(recipe)
        except FileNotFoundError:
            self.load_default_recipes()
        except Exception as e:
            print(f"Error loading from file: {e}")

    def load_default_recipes(self):
       default_recipes = [
        Recipe("Khachapuri", "Georgian", [Ingredient("Flour", "500g"), Ingredient("Cheese", "300g"), Ingredient("Egg", "1")], "Mix flour, cheese, and egg together. Knead the dough and let it rest. Shape the dough into a round shape and fill with cheese. Bake until golden brown."),
        Recipe("Khinkali", "Georgian", [Ingredient("Flour", "300g"), Ingredient("Meat", "200g"), Ingredient("Onion", "1")], "Mix flour, meat, and onion together. Knead the dough and let it rest. Shape the dough into dumplings and boil them."),
        Recipe("Tacos", "Mexican", [Ingredient("Tortilla", "4"), Ingredient("Chicken", "200g"), Ingredient("Cheese", "100g")], "Fill tortillas with chicken and cheese."),
        Recipe("Enchiladas", "Mexican", [Ingredient("Tortilla", "6"), Ingredient("Beef", "300g"), Ingredient("Tomato", "400g")], "Fill tortillas with beef and tomato sauce. Top with cheese and bake."),
        Recipe("Sushi", "Japanese", [Ingredient("Rice", "200g"), Ingredient("Fish", "200g"), Ingredient("Seaweed", "3 sheets")], "Roll the rice and fish in seaweed."),
        Recipe("Ramen", "Japanese", [Ingredient("Noodles", "200g"), Ingredient("Broth", "1L"), Ingredient("Pork", "100g")], "Cook noodles in broth. Top with pork and other desired toppings.")
      ]
       for recipe in default_recipes:
        self.add_recipe(recipe)

def print_menu():
    print("1. Add Dishes")
    print("2. View Dishes")
    print("3. Update Dishes")
    print("4. Delete Dishes")
    print("5. Save and Exit")

def add_recipe(manager):
    try:
        country_names = list(manager.countries.keys())
        for i, country_name in enumerate(country_names, 1):
            print(f"{i}. {country_name} Dishes")
        print(f"{len(country_names) + 1}. Add a new country")

        while True:
            country_choice = input("Enter the number of the country: ")
            if country_choice.isdigit() and 1 <= int(country_choice) <= len(country_names) + 1:
                if int(country_choice) == len(country_names) + 1:
                    country = input("Enter new country name: ")
                else:
                    country = country_names[int(country_choice) - 1]
                break
            else:
                print("Please enter a valid number.")

        name = input("Enter dish name: ")
        ingredients = []
        while True:
            ing_name = input("Enter ingredient name (or 'done' to finish): ")
            if ing_name.lower() == 'done':
                break
            ing_quantity = input("Enter ingredient quantity: ")
            ingredients.append(Ingredient(ing_name, ing_quantity))
        instructions = input("Enter instructions: ")
        recipe = Recipe(name, country, ingredients, instructions)
        manager.add_recipe(recipe)
        print("Dish added successfully!")
    except Exception as e:
        print(f"Error adding recipe: {e}")

def select_country(manager):
    try:
        if not manager.countries:
            print("No countries available.")
            return None

        country_names = list(manager.countries.keys())
        for i, country_name in enumerate(country_names, 1):
            print(f"{i}. {country_name} Dishes")

        while True:
            country_choice = input("Enter the number of the country: ")
            if country_choice.isdigit() and 1 <= int(country_choice) <= len(country_names):
                return country_names[int(country_choice) - 1]
            else:
                print("Please enter a valid number.")
    except Exception as e:
        print(f"Error selecting country: {e}")
        return None

def select_dish(manager, country_name):
    try:
        if country_name in manager.countries:
            print(f"{country_name} Dishes:")
            dish_names = manager.countries[country_name].display_dishes()
            for i, dish_name in enumerate(dish_names, 1):
                print(f"{i}. {dish_name}")

            while True:
                dish_choice = input("Enter the number of the dish: ")
                if dish_choice.isdigit() and 1 <= int(dish_choice) <= len(dish_names):
                    return dish_names[int(dish_choice) - 1]
                else:
                    print("Please enter a valid number.")
        else:
            print("Country not found.")
            return None
    except Exception as e:
        print(f"Error selecting dish: {e}")
        return None

def view_recipe(manager):
    try:
        country_name = select_country(manager)
        if country_name:
            dish_name = select_dish(manager, country_name)
            if dish_name:
                recipe = manager.view_recipe(country_name, dish_name)
                if recipe:
                    print(recipe.display_recipe())
                else:
                    print("Dish not found!")
    except Exception as e:
        print(f"Error viewing recipe: {e}")

def update_recipe(manager):
    try:
        country_name = select_country(manager)
        if country_name:
            dish_name = select_dish(manager, country_name)
            if dish_name:
                new_ingredients = []
                while True:
                    ing_name = input("Enter new ingredient name (or 'done' to finish): ")
                    if ing_name.lower() == 'done':
                        break
                    ing_quantity = input("Enter ingredient quantity: ")
                    new_ingredients.append(Ingredient(ing_name, ing_quantity))
                new_instructions = input("Enter new instructions: ")
                updated_recipe = manager.update_recipe(dish_name, country_name, new_ingredients=new_ingredients, new_instructions=new_instructions)
                if updated_recipe:
                    print("Dish updated successfully!")
                else:
                    print("Dish not found!")
    except Exception as e:
        print(f"Error updating recipe: {e}")

def delete_recipe(manager):
    try:
        country_name = select_country(manager)
        if country_name:
            dish_name = select_dish(manager, country_name)
            if dish_name:
                deleted_recipe = manager.delete_recipe(dish_name, country_name)
                if deleted_recipe:
                    print("Dish deleted successfully!")
                else:
                    print("Dish not found!")
    except Exception as e:
        print(f"Error deleting recipe: {e}")

def main():
    manager = RecipeManager()
    try:
        manager.load_from_file("recipes.json")
    except Exception as e:
        print(f"Error loading recipes from file: {e}")

    while True:
        print_menu()
        choice = input("Enter your choice: ")
        if choice == '1':
            add_recipe(manager)
        elif choice == '2':
            view_recipe(manager)
        elif choice == '3':
            update_recipe(manager)
        elif choice == '4':
            delete_recipe(manager)
        elif choice == '5':
            try:
                manager.save_to_file("recipes.json")
                print("Dishes saved! Exiting...")
                break
            except Exception as e:
                print(f"Error saving recipes to file: {e}")
        else:
            print("Invalid choice! Please try again.")

if __name__ == "__main__":
    main()
