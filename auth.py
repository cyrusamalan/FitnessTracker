import configparser
import psycopg2
import bcrypt


def create_user_table():
    try:
        conn = psycopg2.connect(
            dbname="postgres",
            user="postgres",
            password="Cyrus!234",
            host="localhost",
            port="5432"
        )
        cursor = conn.cursor()
        user_table = '''
        CREATE TABLE IF NOT EXISTS planner.users (
            user_id SERIAL PRIMARY KEY,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
        '''
        cursor.execute(user_table)
        conn.commit()
        print("User table created successfully.")
    except Exception as e:
        print(f"Error creating user table: {e}")
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()



def register_user(username, password, email):
    try:
        conn = psycopg2.connect(
            dbname="postgres",
            user="postgres",
            password="Cyrus!234",
            host="localhost",
            port="5432"
        )
        cursor = conn.cursor()
        
        # Hash the password
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
        print(f"Hashed Password: {hashed_password}")
        
        # Insert the user into the database
        insert_user = '''
        INSERT INTO planner.users (username, password, email) VALUES (%s, %s, %s);
        '''
        cursor.execute(insert_user, (username, hashed_password.decode('utf-8'), email))
        conn.commit()
        
        print("User registered successfully.")
        login = str(input("Username: "))
        password = str(input("Password: "))
        # Example usage
        user_id = login_user(login, password)
    except Exception as e:
        print(f"Error registering user: {e}")
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

def login_user(username, password):
    try:
        conn = psycopg2.connect(
            dbname="postgres",
            user="postgres",
            password="Cyrus!234",
            host="localhost",
            port="5432"
        )
        cursor = conn.cursor()
        
        # Fetch the user from the database
        select_user = '''
        SELECT user_id, password FROM planner.users WHERE username = %s;
        '''
        cursor.execute(select_user, (username,))
        user = cursor.fetchone()
        
        # Print the fetched user data for debugging
        #print(f"Fetched User: {user}")
        
        # Check if the user exists and if the passwords match
        if user:
            stored_password = user[1]
            #print(f"Stored Password: {stored_password}")
            if bcrypt.checkpw(password.encode('utf-8'), stored_password.encode('utf-8')):
                print("Login successful.")
                configparser.var = 1
                configparser.user_id = user[0]
                return user[0]  # Return user_id
            else:
                print("Password mismatch.")
                return None
        else:
            print("User not found.")
            return None
    except Exception as e:
        print(f"Error logging in: {e}")
        return None
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()


def account_info():
    if configparser.account == "n":
        # Prompt user to create a username and password
        register_username = str(input("Create a Username: "))
        register_password = str(input("Create a Password: "))
        reenter_password = str(input("Re-enter Password: "))

        enter_email = " "
        # Check if the re-entered password matches the original password
        if reenter_password != register_password:
            print("Passwords do not match. Please try again.")
            register_password = str(input("Create a Password: "))
            reenter_password = str(input("Re-enter Password: "))
        else:
            # If passwords match, prompt for email and confirm registration
            enter_email = str(input("Enter Email: "))
            print("Account successfully registered.")

        if enter_email == " ":
            enter_email = str(input("Enter Email: "))
        # Example usage
        register_user(register_username, register_password, enter_email)
    else:
        login = str(input("Username: "))
        password = str(input("Password: "))
        # Example usage
        user_id = login_user(login, password)

