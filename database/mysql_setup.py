import mysql.connector
from dotenv import load_dotenv
import os

load_dotenv()

def create_database():
    conn = mysql.connector.connect(
        host=os.getenv('DB_HOST'),
        user=os.getenv('DB_USER'),
        password=os.getenv('DB_PASSWORD')
    )
    
    cursor = conn.cursor()
    
    # Create database
    cursor.execute("CREATE DATABASE IF NOT EXISTS ecommerce_analytics")
    
    # Create tables
    cursor.execute("USE ecommerce_analytics")
    
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS products (
            product_id VARCHAR(36) PRIMARY KEY,
            name VARCHAR(255),
            category VARCHAR(50),
            price DECIMAL(10,2),
            rating DECIMAL(2,1),
            stock INT,
            created_at DATETIME
        )
    """)
    
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS user_behavior (
            event_id VARCHAR(36) PRIMARY KEY,
            user_id VARCHAR(36),
            event_type VARCHAR(20),
            timestamp DATETIME,
            session_id VARCHAR(36),
            device VARCHAR(20),
            location VARCHAR(10),
            product_id VARCHAR(36),
            FOREIGN KEY (product_id) REFERENCES products(product_id)
        )
    """)
    
    conn.commit()
    cursor.close()
    conn.close()

if __name__ == "__main__":
    create_database()
