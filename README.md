# FitnessTracker
Created a fitness tracker that gives a brief description of certain foods and keeps track of food you are eating.

food.py
The food.py file is responsible for interacting with a database to store and retrieve information related to food items. It contains functions for connecting to a database, executing SQL queries, and handling exceptions. This file includes logic for inserting new food items into the database, selecting existing food items based on certain criteria, and updating or deleting records as needed.

food_ai.py
The food_ai.py file integrates AI functionalities, such as natural language processing or machine learning, with food-related data. It involves generating nutritional information based on food descriptions, providing dietary recommendations, and performing other AI-driven tasks. This file uses libraries like OpenAI to interact with language models and process user inputs or database records.

macro_planner.py
The macro_planner.py file focuses on planning and tracking macronutrients (carbs, fats, proteins) for different meals. It involves creating tables to store daily or weekly meal plans, inserting food items into these plans, and calculating the total nutritional intake for each meal or day. This file contains functions for creating, reading, updating, and deleting records in a database, as well as handling user inputs for planning meals.

main.py
The main.py file is the entry point of the application. It initializes the necessary modules, handles user inputs, and coordinates the interactions between different parts of the application. This file imports functions from food.py, food_ai.py, and macro_planner.py to provide a cohesive user experience. It includes a command-line interface or a web server to handle requests and responses.
