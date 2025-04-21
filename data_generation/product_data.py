from faker import Faker
import pymysql
from dotenv import load_dotenv
import os
import random

load_dotenv()
fake = Faker()

categories = ['Electronics', 'Clothing', 'Home & Kitchen', 'Books', 'Beauty']

def generate_products(num_products=50):
    connection = pymysql.connect(
        host=os.getenv('MYSQL_HOST'),
        user=os.getenv('MYSQL_USER'),
        password=os.getenv('MYSQL_PASSWORD'),
        database=os.getenv('MYSQL_DATABASE')
    )
    
    try:
        with connection.cursor() as cursor:
            for _ in range(num_products):
                product = {
                    'name': fake.catch_phrase(),
                    'category': random.choice(categories),
                    'price': round(random.uniform(10, 500), 2),
                    'stock': random.randint(0, 1000)
                }
                
                cursor.execute("""
                    INSERT INTO products (name, category, price, stock)
                    VALUES (%(name)s, %(category)s, %(price)s, %(stock)s)
                """, product)
            
            connection.commit()
            print(f"Generated {num_products} products")
    finally:
        connection.close()

if __name__ == "__main__":
    generate_products()