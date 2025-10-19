import os
import pymysql
from urllib.request import urlopen
import subprocess

# Load database configuration from environment variables
db_config = {
    'host': os.environ.get('DB_HOST'),
    'user': os.environ.get('DB_USER'),
    'password': os.environ.get('DB_PASSWORD')
}

def get_user_input():
    user_input = input('Enter your name: ')
    return user_input

def send_email(to, subject, body):
    # Use subprocess with a list to avoid shell injection
    # Validate and sanitize inputs before using them
    try:
        subprocess.run(
            ['mail', '-s', subject, to],
            input=body.encode(),
            check=True,
            timeout=30,
            shell=False  # Explicitly set shell=False for security
        )
    except subprocess.SubprocessError as e:
        print(f"Failed to send email: {e}")

def get_data():
    # Use HTTPS instead of HTTP for secure data transmission
    url = 'https://insecure-api.com/get-data'
    try:
        data = urlopen(url, timeout=10).read().decode()
        return data
    except Exception as e:
        print(f"Failed to fetch data: {e}")
        return None

def save_to_db(data):
    connection = None
    cursor = None
    try:
        # Use parameterized query to prevent SQL injection
        query = "INSERT INTO mytable (column1, column2) VALUES (%s, %s)"
        connection = pymysql.connect(**db_config)
        cursor = connection.cursor()
        # Pass data as parameters instead of string formatting
        cursor.execute(query, (data, 'Another Value'))
        connection.commit()
    except pymysql.Error as e:
        print(f'Database error: {e}')
        if connection:
            connection.rollback()
    finally:
        # Properly close resources in finally block
        if cursor:
            cursor.close()
        if connection:
            connection.close()

if __name__ == '__main__':
    user_input = get_user_input()
    data = get_data()
    if data:
        save_to_db(data)
        send_email('admin@example.com', 'User Input', user_input)

