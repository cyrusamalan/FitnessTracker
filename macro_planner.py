from datetime import date
import configparser
import psycopg2
import food

def create_planner_table():
    try:
        conn = psycopg2.connect(
            dbname="postgres",
            user="postgres",
            password="Cyrus!234",
            host="localhost",
            port="5432"
        )
        cursor = conn.cursor()

        #Create table query
        planner = f'''CREATE TABLE IF NOT EXISTS planner.{configparser.formatted_date} (
                        id SERIAL PRIMARY KEY,
                        user_id INT,
                        food_id TEXT,
                        food_name TEXT,
                        calories REAL,
                        fat REAL,
                        carbs REAL,
                        protein REAL,
                        servings REAL,
                        type TEXT,
                        CONSTRAINT fk_food
                          FOREIGN KEY(food_id)
                          REFERENCES public.food_data(food_id),
                        CONSTRAINT fk_user
                          FOREIGN KEY(user_id)
                          REFERENCES planner.users(user_id)
                        );'''
        cursor.execute(planner)
        conn.commit()
        print("Macro planner table created successfully.")
    except Exception as e:
        print(f"Error creating planner table: {e}")
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

def insert_in_planner(user_id):
    food_id = str(input("Insert food ID: "))
    meal_type = str(input("Breakfast/Lunch/Dinner(b,l,d): "))
    servings = float(input("Serving Size: "))
    if meal_type == 'b':
        meal_type = "breakfast"
    if meal_type == "l":
        meal_type = "lunch"
    if meal_type == "d":
        meal_type = "dinner"
    else:
        ValueError("Invalid meal type. Please enter 'b', 'l', or 'd'.")
    try:
        conn = psycopg2.connect(
            dbname="postgres",
            user="postgres",
            password="Cyrus!234",
            host="localhost",
            port="5432"
        )
        cursor = conn.cursor()

        planner_table_name = f"planner.{configparser.formatted_date}"

        # Perform the SELECT query
        select_query = '''SELECT food_id, food_name, calories, fat, carbs, protein
                          FROM food_data WHERE food_id = %s;'''
        cursor.execute(select_query, (food_id,))
        row = cursor.fetchone()

        if row:
            print("Selected Data:", row)
            # Extract the data
            food_id, food_name, calories, fat, carbs, protein = row
            user_id = configparser.user_id
            # Perform the INSERT query
            insert_query = f'''INSERT INTO planner.{configparser.formatted_date} 
                               (user_id, food_id, food_name, calories, fat, carbs, protein, servings, type)
                               VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
                               ;'''
            cursor.execute(insert_query, (configparser.user_id, food_id, food_name, calories, fat, carbs, protein, servings, meal_type))
            conn.commit()
            print("Data inserted successfully into the planner table.")
        else:
            print("No data found for the given food ID.")

    except Exception as e:
        print(f"Error inserting data: {e}")
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close() 


