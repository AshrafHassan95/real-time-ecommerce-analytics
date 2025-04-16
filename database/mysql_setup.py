import pymysql
from dotenv import load_dotenv
import os

load_dotenv()

def create_database():
    connection = pymysql.connect(
        host=os.getenv('MYSQL_HOST'),
        user=os.getenv('MYSQL_USER'),
        password=os.getenv('MYSQL_PASSWORD')
    )
    
    try:
        with connection.cursor() as cursor:
            # Create database
            cursor.execute(f"CREATE DATABASE IF NOT EXISTS {os.getenv('MYSQL_DATABASE')}")
            
            # Use the database
            cursor.execute(f"USE {os.getenv('MYSQL_DATABASE')}")
            
            # Create tables
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS products (
                    product_id INT AUTO_INCREMENT PRIMARY KEY,
                    name VARCHAR(255) NOT NULL,
                    category VARCHAR(100) NOT NULL,
                    price DECIMAL(10, 2) NOT NULL,
                    stock INT NOT NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
            
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS users (
                    user_id INT AUTO_INCREMENT PRIMARY KEY,
                    username VARCHAR(100) NOT NULL,
                    email VARCHAR(255) NOT NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
            
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS user_activity (
                    activity_id INT AUTO_INCREMENT PRIMARY KEY,
                    user_id INT NOT NULL,
                    product_id INT NOT NULL,
                    activity_type ENUM('view', 'add_to_cart', 'purchase') NOT NULL,
                    activity_data JSON,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (user_id) REFERENCES users(user_id),
                    FOREIGN KEY (product_id) REFERENCES products(product_id)
                )
            """)
            
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS ai_insights (
                    insight_id INT AUTO_INCREMENT PRIMARY KEY,
                    product_id INT NOT NULL,
                    insight_text TEXT NOT NULL,
                    generated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (product_id) REFERENCES products(product_id)
                )
            """)
            
        connection.commit()
        print("Database and tables created successfully!")
    finally:
        connection.close()

if __name__ == "__main__":
    create_database()