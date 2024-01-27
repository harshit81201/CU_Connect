# db_access.py
import sqlite3

# Connect to the database
conn = sqlite3.connect('instance\site.db')
c = conn.cursor()

# Execute a query
c.execute("SELECT * FROM user")

# Fetch and print all rows from the query
print(c.fetchall())

# Close the connection
conn.close()


"""
# Function to delete a user by email
def delete_user_by_email(user_email):
    try:
        c.execute("DELETE FROM user WHERE email = ?", (user_email,))
        conn.commit()
        print(f"User with email {user_email} deleted successfully.")
    except sqlite3.Error as e:
        print("An error occurred:", e.args[0])
    finally:
        if conn:
            conn.close()

# Replace 'user_email@example.com' with the email of the user you want to delete
delete_user_by_email('user_email@example.com')"""