# db_connection.py
import mysql.connector

def get_db_connection():
    try:
        connection = mysql.connector.connect(
            host="127.0.0.1",
            user="root",       # Your MySQL username
            password="12345",  # Your MySQL password
            database="library_db"   # Your database name
        )
        if connection.is_connected():
            print("Connected to MySQL database")
            return connection
        else:
            print("Connection to MySQL database failed")
            return None
    except mysql.connector.Error as e:
        print(f"Error connecting to MySQL: {e}")
        return None

if __name__ == '__main__':
    conn = get_db_connection()
    if conn:
        conn.close()