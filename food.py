from fatsecret import Fatsecret
from openai import OpenAI
import configparser
import psycopg2
import re
import food_ai

# Function to create the recipe table
def create_recipe_table():
    try:
        conn = psycopg2.connect(
            dbname="postgres",
            user="postgres",
            password="Cyrus!234",
            host="localhost",
            port="5432"
        )
        cursor = conn.cursor()
        # Create table query
        recipe_data = '''CREATE TABLE IF NOT EXISTS recipe_data (
                      recipe_id TEXT PRIMARY KEY,
                      recipe_name TEXT,
                      recipe_description TEXT,
                      recipe_url TEXT
                      );'''
        cursor.execute(recipe_data)
        conn.commit()
        print("Recipe table created successfully.")
    except Exception as e:
        print(f"Error creating table: {e}")
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

def create_recipe_nutrition_table():
    try:
        conn = psycopg2.connect(
            dbname="postgres",
            user="postgres",
            password="Cyrus!234",
            host="localhost",
            port="5432"
        )
        cursor = conn.cursor()
        # Create table query
        recipe_nutrition = '''CREATE TABLE IF NOT EXISTS recipe_nutrition (
                           recipe_id TEXT PRIMARY KEY,
                           calories REAL,
                           carbs REAL,
                           fat REAL,
                           protein REAL,
                           CONSTRAINT fk_recipe
                             FOREIGN KEY(recipe_id) 
                             REFERENCES recipe_data(recipe_id)
                           );'''
        cursor.execute(recipe_nutrition)
        conn.commit()
        print("Recipe_nutrition table created successfully.")
    except Exception as e:
        print(f"Error creating table: {e}")
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

# Function to create the food table
def create_food_table():
    try:
        # Connect to PostgreSQL database
        conn = psycopg2.connect(
            dbname="postgres",
            user="postgres",
            password="Cyrus!234",
            host="localhost",
            port="5432"
        )
        cursor = conn.cursor()
        # Create table query
        food_data = '''CREATE TABLE IF NOT EXISTS food_data (
                    food_id TEXT PRIMARY KEY,
                    calories REAL,
                    fat REAL,
                    carbs REAL,
                    protein REAL,
                    food_name TEXT,
                    generic TEXT,
                    food_url TEXT
                );'''
        cursor.execute(food_data)
        conn.commit()
        print("Food table created successfully.")
    except Exception as e:
        print(f"Error creating table: {e}")
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

# Function to parse nutritional values from the description
def parse_nutritional_values(description):
    nutrition = {'calories': None, 'fat': None, 'carbs': None, 'protein': None}
    try:
        calories = re.search(r'Calories: (\d+)kcal', description)
        if calories:
            nutrition['calories'] = float(calories.group(1))
        
        fat = re.search(r'Fat: ([\d\.]+)g', description)
        if fat:
            nutrition['fat'] = float(fat.group(1))

        carbs = re.search(r'Carbs: ([\d\.]+)g', description)
        if carbs:
            nutrition['carbs'] = float(carbs.group(1))

        protein = re.search(r'Protein: ([\d\.]+)g', description)
        if protein:
            nutrition['protein'] = float(protein.group(1))
    except Exception as e:
        print(f"Error parsing nutritional values: {e}")
    return nutrition

# Function to insert data into PostgreSQL
def insert_food_data(food_data):
    try:
        # Connect to PostgreSQL database
        conn = psycopg2.connect(
            dbname="postgres",
            user="postgres",
            password="Cyrus!234",
            host="localhost",
            port="5432"
        )
        cursor = conn.cursor()
        # Iterate over each food item
        for food in food_data:
            food_id = food['food_id']
            food_name = food['food_name']
            food_type = food['food_type']
            food_url = food['food_url']

            # Parse nutritional values from description
            nutrition = parse_nutritional_values(food.get('food_description', ''))

            cursor.execute('''
                INSERT INTO food_data (food_id, calories, fat, carbs, protein, food_name, generic, food_url)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                ON CONFLICT (food_id) DO NOTHING;
            ''', (
                food_id,
                nutrition['calories'],
                nutrition['fat'],
                nutrition['carbs'],
                nutrition['protein'],
                food_name,
                food_type,
                food_url
            ))
        food_ai.openai(food_name)
   
        
        conn.commit()
        print("Data inserted successfully.")
    except Exception as e:
        print(f"Error inserting data: {e}")
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

def insert_recipe_data(recipe_data):
    try:
        # Connect to PostgreSQL database
        conn = psycopg2.connect(
            dbname="postgres",
            user="postgres",
            password="Cyrus!234",
            host="localhost",
            port="5432"
        )
        cursor = conn.cursor()
        for data in recipe_data:
            recipe_id = data['recipe_id']
            recipe_name = data['recipe_name']
            recipe_description = data.get('recipe_description', '')
            recipe_url = data['recipe_url']
            

            cursor.execute('''
                INSERT INTO recipe_data (recipe_id, recipe_name, recipe_description, recipe_url)
                VALUES (%s, %s, %s, %s)
                ON CONFLICT(recipe_id) DO NOTHING;
            ''', (
                recipe_id,
                recipe_name,
                recipe_description,
                recipe_url
            ))
        conn.commit()
        print("Recipe Data inserted successfully.")
    except Exception as e:
        print(f"Error inserting data: {e}")
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

def insert_recipe_nutrition(food_data):
    try:
        # Connect to PostgreSQL database
        conn = psycopg2.connect(
            dbname="postgres",
            user="postgres",
            password="Cyrus!234",
            host="localhost",
            port="5432"
        )
        cursor = conn.cursor()
        # Iterate over each food item
        for recipe in food_data:
            recipe_id = recipe['recipe_id']
            recipe_nutrition = recipe['recipe_nutrition']
            calories = float(recipe_nutrition.get('calories', 0))
            carbs = float(recipe_nutrition.get('carbohydrate', 0))
            fat = float(recipe_nutrition.get('fat', 0))
            protein = float(recipe_nutrition.get('protein', 0))
          

            cursor.execute('''
                INSERT INTO recipe_nutrition (recipe_id, calories, carbs, fat, protein)
                VALUES (%s, %s, %s, %s, %s)
                ON CONFLICT (recipe_id) DO NOTHING;
            ''', (
                recipe_id,
                calories,
                carbs,
                fat,
                protein,
            ))
        conn.commit()
        print("Recipe Nutrition Data inserted successfully.")
    except Exception as e:
        print(f"Error inserting data: {e}")
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

def select_food():
    try:
        conn = psycopg2.connect(
        dbname="postgres",
        user="postgres",
        password="Cyrus!234",
        host="localhost",
        port="5432"
        )
        cursor = conn.cursor()
        query = '''SELECT food_id, food_name, calories FROM food_data 
                   WHERE food_name ILIKE %s;'''
        cursor.execute(query, (f"%{configparser.food_item}%",))
        print(configparser.food_item)
        # Fetch and print the results
        rows = cursor.fetchall()
        print(" ID  |            NAME                  |   Calories")
        print("-------------------------------------------------------------------")
        for row in rows:
            print(row)
    except Exception as e:
        print(f"Error creating table: {e}")
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()
'''print("Recipe Search Results:")
print("{}\n".format(recipes))

for recipe in recipes:
    print(recipe)

print("Food Search Results: {}".format(len(food_item)))
print("{}\n".format(foods))'''
