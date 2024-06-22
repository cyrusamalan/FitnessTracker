from fatsecret import Fatsecret

fs = Fatsecret('consumer key','consumer secret')


# Test Calls w/o authentication

print("\n\n ---- No Authentication Required ---- \n\n")

foods = fs.foods_search("Tacos")
print("Food Search Results: {}".format(len(foods)))
print("{}\n".format(foods))

food = fs.food_get("1345")
print("Food Item 1345")
print("{}\n".format(food))

recipes = fs.recipes_search("Tomato Soup")
print("Recipe Search Results:")
print("{}\n".format(recipes))

recipe = fs.recipe_get("88339")
print("Recipe 88339")
print("{}\n".format(recipe))