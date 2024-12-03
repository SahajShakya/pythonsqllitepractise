import sqlite3

#Step 1: Initialize the database
def get_connection(db_name):
    try:
        return sqlite3.connect(db_name)
    except Exception as e:
        print('Error in connection', e)
        raise

#Step 2: Create a table in database
def create_table(connection):
    query = """
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY,
                name TEXT NOT NULL,
                age INTEGER,
                email TEXT UNIQUE
            )
            """
    try:
        with connection:
            connection.execute(query)
        print('Table was created successfully')
    except Exception as e:
        print('Error in creating table', e)
        raise

#Step 3: Insert User to the database
def insert_user(connection, name:str, age:int, email:str):
    query = """
            INSERT INTO users (name, age, email)
                VALUES (?, ?, ?)
                """
    try:
        with connection:
            connection.execute(query, (name, age, email))
        print('User was inserted successfully')
    except Exception as e:
        print('Error in inserting user', e)
        raise

#Step 4: Query all the users in database
def fetch_users(connection, condition:str = None) -> list[tuple]:
    query = """
    SELECT * FROM users
    """
    if condition:
        query += f"WHERE {condition}"
    try:
        with connection:
            rows = connection.execute(query).fetchall()
        return rows
    except Exception as e:
        print("Error during fetching", e)

#Step 5: Delete a User in Database
def delete_user(connection, user_id:int):
    query = """
    DELETE FROM users where id = ?
    """
    try:
        with connection:
            connection.execute(query, (user_id,))
        print("User was deleted")
    except Exception as e:
        print("User deletion failed", e)

#Step 6: Update a User in Database
def update_user(connection, user_id:int, email: str) -> list[tuple]:
    query = """
        UPDATE users SET email = ? WHERE id = ?
    """
    try:
        with connection:
            connection.execute(query, (email, user_id,))
        print(f"User ID {user_id} has new email of {email}")
    except Exception as e:
        print("Fail to update user", e)

#Step 7: Fetch user by user_id
def fetch_user(connection, user_id: int) -> list[tuple]:
    query= """
        SELECT * FROM users
    """
    if user_id:
        query += "WHERE id = ?"

        try:
            with connection:
                row = connection.execute(query, (user_id,)).fetchall()
            return row
        except Exception as e:
            print("Failed to fetch the user")

#Step 8: Ability add multiple users to the database
def insert_users(connection, users: list[tuple[str, int, str]]):
    if not users:
        print("No users to add.")
        return

    query = """
    INSERT INTO users (name, age, email)
        VALUES (?,?,?)
    """
    try:
        with connection:
            connection.executemany(query, users)
        print(f"{len(users)} user(s) were added to the database")
    except Exception as e:
        print("Failed to insert the user", e)

#Main Wrapper Function
def main():
    connection = get_connection('data.db')
    if connection:
        print('Connection Established')
    try:
        #create database
        create_table(connection)
        while True:
            start = input('Enter Option (Add, Delete, Update, SearchId ,Search All, Add Many, Exit): ').lower()
            if (start == 'add'):
                name = input('Enter Name: ')
                age = int(input('Enter Age: '))
                email = input('Enter Email: ')
                insert_user(connection, name, age, email)
            elif start == 'searchall':
                print("All Users:")
                for user in fetch_users(connection):
                    print(user)
            elif start == 'delete':
                user_id = int(input("Enter the user id you want to delete: "))
                delete_user(connection, user_id)
            elif start == 'searchid':
                user_id = int(input("Enter the user id you want to fetch: "))
                data = fetch_user(connection, user_id)
                print (f"User {user_id} ")
                print(data)
            elif start == 'update':
                user_id = int(input("Enter the user id you want to update: "))
                email = input("Enter the new email: ")
                update_user(connection, user_id, email)
            elif start == 'add many':
                users = []
                while True:
                    # Collect user information
                    name = input("Enter user's name: ")
                    age = int(input("Enter user's age: "))
                    email = input("Enter user's email: ")

                    # Add the new user as a tuple to the list
                    users.append((name, age, email))

                    # Ask if the user wants to add more
                    more = input("Do you want to add another user? (y/n): ").strip().lower()
                    if more != 'y':
                        break
                # Now insert the collected users into the database
                insert_users(connection, users)
            elif start == 'exit':
                break
            else:
                print('Invalid Option')
    finally:
        connection.close()

if __name__ == '__main__':
    main()