from faker import Faker
import pymysql
from dotenv import load_dotenv
import os

load_dotenv()
fake = Faker()

def generate_users(num_users=100):
    connection = pymysql.connect(
        host=os.getenv('MYSQL_HOST'),
        user=os.getenv('MYSQL_USER'),
        password=os.getenv('MYSQL_PASSWORD'),
        database=os.getenv('MYSQL_DATABASE')
    )
    
    try:
        with connection.cursor() as cursor:
            for _ in range(num_users):
                user = {
                    'username': fake.user_name(),
                    'email': fake.email()
                }
                
                cursor.execute("""
                    INSERT INTO users (username, email)
                    VALUES (%(username)s, %(email)s)
                """, user)
            
            connection.commit()
            print(f"Generated {num_users} users")
    finally:
        connection.close()

if __name__ == "__main__":
    generate_users()