import requests
from collections import Counter

from secrets import APP_ID, APP_KEY

BASE_URL = 'https://api.edamam.com/api/recipes/v2?type=public'

def call_edamam_api(query_food: str, health_trend: str, calorie_amount: int) -> list:
    url = f"{BASE_URL}&q={query_food}&app_id={APP_ID}&app_key={APP_KEY}"
    response = requests.get(url)
    recipes = response.json()['hits']
    
    valid_recipes = []
    
    for (item, recipe) in enumerate(recipes):
        recipe = recipe['recipe']
        recipe_name = recipe['label']
        health_labels = recipe['healthLabels']
        calories = recipe['calories']
        
        if ((health_trend in health_labels) and (calories < calorie_amount)):
            health_labels.remove(health_trend)
            valid_recipe = {
                "item_number": item,
                "name": recipe_name,
                "other_health_labels": health_labels,
                "calories": calories
            }
            valid_recipes.append(valid_recipe)
    
    return valid_recipes

def recipe_search(food_query: str, health_label_query: list) -> int:
    url = f"{BASE_URL}&q={food_query}&app_id={APP_ID}&app_key={APP_KEY}"
    response = requests.get(url)
    data = response.json()['hits']
    
    valid_recipes = []

    # find recipes that include all lables in health label query list
    for item in data:
        recipe = item['recipe']
        health_labels = recipe['healthLabels']
        
        health_label_match = True

        for label in health_label_query:
            if label not in health_labels:
                health_label_match = False

        if health_label_match:
            valid_recipes.append(recipe)

    return len(valid_recipes)

def top_cal_recipe(recipes: list) -> dict:
    largest_cal_recipe = None
    largest_cal_num = 0
    
    for recipe in recipes:
        calories = recipe['calories']
        
        if (calories > largest_cal_num):
            largest_cal_num = calories
            largest_cal_recipe = recipe
    
    return largest_cal_recipe

def find_most_popular_health_label(recipes: list) -> str:
    all_health_labels = []
    
    # build list of all health labels in all recipes
    for recipe in recipes:
        health_labels = recipe['other_health_labels']
        for label in health_labels:
            all_health_labels.append(label)
    
    # find most common health label
    data = Counter(all_health_labels)
    return data.most_common(1)[0][0]

def main():
    #return the number of chicken recepies that are in the 'Mediterranean' food trend & under 5000 calories
    chicken_recipes = call_edamam_api(
        query_food="chicken",
        health_trend="Mediterranean",
        calorie_amount=5000
    )

    most_popular_health_label = find_most_popular_health_label(chicken_recipes)

    cilantro_recipes = recipe_search(
        food_query='cilantro',
        health_label_query=['Vegan', 'Gluten-Free']
    )

if __name__ == "__main__":
    main()
